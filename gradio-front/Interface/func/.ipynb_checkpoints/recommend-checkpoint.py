import pandas as pd
import json
import torch
from sklearn.cluster import DBSCAN
from sklearn.cluster import KMeans
import numpy as np
from datetime import datetime
import math
import faiss
import random
from Interface.LLM.LLM_generate_embedding import generate_embedding
import zipfile

# 读取用户数据
def read_csv_data(csv_file_path, user_id):
    df = pd.read_csv(csv_file_path, names=['user_id', 'article_id', 'time', 'operation']) # 没有id这一列
    filtered_df = df[df['user_id'] == str(user_id)]
    # 提取用户读过的文章 id 列表，用于聚类
    article_ids_str = filtered_df['article_id'].tolist() 
    article_ids = [int(x) for x in article_ids_str]
    return df, article_ids

# 获得每个用户读过的所有文章信息，每篇包含文章标题、关键词、摘要
def get_article_basic_info(jsonl_file_path, target_id_list):
    article_list = []
    tag_list = []  # 用于多样性推荐（粗粒度筛选）
    with zipfile.ZipFile('./data/Data.zip','r') as zip_ref:
        with zip_ref.open(jsonl_file_path) as file:
            while True:
                line_bytes = file.readline()
                line = line_bytes.decode('utf-8').strip()
                if line is None or line == "":
                    break
                json_data = json.loads(line)
                article_id = json_data['Id']  
                if article_id in target_id_list:
                    tag = json_data['Tag']
                    title = json_data['Title']
                    keyword = json_data['Keywords']
                    summary = json_data['Summary']
                    
                    combined_text = f"{tag} {title} {keyword} {summary}"
                    article_list.append(combined_text)
  
    return article_list

# 对用户读过的文章的标题、关键词、摘要进行 embedding

# 对 embedding 进行聚类，用于将文章分为不同主题类
def dbscan_clustering(embeddings, eps, min_samples):
    dbscan = DBSCAN(eps=eps, min_samples=min_samples, metric='cosine')
    labels = dbscan.fit_predict(embeddings)
    clustered_article_indices = {}
    for idx, label in enumerate(labels):  
        if label not in clustered_article_indices:
            clustered_article_indices[label] = []
        clustered_article_indices[label].append(idx)
    return clustered_article_indices

# 计算每个类别的 embedding 表示（该类别下所有文章的 embedding 的均值）
def calculate_cluster_embeddings(clustered_article_indices, article_embs):
    cluster_embeddings = {}
    for label, indices in clustered_article_indices.items():
        cluster_embs = [article_embs[idx] for idx in indices]
        cluster_embs_avg = np.mean(cluster_embs, axis=0)
        cluster_embeddings[label] = cluster_embs_avg
    return cluster_embeddings

# 计算时间衰减因子，距今时间越久远，则权重越低
def calculate_decay_factor(time_diff, decay_rate):
    return np.exp(-decay_rate * time_diff)

# 综合考虑时间衰减和用户行为，计算权重
def calculate_weight(operation, decay, weight_factor):
    if operation == 'view':
        return decay * weight_factor['view']
    elif operation == 'star':
        return decay * weight_factor['star']
    else:
        return 0

# 计算每篇文章的权重
def calculate_article_weights(df, decay_rate, weight_factor):
    now = datetime.now()
    article_weights = {}
    for index, row in df.iterrows():
        if index == 0:  # 跳过第一行表头
            continue
        article_id = int(row['article_id'].strip())
        operation = row['operation'].strip()
        operation_time_str = row['time'].strip()  # 去除开头和结尾的空格    
        operation_time = datetime.strptime(operation_time_str, '%Y-%m-%d')
        
        time_diff = (now - operation_time).days
        decay = calculate_decay_factor(time_diff, decay_rate)
        weight = calculate_weight(operation, decay, weight_factor)
        
        if article_id not in article_weights:
            article_weights[article_id] = 0
        article_weights[article_id] += weight
    
    return article_weights 

# 计算主题类权重（用于确定每个类别将要推荐的文章数量）
def calculate_cluster_weights(clustered_article_indices, article_weights, article_ids):
    cluster_weights = {}  
    for label, indices in clustered_article_indices.items():
        weight_sum = 0.0  
        # 仅累加一个类别下所有文章的权重（可以考虑后续优化）
        for idx in indices:
            article_id = article_ids[idx]
            weight = article_weights[article_id] 
            weight_sum += weight
        cluster_weights[label] = weight_sum
        
    # 计算总的权重和
    total_weight = sum(cluster_weights.values())
    # 归一化每个类别的权重
    for label in cluster_weights:
        cluster_weights[label] /= total_weight
        
    return cluster_weights

# 根据主题类权重，计算每个类别要推荐的文章数量
def calculate_cluster_recommendations(cluster_weights, total_recommendations):
    cluster_recommendations = {}
    initial_sum = 0
    adjustment_needed = 0
    non_zero_clusters = []
    
    for cluster_index, weight in cluster_weights.items():
        num_recommendations = math.floor(weight * total_recommendations)  # 向下取整，多的再调整
        if num_recommendations == 0:
            num_recommendations = 1
            cluster_recommendations[cluster_index] = num_recommendations
        else:
            non_zero_clusters.append(cluster_index)
        initial_sum += num_recommendations        
    
    adjustment_needed += (total_recommendations - initial_sum)
        
    for cluster_index in non_zero_clusters:
        num_recommendations = math.floor(cluster_weights[cluster_index] * total_recommendations)
        if adjustment_needed > 0:
            num_recommendations += 1
            adjustment_needed -= 1
        cluster_recommendations[cluster_index] = num_recommendations
    
    return cluster_recommendations

# 推荐
def recommend(faiss_index_path, cluster_embeddings, cluster_recommendations, diversity_num, article_ids):

    # 加载离线做好的 Embedding 索引
    index = faiss.read_index(faiss_index_path)

    recommend_based_on_similarity = []
    recommend_based_on_diversity = []

    topk = 1000
    radius = 50
    
    # 对每个类别进行召回
    for cluster_index, num_recommendations in cluster_recommendations.items(): # 这里的 num_recommendations 是相似性的推荐数量
        
        cluster_emb = cluster_embeddings[cluster_index]  
        scores, ids = index.search(cluster_emb.reshape(1, -1), topk) 
        
        ids[0] = [i+1 for i in ids[0]]  # 向量数据库的索引从0开始，而 article_id 从1开始
        sorted_ids = [idx for _, idx in sorted(zip(scores[0], ids[0]), reverse=True)]
                
        # 去除重复推荐和已经阅读过的的文章
        sorted_ids = [id for id in sorted_ids if id not in recommend_based_on_similarity and id not in recommend_based_on_diversity and id not in article_ids]
        # 推荐：基于相似性         
        recommend_based_on_similarity.extend(sorted_ids[:num_recommendations])
        # 推荐：基于多样性
        diversity_list = random.sample(sorted_ids[-(len(sorted_ids)-radius):], 10) # 为排名引入随机性：在后 50个中随机选取 10个
        recommend_based_on_diversity.extend(diversity_list)
    # 多样性随机筛选   
    recommend_based_on_diversity = random.sample(recommend_based_on_diversity, diversity_num) # 目前多样性推荐是 3个
        
    return recommend_based_on_similarity, recommend_based_on_diversity


def recommend_func(csv_file_path, user_id):
    
    # 目前数据只考虑中文
    jsonl_file_path = 'data_zh.jsonl' 
    faiss_index_path = './data/info_index_zh.faiss'
    
    # 计算每个类别要推荐的文章数量
    total_recommendations = 9 
    
    # 读取用户数据
    df, article_ids = read_csv_data(csv_file_path, user_id) 
    
    # 冷启动预案
    if len(article_ids) == 0:
        recommend_article_ids = random.sample(range(1, 2001), total_recommendations)
    else:
        if len(article_ids) < 5:
            similarity_ratio = 0.4
        else:
            similarity_ratio = 0.7
    
        # 获取用户阅读过的文章关键信息（已提前离线完成）
        article_list = get_article_basic_info(jsonl_file_path, article_ids)

        # 对用户阅读的文章进行 embedding
        article_embs = generate_embedding(article_list)

        # 对 embedding 用 DBSCAN 进行聚类
        eps = 0.4  # 邻域半径
        min_samples = 2  # 最小样本数
        clustered_article_indices = dbscan_clustering(article_embs, eps, min_samples)

        # 计算每个类别的 embedding 表示
        cluster_embeddings = calculate_cluster_embeddings(clustered_article_indices, article_embs)

        # 计算每个类别的权重
        decay_rate = 0.005  # 时间衰减系数：越大的话，相同的时间间隔会导致分差变大
        weight_factor = {'view': 1, 'star': 1.5}  # 用户行为权重：越大表示该行为级重要程度越高
        article_weights = calculate_article_weights(df, decay_rate, weight_factor)
        cluster_weights = calculate_cluster_weights(clustered_article_indices, article_weights, article_ids)

        # 根据 weight 排序（让权重较大的放在前面推荐）
        cluster_weights = dict(sorted(cluster_weights.items(), key=lambda item: item[1], reverse=True))

        similarity_num = math.floor(total_recommendations * similarity_ratio)
        diversity_num = total_recommendations - similarity_num
        cluster_recommendations = calculate_cluster_recommendations(cluster_weights, similarity_num)

        # 推荐：兼顾相似性和多样性
        recommend_based_on_similarity, recommend_based_on_diversity = recommend(faiss_index_path, cluster_embeddings, cluster_recommendations, diversity_num, article_ids)
        recommend_article_ids = recommend_based_on_similarity + recommend_based_on_diversity
    
    return recommend_article_ids