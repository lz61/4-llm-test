import re
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime


def get_info_based_url_zhuhuzhuanlan(url):
    # 查看url形式
    pattern = r"https://zhuanlan.zhihu.com/p/(\d+)"
    get_successfully = False
    match = re.match(pattern, url)
    if match:
        id = match[1]
        res = requests.get(url=url)
        if res.status_code == 200:
            get_successfully = True
            text = res.text

            content_html_bs = BeautifulSoup(text, "html.parser")
            data = content_html_bs.find(
                "script", attrs={"id": "js-initialData"}
            ).get_text()
            json_dict = json.loads(data)

            article = json_dict["initialState"]["entities"]["articles"][id]["content"]

            ps = BeautifulSoup(article, "html.parser")
            ps = ps.find_all("p")
            description = ""
            for p in ps:
                description += p.get_text()
            link = json_dict["initialState"]["entities"]["articles"][id]["url"]
            title = json_dict["initialState"]["entities"]["articles"][id]["title"]
            publishDate = str(
                datetime.fromtimestamp(
                    json_dict["initialState"]["entities"]["articles"][id]["updated"]
                )
            )
            tag = "tag"
            imgLink = json_dict["initialState"]["entities"]["articles"][id][
                "titleImage"
            ]

    if (not get_successfully) or link is None or title is None:
        link = url
        title = " "
        publishDate = " "
        tag = " "
        imgLink = "./images/No-Image.jpg"
        description = "url形式有误"
    if publishDate is None:
        publishDate = ""
    if tag is None:
        tag = ""
    if imgLink is None:
        imgLink = ""
    if description is None:
        description = ""

    # print(link)
    # print(title)
    # print(publishDate)
    # print(tag)
    # print(imgLink)
    # print(description)

    return link, title, publishDate, tag, imgLink, description


def get_info_by_url_banyuetan_wenhua(url):
    # 查看url形式
    pattern = r"http://www.banyuetan.org/wh/detail/(\d+)/(\d+)_(\d{1}).html"
    get_successfully = False
    match = re.match(pattern, url)
    link = None
    title = None
    publishDate = None
    tag = None
    imgLink = None
    description = None
    if match:
        res = requests.get(url=url)
        if res.status_code == 200:
            get_successfully = True
            text = res.text

            content_html_bs = BeautifulSoup(text, "html.parser")
            detail_title = content_html_bs.find("div", attrs={"class": "detail_tit"})

            link = url
            title = ""
            publishDate = ""
            tag = "文化"
            imgLink = ""
            description = ""

            title_h1 = detail_title.find("h1")
            if title_h1 is not None:
                title = title_h1.get_text()
            pubDate_div = detail_title.find("div", attrs={"class": "detail_tit_time"})
            if pubDate_div is not None:
                publishDate = pubDate_div.get_text()

            detail_content = content_html_bs.find(
                "div", attrs={"class": "detail_content"}
            )
            img_p = detail_content.find("p", attrs={"class": "p_image"})
            if img_p is not None:
                imgLink = img_p.find("img").get("src")
            ps = detail_content.find_all("p")
            for p in ps:
                description += p.get_text()

    if (not get_successfully) or link is None or title is None:
        link = url
        title = " "
        publishDate = " "
        tag = " "
        imgLink = "./images/No-Image.jpg"
        description = "url形式有误"
    if publishDate is None:
        publishDate = ""
    if tag is None:
        tag = ""
    if imgLink is None:
        imgLink = ""
    if description is None:
        description = ""

    return link, title, publishDate, tag, imgLink, description


def get_info_by_url_banyuetan_shengtai(url):
    # 查看url形式
    pattern = r"http://www.banyuetan.org/st/detail/(\d+)/(\d+)_(\d{1}).html"
    get_successfully = False
    match = re.match(pattern, url)
    link = None
    title = None
    publishDate = None
    tag = None
    imgLink = None
    description = None
    if match:
        res = requests.get(url=url)
        if res.status_code == 200:
            get_successfully = True
            text = res.text

            content_html_bs = BeautifulSoup(text, "html.parser")
            detail_title = content_html_bs.find("div", attrs={"class": "detail_tit"})

            link = url
            title = ""
            publishDate = ""
            tag = "文化"
            imgLink = ""
            description = ""

            title_h1 = detail_title.find("h1")
            if title_h1 is not None:
                title = title_h1.get_text()
            pubDate_div = detail_title.find("div", attrs={"class": "detail_tit_time"})
            if pubDate_div is not None:
                publishDate = pubDate_div.get_text()

            detail_content = content_html_bs.find(
                "div", attrs={"class": "detail_content"}
            )
            img_p = detail_content.find("p", attrs={"class": "p_image"})
            if img_p is not None:
                imgLink = img_p.find("img").get("src")
            ps = detail_content.find_all("p")
            for p in ps:
                description += p.get_text()

    if (not get_successfully) or link is None or title is None:
        link = url
        title = " "
        publishDate = " "
        tag = " "
        imgLink = "./images/No-Image.jpg"
        description = "url形式有误"
    if publishDate is None:
        publishDate = ""
    if tag is None:
        tag = ""
    if imgLink is None:
        imgLink = ""
    if description is None:
        description = ""

    return link, title, publishDate, tag, imgLink, description


def get_info_by_url_dongqiudi(url):
    # 查看url形式
    pattern = r"https://www.dongqiudi.com/articles/(\d+).html"
    get_successfully = False
    match = re.match(pattern, url)
    link = None
    title = None
    publishDate = None
    tag = None
    imgLink = None
    description = None
    if match:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.62"
        }
        res = requests.get(url=url, headers=headers)
        if res.status_code == 200:
            get_successfully = True

            text = res.text
            content_html_bs = BeautifulSoup(text, "html.parser")

            title_h1 = content_html_bs.find("h1", attrs={"class": "news-title"})
            if title_h1 is not None:
                title = title_h1.get_text()

            p_tag = content_html_bs.find("p", class_="tips")
            if p_tag:
                publishDate = p_tag.get_text().strip()[-16:-1]

            content = content_html_bs.find("div", attrs={"class": "con"})
            img = content.find("img")
            if img is not None:
                imgLink = img.get("data-src")

            description = ""
            ps = content.find_all("p")
            for p in ps:
                description += p.get_text()

            tag = "体育"
            link = url
    if (not get_successfully) or link is None or title is None:
        link = url
        title = " "
        publishDate = " "
        tag = " "
        imgLink = "./images/No-Image.jpg"
        description = "url形式有误"
    if publishDate is None:
        publishDate = ""
    if tag is None:
        tag = ""
    if imgLink is None:
        imgLink = ""
    if description is None:
        description = ""

    return link, title, publishDate, tag, imgLink, description
