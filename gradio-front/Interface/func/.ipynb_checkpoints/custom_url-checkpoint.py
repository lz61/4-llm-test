import jsonlines
import sys

# # 添加 LLM 文件夹到搜索路径
# sys.path.append('./LLM')

from Interface.LLM.LLM_generate_basic import generate_summary
from Interface.LLM.LLM_generate_basic import generate_key_sentences
from Interface.LLM.LLM_generate_basic import generate_summary_en
from Interface.LLM.LLM_generate_basic import generate_tag


# 这个函数其实只用到了description
def generate_summary_tag_func(link, title, publishDate, tag, imgLink, description):
    tag = generate_tag(description)
    description = generate_summary(description)
    return link, title, publishDate, tag, imgLink, description
