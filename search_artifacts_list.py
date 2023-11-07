from googlesearch import search

# 设置搜索关键字
query = "聖遺物一覧gamewith"

# 使用Google搜索库执行搜索
search_results = list(search(query, num=1, stop=1, pause=2))

# 获取第一个搜索结果的URL
first_result_url = search_results[0]

# 从URL中提取内容
import requests
from bs4 import BeautifulSoup

response = requests.get(first_result_url)
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    # 提取<div class="genshin saka">中的文本内容
    genshin_saka_div = soup.find('div', class_='genshin_saka')
    if genshin_saka_div:
        content = ""
        td_elements = genshin_saka_div.find_all('td')
        for td in td_elements:
            # 查找所有的<a>元素
            a_elements = td.find_all('a')

            for a in a_elements:
                # 获取<a>元素中的文本内容
                text = a.get_text()
                content += text + " "

        # 去掉首尾的空白
        content = content.strip()
    else:
        content = "未找到指定的<div>元素"

    # 将内容保存为文本文件
    with open('search_artifacts_list.txt', 'w', encoding='utf-8') as textfile:
        textfile.write(content)

    print(f"Content saved to 'search_artifacts_list.text'")
else:
    print(f"Failed to retrieve content from the URL. Status code: {response.status_code}")