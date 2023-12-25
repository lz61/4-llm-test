import pandas as pd
import re
import json
import os
import torch
import faiss
import pickle
from Interface.LLM.LLM_generate_basic import response_qa
from Interface.LLM.LLM_generate_embedding import generate_embedding
import zipfile


# 读取用户数据（阅读过的文章id列表）
def read_csv_data(csv_file_path, user_id):
    df = pd.read_csv(
        csv_file_path, names=["user_id", "article_id", "time", "operation"]
    )
    # 读取特定用户的数据
    filtered_df = df[df["user_id"] == str(user_id)]
    # 提取用户读过的文章 id 列表，用于聚类
    article_ids_str = filtered_df["article_id"].tolist()
    article_ids = [int(x) for x in article_ids_str]
    return article_ids


def split_text(text, max_length=300):
    # 清除多余的空格和换行符
    text = text.replace("\n", "")
    text = text.replace("\n\n", "")
    text = re.sub(r"\s+", " ", text)
    # 按照句子分割文章
    sentences = re.split("(；|。|！|\!|\.|？|\?)", text)
    # 按照 max_length 的长度限制，把多个句子组成一个小段落
    paragraphs = []
    current_length = 0
    current_paragraph = ""
    for sentence in sentences:
        sentence_length = len(sentence)
        if current_length + sentence_length <= max_length:
            current_paragraph += sentence
            current_length += sentence_length
        else:
            paragraphs.append(current_paragraph.strip())
            current_paragraph = sentence
            current_length = sentence_length
    paragraphs.append(current_paragraph.strip())
    return paragraphs


# 生成器函数（yield）：逐批读取并分割文本
def prepare_data_from_file(file_path, article_ids, batch_size):
    chunk_data = []  # 包含描述、标题和链接的字典列表
    with zipfile.ZipFile("./data/Data.zip", "r") as zip_ref:
        with zip_ref.open(file_path) as f:
            for line in f:
                line = line.decode("utf-8")
                try:
                    json_data = json.loads(line)
                    article_id = json_data["Id"]

                    if article_id in article_ids:
                        description = json_data.get("Description", "")
                        title = json_data.get("Title", "")
                        link = json_data.get("Link", "")  # 提取链接
                        split_description = split_text(description)
                        chunk_data += [
                            {"description": chunk, "title": title, "link": link}
                            for chunk in split_description
                        ]
                        if len(chunk_data) >= batch_size:
                            yield chunk_data[:]
                            chunk_data.clear()
                except json.JSONDecodeError:
                    print(f"Failed to decode JSON: {line}")
                    continue
    if chunk_data:
        yield chunk_data


def prepare_data_from_folder(folder_path, batch_size):
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)

        if os.path.isfile(file_path) and file_name.endswith(".jsonl"):
            yield from prepare_data_from_file(file_path, batch_size)


# def generate_embedding(pipeline_se, text_list):
#     with torch.no_grad():
#         embs = pipeline_se(input={"source_sentence": text_list})["text_embedding"]
#     return embs


def build_index(file_path, article_ids, batch_size):
    dim = 768
    index = faiss.IndexFlatIP(dim)
    descriptions = []  # 存储描述
    titles = []  # 存储标题
    links = []  # 存储链接
    for chunk_data in list(prepare_data_from_file(file_path, article_ids, batch_size)):
        for chunk in chunk_data:
            descriptions.append(chunk["description"])
            titles.append(chunk["title"])
            links.append(chunk["link"])
        embs = generate_embedding([chunk["description"] for chunk in chunk_data])
        # embs = generate_embedding(
        #     pipeline_se, [chunk["description"] for chunk in chunk_data]
        # )
        index.add(embs)

    print("finish building index of corpus")
    return index, descriptions, titles, links


def save_index_and_corpus(index, descriptions, titles, links, index_path, corpus_path):
    faiss.write_index(index, index_path)

    data_to_save = {"descriptions": descriptions, "titles": titles, "links": links}
    with open(corpus_path, "wb") as corpus_file:
        pickle.dump(data_to_save, corpus_file)


def load_index_and_corpus(index_path, corpus_path):
    index = faiss.read_index(index_path)

    with open(corpus_path, "rb") as corpus_file:
        data = pickle.load(corpus_file)
        descriptions = data["descriptions"]
        titles = data["titles"]
        links = data["links"]

    return index, descriptions, titles, links


def search(index, query, corpus, topk=3):
    # 将 query 向量化，用于在向量库中进行相似度匹配
    q_embs = generate_embedding(query)

    # 在知识库中选取 topk 个最相似的文本返回
    scores, ids = index.search(
        q_embs.reshape(1, -1), topk
    )  # scores[]列表中，每个元素表示一个query与语料库中所有文本块的相似度分数列表
    candidate_docs = [corpus[int(i)] for i in ids[0]]  # 注意：目前只针对单个query，所以用 ids[0]
    ranked_docs = sorted(
        zip(scores[0], candidate_docs), key=lambda x: x[0], reverse=True
    )

    return ranked_docs


# def rank_text(pipeline_rank, query, candidate_docs):
#     # 二次的细粒度排序 （推荐系统中二次排序算法会更复杂）
#     scores = pipeline_rank(
#         input={"source_sentence": query, "sentences_to_compare": candidate_docs}
#     )["scores"]
#     ranked_docs = sorted(zip(scores, candidate_docs), key=lambda x: x[0], reverse=True)
#     return ranked_docs


def build_prompt(query, ranked_docs):
    # 将相似度较高的文本组织起来
    ranked_results_section = ""
    for rank, (score, sentence) in enumerate(ranked_docs):
        ranked_results_section += f"{rank+1}. {score}. {sentence}\n"
    # 设计 prompt
    prompt = f"""
    你是一个智能问答助手，你需要根据用户的提问，并结合给出的知识库，来回答用户的问题。

    用户的提问如下：

    > {query}

    你拥有的知识库，这些知识已经按照和用户所提问题的相关性进行了筛选和排序，它们的排名、得分、对应的知识背景如下：

    | 排名 | 得分 | 知识背景 |
    |---|---|---|
    {ranked_results_section}

    请参考知识库中得分较高的内容，忽略得分较低的内容，结合你自己的判断，给出你的回答。

    你的回答应该分为多个点，每个点的回答不超过100字。

    > 例如：
    >
    > - 1.
    > - 2.
    > - 3.

    请尽量保证你的回答是全面、准确、客观的。
    """
    return prompt


def generate_response(pipeline_chat, query, prompt):
    result_without_prompt = pipeline_chat(input={"text": query, "history": []})
    result_with_prompt = pipeline_chat(input={"text": prompt, "history": []})
    return result_without_prompt, result_with_prompt


def intelligent_qa_func(article_ids, user_query):
    csv_file_path = "../Data/Recommend/test.csv"
    json_file_path = "../Data/data_zh.jsonl"

    csv_file_path = "../Data/Recommend/test.csv"
    json_file_path = "data_zh.jsonl"
    batch_size = 20

    # 读取用户数据
    # article_ids = read_csv_data(csv_file_path, user_id)
    # article_ids = list(range(1,11))

    # 用户提问
    query = []
    query.append(user_query)

    # 生成本地知识库 embedding
    index, descriptions, titles, links = build_index(
        json_file_path, article_ids, batch_size
    )

    # 召回
    ranked_docs = search(index, query, descriptions, topk=5)

    # 排序
    # ranked_docs = rank_text(pipeline_rank, query, candidate_docs)

    # 调用问答模型
    output_text = response_qa(query, ranked_docs, descriptions, titles, links)

    return output_text
