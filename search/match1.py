from googlesearch import search
import requests
from bs4 import BeautifulSoup

# 设置搜索关键字
query = "おすすめ聖遺物gamewith"

# 使用Google搜索库执行搜索
search_results = list(search(query, num=1, stop=1, pause=2))

# 获取第一个搜索结果的URL
first_result_url = search_results[0]

response = requests.get(first_result_url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    # 查找带有特定id的<div>元素
    genshin_saka_div = soup.find('div', class_='article-wrap')
   # 检查是否找到了目标<div>元素
    if genshin_saka_div:
        content = ""
        td_elements = genshin_saka_div.find_all('td')
        for td in td_elements:
            # 查找所有的<a>元素
            a_elements = td.find_all('a')

            for a in a_elements:
                # 获取<a>元素中的文本内容
                text = a.get_text()
                content += text + "\n"

        # 去掉首尾的空白
        content = content.strip()
    else:
        content = "未找到指定的<div>元素"
                


    # 将内容保存为文本文件
    with open('match1.txt', 'w', encoding='utf-8') as textfile:
        textfile.write(content)

    print(f"内容已保存到 'match1.text'")
else:
    print(f"未能从URL中检索内容。状态码：{response.status_code}")