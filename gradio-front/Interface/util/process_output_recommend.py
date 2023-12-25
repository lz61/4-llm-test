def process_output_recommend(imgLinks,titles,tags,pubDates,links):
    # oup_img1 = 'https://pic1.zhimg.com/v2-d9fee183f9196303fa5d8b96a2c023e6_r.jpg?source=1940ef5c'
    # oup_img2 = 'https://pic1.zhimg.com/v2-d9fee183f9196303fa5d8b96a2c023e6_r.jpg?source=1940ef5c'
    # oup_img3 = 'https://pic1.zhimg.com/v2-d9fee183f9196303fa5d8b96a2c023e6_r.jpg?source=1940ef5c'
    # oup_img4 = 'https://pic1.zhimg.com/v2-d9fee183f9196303fa5d8b96a2c023e6_r.jpg?source=1940ef5c'
    # oup_img5 = 'https://pic1.zhimg.com/v2-d9fee183f9196303fa5d8b96a2c023e6_r.jpg?source=1940ef5c'
    # oup_img6 = 'https://pic1.zhimg.com/v2-d9fee183f9196303fa5d8b96a2c023e6_r.jpg?source=1940ef5c'
    # oup_img7 = 'https://pic1.zhimg.com/v2-d9fee183f9196303fa5d8b96a2c023e6_r.jpg?source=1940ef5c'
    # oup_img8 = 'https://pic1.zhimg.com/v2-d9fee183f9196303fa5d8b96a2c023e6_r.jpg?source=1940ef5c'
    # oup_img9 = 'https://pic1.zhimg.com/v2-d9fee183f9196303fa5d8b96a2c023e6_r.jpg?source=1940ef5c'
    # oup_title1 = "Sample title 1"
    # oup_title2 = "Sample title 2"
    # oup_title3 = "Sample title 3"
    # oup_title4 = "Sample title 4"
    # oup_title5 = "Sample title 5"
    # oup_title6 = "Sample title 6"
    # oup_title7 = "Sample title 7"
    # oup_title8 = "Sample title 8"
    # oup_title9 = "Sample title 9"
    # oup_tag1 = "tag1"
    # oup_tag2 = "tag2"
    # oup_tag3 = "tag3"
    # oup_tag4 = "tag4"
    # oup_tag5 = "tag5"
    # oup_tag6 = "tag6"
    # oup_tag7 = "tag7"
    # oup_tag8 = "tag8"
    # oup_tag9 = "tag9"
    # oup_pubDate1 = "pubDate1"
    # oup_pubDate2 = "pubDate2"
    # oup_pubDate3 = "pubDate3"
    # oup_pubDate4 = "pubDate4"
    # oup_pubDate5 = "pubDate5"
    # oup_pubDate6 = "pubDate6"
    # oup_pubDate7 = "pubDate7"
    # oup_pubDate8 = "pubDate8"
    # oup_pubDate9 = "pubDate9"
    # oup_link1 = "https://www.zhihu.com/question/618895483"
    # oup_link2 = "https://www.zhihu.com/question/618895483"
    # oup_link3 = "https://www.zhihu.com/question/618895483"
    # oup_link4 = "https://www.zhihu.com/question/618895483"
    # oup_link5 = "https://www.zhihu.com/question/618895483"
    # oup_link6 = "https://www.zhihu.com/question/618895483"
    # oup_link7 = "https://www.zhihu.com/question/618895483"
    # oup_link8 = "https://www.zhihu.com/question/618895483"
    # oup_link9 = "https://www.zhihu.com/question/618895483"
    
    # oup_content1 = f"""
    #     <div style="height:98.6px;">
    #         <div style="height:20px;"><span>{oup_tag1}</span>&nbsp;&nbsp;&nbsp;<span style="float:right;">{oup_pubDate1}</span></div>
    #         <div style="width:100%;"><a href="{oup_link1}"><h3 style="display:block;text-align:center;">{oup_title1}</h3></a></div>
    #     </div>
    # """
    # oup_content2 = f"""
    #     <div style="height:98.6px;">
    #         <div style="height:20px;"><span>{oup_tag2}</span>&nbsp;&nbsp;&nbsp;<span style="float:right;">{oup_pubDate2}</span></div>
    #         <div style="width:100%;"><a href="{oup_link2}"><h3 style="display:block;text-align:center;">{oup_title2}</h3></a></div>
    #     </div>
    # """
    # oup_content3 = f"""
    #     <div style="height:98.6px;">
    #         <div style="height:20px;"><span>{oup_tag3}</span>&nbsp;&nbsp;&nbsp;<span style="float:right;">{oup_pubDate3}</span></div>
    #         <div style="width:100%;"><a href="{oup_link3}"><h3 style="display:block;text-align:center;">{oup_title3}</h3></a></div>
    #     </div>
    # """
    # oup_content4 = f"""
    #     <div style="height:98.6px;">
    #         <div style="height:20px;"><span>{oup_tag4}</span>&nbsp;&nbsp;&nbsp;<span style="float:right;">{oup_pubDate4}</span></div>
    #         <div style="width:100%;"><a href="{oup_link4}"><h3 style="display:block;text-align:center;">{oup_title4}</h3></a></div>
    #     </div>
    # """
    # oup_content5 = f"""
    #     <div style="height:98.6px;">
    #         <div style="height:20px;"><span>{oup_tag5}</span>&nbsp;&nbsp;&nbsp;<span style="float:right;">{oup_pubDate5}</span></div>
    #         <div style="width:100%;"><a href="{oup_link5}"><h3 style="display:block;text-align:center;">{oup_title5}</h3></a></div>
    #     </div>
    # """
    # oup_content6 = f"""
    #     <div style="height:98.6px;">
    #         <div style="height:20px;"><span>{oup_tag6}</span>&nbsp;&nbsp;&nbsp;<span style="float:right;">{oup_pubDate6}</span></div>
    #         <div style="width:100%;"><a href="{oup_link6}"><h3 style="display:block;text-align:center;">{oup_title6}</h3></a></div>
    #     </div>
    # """
    # oup_content7 = f"""
    #     <div style="height:98.6px;">
    #         <div style="height:20px;"><span>{oup_tag7}</span>&nbsp;&nbsp;&nbsp;<span style="float:right;">{oup_pubDate7}</span></div>
    #         <div style="width:100%;"><a href="{oup_link7}"><h3 style="display:block;text-align:center;">{oup_title7}</h3></a></div>
    #     </div>
    # """
    # oup_content8 = f"""
    #     <div style="height:98.6px;">
    #         <div style="height:20px;"><span>{oup_tag8}</span>&nbsp;&nbsp;&nbsp;<span style="float:right;">{oup_pubDate8}</span></div>
    #         <div style="width:100%;"><a href="{oup_link8}"><h3 style="display:block;text-align:center;">{oup_title8}</h3></a></div>
    #     </div>
    # """
    # oup_content9 = f"""
    #     <div style="height:98.6px;">
    #         <div style="height:20px;"><span>{oup_tag9}</span>&nbsp;&nbsp;&nbsp;<span style="float:right;">{oup_pubDate9}</span></div>
    #         <div style="width:100%;"><a href="{oup_link9}"><h3 style="display:block;text-align:center;">{oup_title9}</h3></a></div>
    #     </div>
    # """

    oup_img0 = imgLinks[0]
    oup_img1 = imgLinks[1]
    oup_img2 = imgLinks[2]
    oup_img3 = imgLinks[3]
    oup_img4 = imgLinks[4]
    oup_img5 = imgLinks[5]
    oup_img6 = imgLinks[6]
    oup_img7 = imgLinks[7]
    oup_img8 = imgLinks[8]
    
    oup_content0 = f"""
        <div style="height:98.6px;">
            <div style="height:20px;"><span>{tags[0]}</span>&nbsp;&nbsp;&nbsp;<span style="float:right;">{pubDates[0]}</span></div>
            <div style="width:100%;"><a href="{links[0]}"><h3 style="display:block;text-align:center;">{titles[0]}</h3></a></div>
        </div>
    """
    oup_content1 = f"""
        <div style="height:98.6px;">
            <div style="height:20px;"><span>{tags[1]}</span>&nbsp;&nbsp;&nbsp;<span style="float:right;">{pubDates[1]}</span></div>
            <div style="width:100%;"><a href="{links[1]}"><h3 style="display:block;text-align:center;">{titles[1]}</h3></a></div>
        </div>
    """
    oup_content2 = f"""
        <div style="height:98.6px;">
            <div style="height:20px;"><span>{tags[2]}</span>&nbsp;&nbsp;&nbsp;<span style="float:right;">{pubDates[2]}</span></div>
            <div style="width:100%;"><a href="{links[2]}"><h3 style="display:block;text-align:center;">{titles[2]}</h3></a></div>
        </div>
    """
    oup_content3 = f"""
        <div style="height:98.6px;">
            <div style="height:20px;"><span>{tags[3]}</span>&nbsp;&nbsp;&nbsp;<span style="float:right;">{pubDates[3]}</span></div>
            <div style="width:100%;"><a href="{links[3]}"><h3 style="display:block;text-align:center;">{titles[3]}</h3></a></div>
        </div>
    """
    oup_content4 = f"""
        <div style="height:98.6px;">
            <div style="height:20px;"><span>{tags[4]}</span>&nbsp;&nbsp;&nbsp;<span style="float:right;">{pubDates[4]}</span></div>
            <div style="width:100%;"><a href="{links[4]}"><h3 style="display:block;text-align:center;">{titles[4]}</h3></a></div>
        </div>
    """
    oup_content5 = f"""
        <div style="height:98.6px;">
            <div style="height:20px;"><span>{tags[5]}</span>&nbsp;&nbsp;&nbsp;<span style="float:right;">{pubDates[5]}</span></div>
            <div style="width:100%;"><a href="{links[5]}"><h3 style="display:block;text-align:center;">{titles[5]}</h3></a></div>
        </div>
    """
    oup_content6 = f"""
        <div style="height:98.6px;">
            <div style="height:20px;"><span>{tags[6]}</span>&nbsp;&nbsp;&nbsp;<span style="float:right;">{pubDates[6]}</span></div>
            <div style="width:100%;"><a href="{links[6]}"><h3 style="display:block;text-align:center;">{titles[6]}</h3></a></div>
        </div>
    """
    oup_content7 = f"""
        <div style="height:98.6px;">
            <div style="height:20px;"><span>{tags[7]}</span>&nbsp;&nbsp;&nbsp;<span style="float:right;">{pubDates[7]}</span></div>
            <div style="width:100%;"><a href="{links[7]}"><h3 style="display:block;text-align:center;">{titles[7]}</h3></a></div>
        </div>
    """
    oup_content8 = f"""
        <div style="height:98.6px;">
            <div style="height:20px;"><span>{tags[8]}</span>&nbsp;&nbsp;&nbsp;<span style="float:right;">{pubDates[8]}</span></div>
            <div style="width:100%;"><a href="{links[8]}"><h3 style="display:block;text-align:center;">{titles[8]}</h3></a></div>
        </div>
    """
    

    return oup_img0,oup_content0,oup_img1,oup_content1,oup_img2,oup_content2,oup_img3,oup_content3,oup_img4,oup_content4,oup_img5,oup_content5,oup_img6,oup_content6,oup_img7,oup_content7,oup_img8,oup_content8