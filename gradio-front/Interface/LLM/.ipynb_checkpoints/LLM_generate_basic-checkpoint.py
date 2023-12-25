# from modelscope.utils.constant import Tasks
# from modelscope import Model
# from modelscope.pipelines import pipeline
from modelscope import AutoModelForCausalLM, AutoTokenizer
from modelscope import GenerationConfig

import gradio

# # 加载chatGLM模型
# model = Model.from_pretrained('ZhipuAI/chatglm2-6b', device_map='auto', revision='v1.0.7')
# pipe = pipeline(task=Tasks.chat, model=model)

tokenizer = AutoTokenizer.from_pretrained(
    "qwen/Qwen-7B-Chat", revision="v1.0.5", trust_remote_code=True
)
model = AutoModelForCausalLM.from_pretrained(
    "qwen/Qwen-7B-Chat", revision="v1.0.5", device_map="auto", trust_remote_code=True
).eval()
model.generation_config = GenerationConfig.from_pretrained(
    "qwen/Qwen-7B-Chat", revision="v1.0.5", trust_remote_code=True
)  # 可指定不同的生成长度、top_p等相关超参

# 定义prompt
prompt_summary = """
你是一款智能文章摘要生成器。你的任务如下：
对于输入的文章，生成一个能够概括文章主旨和要点的摘要。
请按照下述格式用中文输出结果：

- 摘要：（一句话或几句话，总结文章的核心内容和观点）

示例1:
用户输入：
在美国创业家伊隆·马斯克创立的太空探索公司SpaceX，专注于研发先进的运载火箭技术，其目标是实现火箭的再利用，大幅降低发射成本，使宇宙空间更加方便、经济地可达。自2002年成立以来，SpaceX已成功研制出Falcon系列运载火箭。迄今为止，SpaceX已进行过100多次Falcon 9火箭的发射任务，将商业卫星、国际空间站的物资和宇航员送入地球轨道。Falcon 9火箭第一级加速器实现了多次回收再利用，大大降低了发射成本。此外，SpaceX也在积极研发大型的Falcon Heavy火箭，力争实现更经济的重型载荷发射。SpaceX公司的进步推进了商业航天事业的发展，为各国政府和商业公司提供了高质量又经济的发射服务。它正引领人类迈向多行星文明的时代，其推动作用将随着时间进一步凸显。

- 摘要：SpaceX是伊隆马斯克创办的太空探索公司，专注于研发火箭技术，实现再利用，促进商业航天发展，并与国际空间站合作。

示例2:
用户输入：
在美国娱乐巨头迪士尼公司，专注于制作优质的动画电影和电视节目，其目标是提供最好的娱乐内容，打造多元化的品牌形象，使文化和艺术更加生动、有趣地传递给人类。自1923年成立以来，迪士尼公司已成功制作出《白雪公主》、《狮子王》、《冰雪奇缘》等多部经典的动画电影。迄今为止，迪士尼公司已拥有超过200个电视频道，为用户提供了迪士尼+、ESPN+、Hulu等多种流媒体服务。迪士尼公司的电影和节目以其故事精彩、画面精美、寓意深刻而受到广泛喜爱。此外，迪士尼公司也在积极拓展新型的娱乐业务，如主题公园、游戏、消费品等，力争实现更多样的收入来源和更广泛的受众群体。迪士尼公司的娱乐推动了文化产业的发展，为全球用户提供了欢乐和梦想。

- 摘要：迪士尼是制作动画电影和电视节目的娱乐公司，专注于提供优质的娱乐内容，拥有多种流媒体服务，并拓展主题公园等业务。

请尽你所能生成精准的中文摘要。谢谢!

我等会会输入文章，请做好准备
"""

prompt_key_sentences = """
你是一款智能文章关键句高亮的生成器。你的任务如下：
根据输入的文章内容，请使用"<u>" "</u>"来标注出文章中重要的句子，然后输出。

以下是两个示例

示例 1：
文章：
"太阳是太阳系中的一颗恒星。它提供了地球上所有生命所需的能量。地球绕太阳旋转。我们的太阳是一颗中等大小的恒星，有上亿年的寿命。它的存在对地球上的生命至关重要。在古代，许多文化都崇拜太阳作为神祇，因为它对人类和其他生物的生存具有无可替代的意义。对于地球上的大多数生物，没有太阳的光和热，生命将无法持续。"
关键句子：
"<u>太阳是太阳系中的一颗恒星。</u>它提供了地球上所有生命所需的能量。地球绕太阳旋转。<u>我们的太阳是一颗中等大小的恒星，有上亿年的寿命。</u>它的存在对地球上的生命至关重要。在古代，许多文化都崇拜太阳作为神祇，因为它对人类和其他生物的生存具有无可替代的意义。<u>对于地球上的大多数生物，没有太阳的光和热，生命将无法持续。</u>"

示例 2：
文章：
"苹果是一种流行的水果。它们有很多种类，如红富士、青苹果等。很多人喜欢它的味道。苹果不仅味道鲜美，还含有大量的营养成分，如维生素C和纤维。这种水果在全球范围内广受欢迎。由于其丰富的营养价值和多种健康益处，苹果经常被描述为'每日一苹果，医生远离我'的食物。无论是作为零食还是在料理中，它都是人们的首选之一。"
关键句子：
"苹果是一种流行的水果。<u>它们有很多种类，如红富士、青苹果等。</u>很多人喜欢它的味道。<u>苹果不仅味道鲜美，还含有大量的营养成分，如维生素C和纤维。</u>这种水果在全球范围内广受欢迎。由于其丰富的营养价值和多种健康益处，<u>苹果经常被描述为'每日一苹果，医生远离我'的食物。</u>无论是作为零食还是在料理中，它都是人们的首选之一。"

根据上述示例，请识别以下文章的关键句子并在文章中使用<u></u>标签来高亮：

我等会会输入文章，请做好准备
"""


def generate_summary(article):
    response, history = model.chat(tokenizer, prompt_summary, history=None)
    response, history = model.chat(tokenizer, article, history=history)
    return response


def generate_key_sentences(article):
    response, history = model.chat(tokenizer, prompt_key_sentences, history=None)
    response, history = model.chat(tokenizer, article, history=history)
    return response
