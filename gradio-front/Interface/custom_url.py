import gradio as gr
from Interface.util.get_info_based_url import get_info_based_url
from Interface.util.process_output_custom_url import process_output_custom_url
from Interface.util.static import CustomURL


def custom_url(url, site):
    link, title, publishDate, tag, imgLink, description = get_info_based_url(
        site=site, url=url
    )
    return process_output_custom_url(
        link, title, publishDate, tag, imgLink, description
    )


def examples(inp1, inp2):
    return inp2, inp1


with gr.Blocks() as custom_url_interface:
    with gr.Row():
        with gr.Column(scale=2):
            with gr.Row():
                oup1 = gr.HTML(
                    value="""
                        <div style="height:110px;">
                            <div style="text-align: center;">
                                <h1>标题</h1>
                            </div>
                            <br>
                            <p style="text-align: center;">
                                <span  style="display:inline-block;margin-right:100px;">日期</span>
                                <span>标签</span>
                            </p>
                        </div>
                    """
                )
            with gr.Row():
                oup2 = gr.Image(label="图片", width=300, height=310)
            with gr.Row():
                oup3 = gr.Chatbot(label="摘要", height=545)
        with gr.Column(scale=1):
            with gr.Group():
                gr.Image(value="./images/OIP-C.jpg", height=200, label="用户头像")
                gr.Textbox(value="自定义用户", label="用户名")

            inp1 = gr.Textbox(label="链接")
            inp2 = gr.Dropdown(
                choices=[
                    "懂球帝",
                    "知乎专栏",
                    "半月谈-文化篇",
                    "半月谈-生态篇",
                ],
                value="知乎专栏",
                label="网站",
            )
            # 输入为隐藏的实例
            inp_for_examples_hidden1 = gr.Textbox(visible=False)
            inp_for_examples_hidden2 = gr.Textbox(visible=False)

            # 加载examples的数据
            CustomURL.load_data()

            gr.Examples(
                CustomURL.examples,
                fn=examples,
                inputs=[inp_for_examples_hidden1, inp_for_examples_hidden2],
                outputs=[inp1, inp2],
                run_on_click=True,
                label="示例",
            )
            with gr.Row():
                btn1 = gr.ClearButton([inp1], value="🧹 清除")
                btn2 = gr.Button(value="🚀 确定")
            btn2.click(fn=custom_url, inputs=[inp1, inp2], outputs=[oup1, oup2, oup3])
