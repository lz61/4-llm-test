def process_output_generate_basic(link,title,publishDate,tag,imgLink,description):
    if link is None or title is None or link == "" or title == "":
        link = ""
        title = "Not Found"
        publishDate = " "
        tag = " "
        imgLink = "./images/No-Image.jpg"
        description = "抱歉，该文章已经不存在"
    if publishDate == "":
        publishDate = " "
    if tag == "":
        tag = " "
    if imgLink == "":
        imgLink = "./images/No-Image.jpg"
    if description == "":
        description = "该文章没有文本内容"

    description_tuple = ("",description)
    description_chat = [description_tuple]
    head_content_html = f"""
        <div style="height:110px;">
            <div style="text-align: center;">
                <a href="{link}"><h1>{title}</h1></a>
            </div>
            <br>
            <p style="text-align: center;">
                <span  style="display:inline-block;margin-right:100px;">{publishDate}</span>
                <span>{tag}</span>
            </p>
        </div>
    """
    return head_content_html, imgLink, description_chat

