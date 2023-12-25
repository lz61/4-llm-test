import pandas as pd
import jsonlines
import json
import zipfile

def transform_to_csv(input, path):
    df = pd.DataFrame(input)
    df.to_csv(path, index=False)

def get_articleId_by_title(title):
    # 通过文章标题获得文章id
    with zipfile.ZipFile('./data/Data.zip','r') as zip_ref:
        file_list = zip_ref.namelist()
        for filename in file_list:
            with zip_ref.open(filename) as file:
                while True:
                    line_bytes = file.readline()
                    line = line_bytes.decode('utf-8').strip()
                    if line is None or line == "":
                        break
                    data_json = json.loads(line)
                    if data_json['Title'] == title:
                        return data_json['Id']
    
    return None

def get_article_by_id(id):
    with zipfile.ZipFile('./data/Data.zip','r') as zip_ref:
        file_list = zip_ref.namelist()
        for filename in file_list:
            with zip_ref.open(filename) as file:
                while True:
                    line_bytes = file.readline()
                    line = line_bytes.decode('utf-8').strip()
                    if line is None or line == "":
                        break
                    data_json = json.loads(line)
                    if data_json['Id'] == id:
                        return data_json
    
    return None

def get_article_by_title(title):
    with zipfile.ZipFile('./data/Data.zip','r') as zip_ref:
        file_list = zip_ref.namelist()
        for filename in file_list:
            with zip_ref.open(filename) as file:
                while True:
                    line_bytes = file.readline()
                    line = line_bytes.decode('utf-8').strip()
                    if line is None or line == "":
                        break
                    data_json = json.loads(line)
                    if data_json['Title'] == title:
                        return data_json
    
    return None

def get_article_title_by_id(id):
    with zipfile.ZipFile('./data/Data.zip','r') as zip_ref:
        file_list = zip_ref.namelist()
        for filename in file_list:
            with zip_ref.open(filename) as file:
                while True:
                    line_bytes = file.readline()
                    line = line_bytes.decode('utf-8').strip()
                    if line is None or line == "":
                        break
                    data_json = json.loads(line)
                    if data_json['Id'] == id:
                        return data_json['Title']
    
    return None


if __name__ == "__main__":
    print(get_articleId_by_title("恐龙灭绝后，这里记录下完整的地球故事"))
    print(get_article_by_id(1))
    print(get_article_title_by_id(1))
    print(get_article_by_title("恐龙灭绝后，这里记录下完整的地球故事"))