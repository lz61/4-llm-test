from modelscope.utils.constant import Tasks
from modelscope import Model
from modelscope.pipelines import pipeline
from modelscope import AutoModelForCausalLM, AutoTokenizer
from modelscope import GenerationConfig
import re

import gradio

# # 加载chatGLM2模型
# model = Model.from_pretrained(
#     "ZhipuAI/chatglm2-6b", device_map="auto", revision="v1.0.7"
# )
# pipe = pipeline(task=Tasks.chat, model=model)

# 加载Qwen-7B-Chat模型
tokenizer = AutoTokenizer.from_pretrained(
    "qwen/Qwen-7B-Chat", revision="v1.1.4", trust_remote_code=True
)
# added: mirror = "tuna"
model = AutoModelForCausalLM.from_pretrained(
    "qwen/Qwen-7B-Chat", revision="v1.1.4", mirror="tuna", device_map="auto", trust_remote_code=True
).eval()

model.generation_config = GenerationConfig.from_pretrained(
    "qwen/Qwen-7B-Chat", revision="v1.1.4", trust_remote_code=True
)  # 可指定不同的生成长度、top_p等相关超参


def highlight(article, keywords):
    keywords = re.split(r",|：|，|、", keywords)
    print(keywords)
    for keyword in keywords:
        keyword = keyword.strip()
        replacement = f'<em style="background-color: yellow">{keyword}</em>'
        article = article.replace(keyword, replacement, 1)
    return article


def get_tag(article):
    all_tags = [
        "体育",
        "新闻",
        "教育",
        "娱乐",
        "科技",
        "健康",
        "财经",
        "文化",
        "环境",
        "旅游",
        "历史",
        "美食",
        "科学",
        "社会",
        "家居",
        "艺术",
        "时尚",
        "互联网",
        "自然",
        "心理学",
        "电影",
        "音乐",
        "汽车",
        "房地产",
        "人物",
        "美容",
        "宠物",
        "游戏",
        "手工艺",
        "农业",
        "能源",
        "气候",
        "书籍",
        "摄影",
    ]
    tags = []
    for tag in all_tags:
        if tag in article:
            tags.append(tag)

    if len(tags) == 0:
        return ""
    else:
        return tags[0]


def build_prompt_tag(article):
    prompt_tag = f"""
    你是一个智能文章标签生成器，根据输入的文章内容，从以下备选标签中选取最合适的一个进行输出：

    体育
    新闻
    教育
    娱乐
    科技
    健康
    财经
    文化
    环境
    旅游
    历史
    美食
    科学
    社会
    家居
    艺术
    时尚
    互联网
    自然
    心理学
    电影
    音乐
    汽车
    房地产
    人物
    美容
    宠物
    游戏
    手工艺
    农业
    能源
    气候
    书籍
    摄影

    输入：{article}
    输出：

    """
    print(prompt_tag)
    return prompt_tag


# 定义prompt
prompt_summary = """
你是一款智能文章摘要生成器。你的任务如下：
对于输入的文章，生成一个能够概括文章主旨和要点的摘要。
请按照下述格式用中文输出结果：

- 摘要：（一句话或几句话，总结文章的核心内容和观点）

示例1:
用户输入：
在健康生活中，坚持适度的运动是非常重要的。适度的运动可以增强心肺功能，提高代谢率，减轻压力，改善睡眠质量，并降低患慢性疾病的风险。每天散步30分钟，骑自行车，或者参加瑜伽课程都是不错的选择。不仅如此，运动也可以增加社交互动，提高幸福感，使人更健康和快乐。

- 摘要：适度的运动对健康有益，可以提高心肺功能，减轻压力，改善睡眠质量，降低慢性疾病风险，并增加幸福感。

示例2:
用户输入：
在环保方面，减少塑料垃圾的使用是一项重要任务。塑料垃圾对环境造成了严重污染，对海洋生态系统产生了负面影响。为了减少塑料污染，我们可以采取措施，如使用可再生材料制作商品，购物时携带可重复使用的袋子，减少一次性塑料用品的使用。此外，垃圾分类和回收也是减少塑料垃圾的重要途径，有助于保护地球环境。

- 摘要：减少塑料垃圾的使用对环保至关重要，可以通过使用可再生材料，携带可重复使用袋子，垃圾分类和回收来实现。

请尽你所能生成精准的中文摘要。谢谢!

我等会会输入文章，请做好准备
"""


def build_prompt_key_sentences(article):
    prompt_key_sentences = f"""
    请输出文章中最能代表文章主题的5个关键词
    所需格式：<逗号分隔的关键词列表>
    输入：{article}
    """
    print(prompt_key_sentences)
    return prompt_key_sentences


prompt_summary_en = """
You are an intelligent article summarization generator. Your task is as follows:
For an input article, generate a summary that captures the main points and essence of the article.
Please use the following format to output the results in Chinese:

- Summary: (A sentence or a few sentences that summarize the core content and viewpoints of the article)

Example 1:
User Input:
SpaceX, founded by American entrepreneur Elon Musk, focuses on developing advanced rocket technology with the goal of achieving rocket reusability, significantly reducing launch costs, and making space more accessible and affordable. Since its establishment in 2002, SpaceX has successfully developed the Falcon series of launch vehicles. To date, SpaceX has conducted over 100 launches of Falcon 9 rockets, delivering commercial satellites, supplies for the International Space Station, and astronauts into Earth orbit. The first stage booster of the Falcon 9 rocket has been successfully reused multiple times, greatly reducing launch costs. Additionally, SpaceX is actively developing the larger Falcon Heavy rocket to enable more cost-effective heavy payload launches. SpaceX's progress has advanced the development of commercial spaceflight and provided high-quality and cost-effective launch services to governments and commercial companies worldwide. It is leading humanity into an era of interplanetary civilization, and its impact will become more prominent over time.

- Summary: SpaceX is a space exploration company founded by Elon Musk, focusing on rocket technology development for reusability, promoting commercial spaceflight, and collaborating with the International Space Station.

Example 2:
User Input:
Disney, the American entertainment giant, specializes in producing high-quality animated movies and TV programs with the goal of providing the best entertainment content, creating a diverse brand image, and delivering culture and art in a vibrant and engaging manner to humanity. Since its establishment in 1923, Disney has successfully produced numerous classic animated movies such as "Snow White," "The Lion King," and "Frozen." To date, Disney owns over 200 television channels, offering various streaming services like Disney+, ESPN+, Hulu, and more. Disney's films and shows are widely loved for their captivating stories, stunning visuals, and profound meanings. In addition, Disney is actively expanding into new entertainment businesses like theme parks, games, consumer products, aiming to diversify revenue sources and reach broader audiences. Disney's entertainment drives the development of the cultural industry and brings joy and dreams to users worldwide.

- Summary: Disney is an entertainment company that produces animated movies and TV programs, focusing on providing high-quality entertainment content, offering various streaming services, and expanding into theme parks and other businesses.

Please prepare the input article, and I'll be ready to generate accurate English summaries. Thank you!
"""

prompt_zh_to_en = """
你是一款智能文章翻译器。你的任务如下：
对于输入的文章，生成一个能够翻译成英文的翻译结果
对于人名、地名等专有名词，或者对某个词语的置信度较低，请输出它的汉语拼音
例如："天津" 翻译成 "Tianjin"
我接下来将输入中文文章：
"""

prompt_en_to_zh = """   
You are an intelligent article translator. Your task is as follows:
For an input article, generate a translation into Chinese.
I will input an English article next:
"""


# 替换html标签
def replace_tags(text):
    text = text.replace("<u>", '<em style="background-color: green">')
    text = text.replace("</u>", "</em>")
    return text


# 生成tag
def generate_tag(article):
    if len(article) > 1600:
        article = article[:1600]
    response, history = model.chat(tokenizer, build_prompt_tag(article), history=None)
    # response, history = model.chat(tokenizer, article, history=history)
    # inputs = {"text": prompt_tag, "history": []}
    # response = pipe(inputs)
    # inputs = {"text": article, "history": response["history"]}
    # response = pipe(inputs)
    # response = response["response"]
    response = get_tag(response)
    return response


# 生成中文摘要
def generate_summary(article):
    # 检查文章内容长度
    if len(article) > 1600:
        article = article[:1600]
    if len(article) < 100:
        return article
    response, history = model.chat(tokenizer, prompt_summary, history=None)
    response, history = model.chat(tokenizer, article, history=history)
    # inputs = {"text": prompt_summary, "history": []}
    # response = pipe(inputs)
    # inputs = {"text": article, "history": response["history"]}
    # response = pipe(inputs)
    # response = response["response"]
    # if len(response) > 400:
    #     response = response[:400] + "..."
    return response


# 直接生成中文摘要
def generate_summary_en(article):
    # 检查文章内容长度
    if len(article) > 1600:
        article = article[:1600]
    if len(article) < 100:
        return article
    response, history = model.chat(tokenizer, prompt_summary_en, history=None)
    response, history = model.chat(tokenizer, article, history=history)
    # inputs = {"text": prompt_summary_en, "history": []}
    # response = pipe(inputs)
    # inputs = {"text": article, "history": response["history"]}
    # response = pipe(inputs)
    # response = response["response"]
    # if len(response) > 400:
    #     response = response[:400] + "..."
    return response


# 英文翻译成中文
def generate_summary_en_to_zh(article):
    if len(article) > 1600:
        article = article[:1600]
    if len(article) < 100:
        return article
    # article_en = generate_summary_en(article)
    article_en = article  # 直接读取数据库里的摘要
    # response, history = model.chat(tokenizer, prompt_summary_en, history=None)
    response, history = model.chat(tokenizer, prompt_en_to_zh, history=None)
    response, history = model.chat(tokenizer, article_en, history=history)
    # inputs = {"text": prompt_summary_en, "history": []}
    # inputs = {"text": prompt_en_to_zh, "history": []}
    # response = pipe(inputs)
    # inputs = {"text": article_en, "history": response["history"]}
    # response = pipe(inputs)
    # response = response["response"]
    # if len(response) > 400:
    #     response = response[:400] + "..."
    return response


# 中文翻译成英文
def generate_summary_zh_to_en(article):
    if len(article) > 1600:
        article = article[:1600]
    if len(article) < 100:
        return article
    # article_zh = generate_summary(article)
    article_zh = article  # 直接读取数据库里的摘要
    # response, history = model.chat(tokenizer, prompt_summary_en, history=None)
    response, history = model.chat(tokenizer, prompt_zh_to_en, history=None)
    response, history = model.chat(tokenizer, article_zh, history=history)
    # inputs = {"text": prompt_summary_en, "history": []}
    # inputs = {"text": prompt_translate, "history": []}
    # response = pipe(inputs)
    # inputs = {"text": article_zh, "history": response["history"]}
    # response = pipe(inputs)
    # response = response["response"]
    # if len(response) > 400:
    #     response = response[:400] + "..."
    return response


# 关键词高亮
def generate_key_sentences(article):
    # 检查文章内容长度
    if len(article) > 1600:
        article = article[:1600]
    if len(article) < 50:
        return article
    response, history = model.chat(
        tokenizer, build_prompt_key_sentences(article), history=None
    )
    response = highlight(article, response)
    # response, history = model.chat(tokenizer, article, history=history)
    # inputs = {"text": prompt_key_sentences, "history": []}
    # response = pipe(inputs)
    # inputs = {"text": article, "history": response["history"]}
    # response = pipe(inputs)
    # response = response["response"]
    # response = replace_tags(response)
    return response


def build_prompt(query, ranked_docs, score_baseline):
    # 将相似度较高的文本组织起来
    ranked_results_section = ""
    for rank, (score, sentence) in enumerate(ranked_docs):
        if score > score_baseline:
            ranked_results_section += f"{rank+1}. {score}. {sentence}\n"
    print("ranked_results_section:", ranked_results_section)
    # 设计 prompt
    if ranked_results_section == "":
        print("无法找到相关的知识")
        return "无法找到相关的知识"
    else:
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


def response_qa(query, ranked_docs, descriptions, titles, links):
    # 构建 prompt
    score_baseline = 50
    prompt = build_prompt(query, ranked_docs, score_baseline)
    if prompt == "无法找到相关的知识":
        # result_with_prompt = "抱歉，您询问的问题超出了我的知识范围。"
        return "抱歉，您询问的问题超出了我的知识范围。"
    else:
        result_with_prompt, history = model.chat(tokenizer, prompt, history=None)
    # result_without_prompt, history = model.chat(tokenizer, query[0], history=None)

    # inputs = {"text": query[0], "history": []}
    # result_without_prompt = pipe(inputs)
    # result_without_prompt = result_without_prompt["response"]
    # inputs = {"text": prompt, "history": []}
    # result_with_prompt = pipe(inputs)
    # result_with_prompt = result_with_prompt["response"]

    output_text = (
        # f"\n未接入本地知识库时的回答: {result_without_prompt}\n"
        f"{result_with_prompt}"
    )
    # 如果没有找到相关的知识，则直接返回
    if prompt == "无法找到相关的知识":
        return output_text

    # 获取排名较高的文本的标题和链接并添加到输出文本中
    ranked_titles_set = set()  # 用于存储已出现的标题
    ranked_titles_and_links = []  # 用于存储排名较高的、不重复的标题和链接
    rank_counter = 0  # 用于维护连续的排名
    for _, (score, sentence) in enumerate(ranked_docs):
        if score < score_baseline:
            continue
        i = descriptions.index(sentence)
        title = titles[i]
        link = links[i]
        if title not in ranked_titles_set:
            ranked_titles_set.add(title)
            rank_counter += 1  # 增加排名计数
            # 将标题和链接组成超链接形式的 HTML 标签，并包含排名
            ranked_titles_and_links.append(
                f'{rank_counter}. <a href="{link}">{title}</a>'
            )

    # 构建排名较高的文本来源和标题部分的 HTML 标签
    ranked_titles_section = "<br>".join(ranked_titles_and_links)
    output_text += f"\n\n回答基于的文本来源于：<br>{ranked_titles_section}"

    return output_text
