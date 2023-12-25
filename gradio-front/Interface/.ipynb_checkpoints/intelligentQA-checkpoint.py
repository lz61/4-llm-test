import gradio as gr

from Interface.func.intelligent_qa import intelligent_qa_func
from Interface.util.process_output_intelligentQA import process_output_intelligentQA
from Interface.util.static import QA_instance
from Interface.util.util import get_articleId_by_title


def change_username_while_change_articles():
    return "自定义用户"

def intelligent_qa(person, articles, query, history=None):
    if history is None:
        history = []

    article_ids = []
    for article in articles:
        article_id = get_articleId_by_title(article)
        if article_id is not None:
            article_ids.append(article_id)

    # chat_returned_message = "re"
    chat_returned_message = intelligent_qa_func(article_ids, query)
    history.append((query, chat_returned_message))
    return process_output_intelligentQA("", history)


def examples(person, description, articles):
    # 这里是针对人的description
    for i in range(len(articles)):
        articles[i] = articles[i][1:-1]
    return person, articles


with gr.Blocks() as QA_interface:
    with gr.Row():
        with gr.Column(scale=2):
            gr.HTML(
                """
                <div style="height:110px;">
                    <div><h1 style="text-align:center">智能QA</h1></div>
                    <br>
                    <br>
                    您的智能问答助手
                    <br>
                </div>
            """
            )
            chatbot = gr.Chatbot(label="问答助手", height=500)
            msg = gr.Textbox(lines=12, label="输入")
            with gr.Row():
                btn1 = gr.ClearButton([msg, chatbot], value="🧹 清除")
                btn2 = gr.Button(value="🚀 确定")

        with gr.Column(scale=1):
            with gr.Group():
                gr.Image(value="./images/OIP-C.jpg", height=200, label="用户头像")
                inp1 = gr.Textbox(value="自定义用户", label="用户名")
            with gr.Group():
                inp2 = gr.Dropdown(
                    choices=QA_instance.choices_without_sign,
                    value=QA_instance.default_values,
                    label="已订阅文章",
                    # info="Please customize the articles you read",
                    info="请自定义您的已订阅文章",
                    multiselect=True,
                )
                inp2.select(
                    fn=change_username_while_change_articles, inputs=[], outputs=[inp1]
                )
        btn2.click(
            fn=intelligent_qa, inputs=[inp1, inp2, msg, chatbot], outputs=[msg, chatbot]
        )
    # 这里是examples,为了丰富示例内容，通过一个函数，为输入绑定示例，设定选中示例自动执行，为下拉多选框赋值
    with gr.Row():
        inp_for_examples_hidden1 = gr.Textbox(visible=False)
        inp_for_examples_hidden2 = gr.Textbox(visible=False)
        inp_for_examples_hidden3 = gr.CheckboxGroup(
            choices=QA_instance.choices, visible=False
        )
        gr.Examples(
            label="用户示例",
            examples=QA_instance.examples,
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
