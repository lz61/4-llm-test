import pandas as pd
from Interface.util.util import get_article_title_by_id

class Recommend:
    # 内容推荐页面静态数据
    choices = []
    choices_without_sign = []
    default_values = []
    examples = []
    def __init__(self):
        data = pd.read_csv('./data/user.csv')
        user_ids = data['user_id'].unique().tolist()
        for id in user_ids:
            username = "用户" + str(id)
            user_data = data[data["user_id"]==id]['article_id'].tolist()
            titles = []
            for article_id in user_data:
                article_title = get_article_title_by_id(article_id)
                if article_title is not None:
                    titles.append("《" + article_title + "》")

            user_description_data = pd.read_csv('./data/user_description.csv')
            user_description = user_description_data[user_description_data['user_id']==id]['description'].tolist()[0]
            user = [username,user_description,titles]
            self.examples.append(user)
        
        article_ids = data['article_id'].unique().tolist()
        for article_id in article_ids:
            article_title = get_article_title_by_id(article_id)
            if article_title is not None:
                self.choices_without_sign.append(article_title)
                self.choices.append("《" + article_title + "》")
        
        for value in self.examples[0][2]:
            self.default_values.append(value[1:-1])


class ArticleDetail:
    # 文章详情页面静态数据
    examples = []
    def __init__(self):
        data = pd.read_csv('./data/article_detail.csv')
        ids = data['id'].to_list()
        titles = data['title'].to_list()
        languages = data['language'].to_list()
        examples = []
        for i in range(len(ids)):
            examples.append([ids[i],titles[i],languages[i]])
        self.examples = examples

import csv

class CustomURL:
    
    csv_file_path = './data/custom_url.csv'
    examples = []

    @classmethod
    def load_data(cls):
        with open(cls.csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
            csvreader = csv.DictReader(csvfile)
            for row in csvreader:
                site = row['Site']
                link = row['Link']
                cls.examples.append([site, link])

class IntelligentQA:
    # 智能QA页面的静态数据
    # 建议标题最多20个字保证排版好看
    choices = []
    choices_without_sign = []
    default_values = []
    examples = []
    def __init__(self):
        data = pd.read_csv('./data/user.csv')
        user_ids = data['user_id'].unique().tolist()
        for id in user_ids:
            username = "用户" + str(id)
            user_data = data[data["user_id"]==id]['article_id'].tolist()
            titles = []
            for article_id in user_data:
                article_title = get_article_title_by_id(article_id)
                if article_title is not None:
                    titles.append("《" + article_title + "》")

            user_description_data = pd.read_csv('./data/user_description.csv')
            user_description = user_description_data[user_description_data['user_id']==id]['description'].tolist()[0]
            user = [username,user_description,titles]
            self.examples.append(user)
        
        article_ids = data['article_id'].unique().tolist()
        for article_id in article_ids:
            article_title = get_article_title_by_id(article_id)
            if article_title is not None:
                self.choices_without_sign.append(article_title)
                self.choices.append("《" + article_title + "》")
        
        for value in self.examples[0][2]:
            self.default_values.append(value[1:-1])

QA_instance = IntelligentQA()
Recommend_instance = Recommend()
detail_instance = ArticleDetail()