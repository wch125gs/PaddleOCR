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

    # 查找带有特定class属性的<div>元素
    genshin_saka_div = soup.find('div', class_='article-wrap')

    # 检查是否找到了目标<div>元素
    if genshin_saka_div:
        content = ""
        #separator = "\n"  # 分隔线

        # 查找所有的<table>元素
        table_elements = genshin_saka_div.find_all('table')

        for table in table_elements:
            td_elements1 = table.find_all('td', attrs={"align": "center"})
            for td in td_elements1:
                a_elements = td.find_all('a')
                for a in a_elements:
                    text = a.get_text()
                    content += text + "\n"
               # content += separator
            

        # 去掉首尾的空白和多余的分隔线
        content = content.strip()
        #if content.endswith(separator):
            #content = content[:-len(separator)]

        # 将内容保存为文本文件
        with open('match2.txt', 'w', encoding='utf-8') as textfile:
            textfile.write(content)

        print(f"内容已保存到 'match2.txt'")
    else:
        content = "未找到指定的<div>元素"
else:
    print(f"未能从URL中检索内容。状态码：{response.status_code}")






