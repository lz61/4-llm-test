import os

os.system("pip install -r requirements.txt")
import gradio as gr
from Interface.intelligentQA import QA_interface
from Interface.recommend import recommend_interface
from Interface.generate_basic import detail_interface
from Interface.custom_url import custom_url_interface


demo = gr.TabbedInterface(
    [detail_interface, custom_url_interface, QA_interface, recommend_interface],
    ["文章详情", "自定义url", "智能QA", "智能筛选"],
)

if __name__ == "__main__":
    demo.launch()
