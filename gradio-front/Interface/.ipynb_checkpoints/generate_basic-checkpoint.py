import gradio as gr

from Interface.func.generate_basic import generate_basic_func
from Interface.util.process_output_generate_basic import process_output_generate_basic
from Interface.util.static import detail_instance
from Interface.util.util import get_articleId_by_title


def generate_basic(article, language="Chinese"):
    link = "https://www.zhihu.com/question/618895483"
    title = "Sample Title"
    publishDate = "2023-08-24"
    tag = "Technology"
    imgLink = "https://pic1.zhimg.com/v2-d9fee183f9196303fa5d8b96a2c023e6_r.jpg?source=1940ef5c"
    description = '据央视新闻客户端24日报道，<em style="background-color:green;">当地</em>时间8月24日13时，日本福岛第一核电站启动核污染水排海。东京电力公司24日在临时记者会上宣布，今天的核污染水排放量预计为200到210吨，每天的排放情况将在次日公布。首次排海每天将排放约460吨，持续17天，合计排放约7800立方米核污染水。据日本共同社，福岛第一核电站的核污染水约有134万吨，2023年度将把约3.12万吨核污染水分4次排放，每次约排放7800吨。根据东电计算，用海水稀释过的核污染水将缓慢流过约1公里的隧道，约1000秒之后抵达大海。根据计划，排海时间至少持续30年。中国生态环境部核与辐射安全中心首席专家刘新华表示：由于福岛第一核电站退役需要数十年，这个过程中还会持续产生大量核污染水，排放时间可能远超30年，核污染水排海将会对海洋生态产生长期影响。'

    articleId = get_articleId_by_title(article)
    if articleId is not None:
        link, title, publishDate, tag, imgLink, description = generate_basic_func(
            articleId, language, True
        )

    return process_output_generate_basic(
        link, title, publishDate, tag, imgLink, description
    )


def clear(inp1, inp2):
    return "", "中文"


def examples(inp1, inp2, inp3):
    return inp2, inp3


with gr.Blocks() as detail_interface:
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
            inp1 = gr.Textbox(
                placeholder="请输入对应的文章", label="文章", value="恐龙灭绝后，这里记录下完整的地球故事"
            )
            inp2 = gr.Dropdown(["中文", "English"], label="语言选择", value="中文")
            # 输入为隐藏的实例
            inp_for_examples_hidden1 = gr.Textbox(visible=False)
            inp_for_examples_hidden2 = gr.Textbox(visible=False)
            inp_for_examples_hidden3 = gr.Textbox(visible=False)
            gr.Examples(
                label="已订阅文章",
                examples=detail_instance.examples,
                inputs=[
                    inp_for_examples_hidden1,
                    inp_for_examples_hidden2,
                    inp_for_examples_hidden3,
                ],
                outputs=[inp1, inp2],
                fn=examples,
                run_on_click=True,
            )
            with gr.Row():
                btn1 = gr.ClearButton(value="🧹 清除")
                btn1.click(clear, inputs=[inp1, inp2], outputs=[inp1, inp2])
                btn2 = gr.Button(value="🚀 确定")
                btn2.click(
                    generate_basic, inputs=[inp1, inp2], outputs=[oup1, oup2, oup3]
                )
