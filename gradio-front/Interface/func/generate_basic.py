import jsonlines
import sys

# # 添加 LLM 文件夹到搜索路径
# sys.path.append('./LLM')

from Interface.LLM.LLM_generate_basic import generate_summary
from Interface.LLM.LLM_generate_basic import generate_key_sentences
from Interface.LLM.LLM_generate_basic import generate_summary_en
from Interface.LLM.LLM_generate_basic import generate_summary_zh_to_en
from Interface.LLM.LLM_generate_basic import generate_summary_en_to_zh
from Interface.util.util import get_article_by_id, get_articleId_by_title


def generate_basic_func(article_id, language, key_sentences=True):
    data = get_article_by_id(article_id)
    if data is None:
        link = "https://www.zhihu.com/question/618895483"
        title = "Sample Title"
        publishDate = "2023-08-24"
        tag = "Technology"
        imgLink = "https://pic1.zhimg.com/v2-d9fee183f9196303fa5d8b96a2c023e6_r.jpg?source=1940ef5c"
        description = "据央视新闻客户端24日报道，当地时间8月24日13时，日本福岛第一核电站启动核污染水排海。东京电力公司24日在临时记者会上宣布，今天的核污染水排放量预计为200到210吨，每天的排放情况将在次日公布。首次排海每天将排放约460吨，持续17天，合计排放约7800立方米核污染水。据日本共同社，福岛第一核电站的核污染水约有134万吨，2023年度将把约3.12万吨核污染水分4次排放，每次约排放7800吨。根据东电计算，用海水稀释过的核污染水将缓慢流过约1公里的隧道，约1000秒之后抵达大海。根据计划，排海时间至少持续30年。中国生态环境部核与辐射安全中心首席专家刘新华表示：由于福岛第一核电站退役需要数十年，这个过程中还会持续产生大量核污染水，排放时间可能远超30年，核污染水排海将会对海洋生态产生长期影响。"
    link = data["Link"]
    title = data["Title"]
    publishDate = data["PubDate"]
    tag = data["Tag"]
    imgLink = data["ImgLink"]
    description = data["Description"]
    summary = data["Summary"]
    article_language = data["Language"]
    if language == "English":
        if article_language == "en":
            # description = generate_summary_en(description)
            description = summary  # 直接读取数据库里的摘要
        else:
            description = generate_summary_zh_to_en(summary)  # summary传进去
        print(f"EN: {description}")
    else:
        if article_language == "zh":
            # description = generate_summary(description)
            description = summary  # 直接读取数据库里的摘要
        else:
            description = generate_summary_en_to_zh(summary)  # summary传进去
        print(f"ZH: {description}")
    # 关键句下划线
    if key_sentences:
        description = generate_key_sentences(description)
    return link, title, publishDate, tag, imgLink, description
    # shown_title = f"""
    #     <br>
    #     <div style="text-align: center;">
    #         <a href="{link}"><h1>{title}</h1></a>
    #     </div>
    # """
    # shown_publishDate_tag = f"""
    #     <p style="text-align: center;">
    #         <span  style="display:inline-block;margin-right:100px;">{publishDate}</span>
    #         <span>{tag}</span>
    #     </p>
    # """
    # return shown_title, shown_publishDate_tag, imgLink, description
