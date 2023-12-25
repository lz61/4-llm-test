import gradio as gr

from Interface.func.recommend import recommend_func
from Interface.util.process_output_recommend import process_output_recommend
from Interface.util.static import Recommend_instance
from Interface.util.util import (
    get_articleId_by_title,
    transform_to_csv,
    get_article_by_id,
)
import pandas as pd
from datetime import datetime, timedelta
import random


def change_username_while_change_articles():
    return "自定义用户"


def recommend(person, articles):
    user_id = 1
    article_ids = []
    for article in articles:
        article_id = get_articleId_by_title(article)
        if article_id is not None:
            article_ids.append(article_id)

    length = len(articles)
    user_ids = [user_id for _ in range(length)]

    start_date = datetime(2023, 9, 1)
    times = [start_date - timedelta(days=i) for i in range(length)]

    operations = [random.choice(["view", "star"]) for _ in range(length)]

    custom_data = {
        "user_id": user_ids,
        "article_id": article_ids,
        "time": times,
        "operation": operations,
    }

    csv_file_path = "./data/tmp.csv"
    transform_to_csv(custom_data, csv_file_path)

    # 列表长度都为9
    imgLinks = []
    titles = []
    tags = []
    pubDates = []
    links = []

    if person == "用户1":
        result_ids = recommend_func("./data/user.csv", 1)
    elif person == "用户2":
        result_ids = recommend_func("./data/user.csv", 2)
    elif person == "用户3":
        result_ids = recommend_func("./data/user.csv", 3)
    elif person == "用户4":
        result_ids = recommend_func("./data/user.csv", 4)
    elif person == "用户5":
        result_ids = recommend_func("./data/user.csv", 5)
    else:
        result_ids = recommend_func(csv_file_path, user_id)
    # result_ids = [1,2,3,4,5,6,7,8,9]
    results = [get_article_by_id(id) for id in result_ids]

    imgLinks = [article["ImgLink"] for article in results]
    titles = [article["Title"] for article in results]
    tags = [article["Tag"] for article in results]
    pubDates = [article["PubDate"] for article in results]
    links = [article["Link"] for article in results]

    return process_output_recommend(imgLinks, titles, tags, pubDates, links)


def clear(inp1, inp2):
    return "", ""


def examples(person, description, articles):
    # 这里是针对人的description
    for i in range(len(articles)):
        articles[i] = articles[i][1:-1]
    return person, articles


with gr.Blocks() as recommend_interface:
    with gr.Row():
        with gr.Column(scale=2):
            gr.HTML(
                """
                <div style="height:78px;">
                    <div><h1 style="text-align:center">文章筛选</h1></div>
                    <br>
                    这是为您筛选后的文章
                    <br>
                </div>
            """
            )
            with gr.Row():
                with gr.Group():
                    oup_img1 = gr.Image(height=236, label="图片")
                    oup_content1 = gr.HTML(
                        """
                        <div style="height:98.6px;">
                            <div style="height:20px;"><span>tag</span>&nbsp;&nbsp;&nbsp;<span style="float:right;">日期</span></div>
                            <div style="width:100%;"><h3 style="display:block;text-align:center;">标题</h3></div>
                        </div>
                    """
                    )

                with gr.Group():
                    oup_img2 = gr.Image(height=236, label="图片")
                    oup_content2 = gr.HTML(
                        """
                        <div style="height:98.6px;">
                            <div style="height:20px;"><span>标签</span>&nbsp;&nbsp;&nbsp;<span style="float:right;">日期</span></div>
                            <div style="width:100%;"><h3 style="display:block;text-align:center;">标题</h3></div>
                        </div>
                    """
                    )

                with gr.Group():
                    oup_img3 = gr.Image(height=236, label="图片")
                    oup_content3 = gr.HTML(
                        """
                        <div style="height:98.6px;">
                            <div style="height:20px;"><span>标签</span>&nbsp;&nbsp;&nbsp;<span style="float:right;">日期</span></div>
                            <div style="width:100%;"><h3 style="display:block;text-align:center;">标题</h3></div>
                        </div>
                    """
                    )

            with gr.Row():
                with gr.Group():
                    oup_img4 = gr.Image(height=236, label="图片")
                    oup_content4 = gr.HTML(
                        """
                        <div style="height:98.6px;">
                            <div style="height:20px;"><span>标签</span>&nbsp;&nbsp;&nbsp;<span style="float:right;">日期</span></div>
                            <div style="width:100%;"><h3 style="display:block;text-align:center;">标题</h3></div>
                        </div>
                    """
                    )

                with gr.Group():
                    oup_img5 = gr.Image(height=236, label="图片")
                    oup_content5 = gr.HTML(
                        """
                        <div style="height:98.6px;">
                            <div style="height:20px;"><span>标签</span>&nbsp;&nbsp;&nbsp;<span style="float:right;">日期</span></div>
                            <div style="width:100%;"><h3 style="display:block;text-align:center;">标题</h3></div>
                        </div>
                    """
                    )

                with gr.Group():
                    oup_img6 = gr.Image(height=236, label="图片")
                    oup_content6 = gr.HTML(
                        """
                        <div style="height:98.6px;">
                            <div style="height:20px;"><span>标签</span>&nbsp;&nbsp;&nbsp;<span style="float:right;">日期</span></div>
                            <div style="width:100%;"><h3 style="display:block;text-align:center;">标题</h3></div>
                        </div>
                   """
                    )
            with gr.Row():
                with gr.Group():
                    oup_img7 = gr.Image(height=236, label="图片")
                    oup_content7 = gr.HTML(
                        """
                        <div style="height:98.6px;">
                            <div style="height:20px;"><span>标签</span>&nbsp;&nbsp;&nbsp;<span style="float:right;">日期</span></div>
                            <div style="width:100%;"><h3 style="display:block;text-align:center;">标题</h3></div>
                        </div>
                    """
                    )

                with gr.Group():
                    oup_img8 = gr.Image(height=236, label="图片")
                    oup_content8 = gr.HTML(
                        """
                        <div style="height:98.6px;">
                            <div style="height:20px;"><span>标签</span>&nbsp;&nbsp;&nbsp;<span style="float:right;">日期</span></div>
                            <div style="width:100%;"><h3 style="display:block;text-align:center;">标题</h3></div>
                        </div>
                    """
                    )

                with gr.Group():
                    oup_img9 = gr.Image(height=236, label="图片")
                    oup_content9 = gr.HTML(
                        """
                        <div style="height:98.6px;">
                            <div style="height:20px;"><span>标签</span>&nbsp;&nbsp;&nbsp;<span style="float:right;">日期</span></div>
                            <div style="width:100%;"><h3 style="display:block;text-align:center;">标题</h3></div>
                        </div>
                   """
                    )
        with gr.Column(scale=1):
            with gr.Group():
                gr.Image(value="./images/OIP-C.jpg", height=200, label="用户头像")
                inp1 = gr.Textbox(value="自定义用户", label="用户名")
            with gr.Group():
                inp2 = gr.Dropdown(
                    choices=Recommend_instance.choices_without_sign,
                    value=Recommend_instance.default_values,
                    label="已阅读文章",
                    # info="Please customize the articles you read",
                    info="请自定义您的已阅读文章",
                    multiselect=True,
                )
                inp2.select(
                    fn=change_username_while_change_articles, inputs=[], outputs=[inp1]
                )
            btn1 = gr.ClearButton([inp1, inp2], value="🧹 清除")
            btn2 = gr.Button(value="🚀 确定")
            btn2.click(
                fn=recommend,
                inputs=[inp1, inp2],
                outputs=[
                    oup_img1,
                    oup_content1,
                    oup_img2,
                    oup_content2,
                    oup_img3,
                    oup_content3,
                    oup_img4,
                    oup_content4,
                    oup_img5,
                    oup_content5,
                    oup_img6,
                    oup_content6,
                    oup_img7,
                    oup_content7,
                    oup_img8,
                    oup_content8,
                    oup_img9,
                    oup_content9,
                ],
            )
    # 这里是examples,为了丰富示例内容，通过一个函数，为输入绑定示例，设定选中示例自动执行，为下拉多选框赋值
    with gr.Row():
        inp_for_examples_hidden1 = gr.Textbox(visible=False)
        inp_for_examples_hidden2 = gr.Textbox(visible=False)
        inp_for_examples_hidden3 = gr.CheckboxGroup(
            choices=Recommend_instance.choices, visible=False
        )
        gr.Examples(
            label="用户示例",
            examples=Recommend_instance.examples,
            fn=examples,
            inputs=[
                inp_for_examples_hidden1,
                inp_for_examples_hidden2,
                inp_for_examples_hidden3,
            ],
            outputs=[inp1, inp2],
            cache_examples=False,  # 不能碰
            run_on_click=True,  # 不能碰
        )
