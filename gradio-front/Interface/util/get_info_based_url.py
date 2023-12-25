from Interface.util.get_info_by_url_sites import (
    get_info_based_url_zhuhuzhuanlan,
    get_info_by_url_banyuetan_wenhua,
    get_info_by_url_banyuetan_shengtai,
    get_info_by_url_dongqiudi,
)

from Interface.func.custom_url import generate_summary_tag_func


def get_info_based_url(site, url):
    link = "https://www.zhihu.com/question/618895483"
    title = "Sample Title"
    publishDate = "2023-08-24"
    tag = "Technology"
    imgLink = "https://pic1.zhimg.com/v2-d9fee183f9196303fa5d8b96a2c023e6_r.jpg?source=1940ef5c"
    description = '据央视新闻客户端24日报道，<em style="background-color:green;">当地</em>时间8月24日13时，日本福岛第一核电站启动核污染水排海。东京电力公司24日在临时记者会上宣布，今天的核污染水排放量预计为200到210吨，每天的排放情况将在次日公布。首次排海每天将排放约460吨，持续17天，合计排放约7800立方米核污染水。据日本共同社，福岛第一核电站的核污染水约有134万吨，2023年度将把约3.12万吨核污染水分4次排放，每次约排放7800吨。根据东电计算，用海水稀释过的核污染水将缓慢流过约1公里的隧道，约1000秒之后抵达大海。根据计划，排海时间至少持续30年。中国生态环境部核与辐射安全中心首席专家刘新华表示：由于福岛第一核电站退役需要数十年，这个过程中还会持续产生大量核污染水，排放时间可能远超30年，核污染水排海将会对海洋生态产生长期影响。'

    if site == "知乎专栏":
        (
            link,
            title,
            publishDate,
            tag,
            imgLink,
            description,
        ) = get_info_based_url_zhuhuzhuanlan(url=url)

    if site == "半月谈-文化篇":
        (
            link,
            title,
            publishDate,
            tag,
            imgLink,
            description,
        ) = get_info_by_url_banyuetan_wenhua(url=url)

    if site == "半月谈-生态篇":
        (
            link,
            title,
            publishDate,
            tag,
            imgLink,
            description,
        ) = get_info_by_url_banyuetan_shengtai(url=url)

    if site == "懂球帝":
        (
            link,
            title,
            publishDate,
            tag,
            imgLink,
            description,
        ) = get_info_by_url_dongqiudi(url=url)
    link, title, publishDate, tag, imgLink, description = generate_summary_tag_func(
        link, title, publishDate, tag, imgLink, description
    )
    return link, title, publishDate, tag, imgLink, description
