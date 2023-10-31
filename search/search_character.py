from googlesearch import search

# 设置搜索关键字
print("キャラの名前を入力してください")
query = (input()+"gamewith")

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
    # 提取你需要的内容，例如，这里提取所有段落文本
    content = "\n".join([p.text for p in soup.find_all('p')])
    
    # 将内容保存为文本文件
    with open('search_character.txt', 'w', encoding='utf-8') as textfile:
        textfile.write(content)

    print(f"Content saved to 'search_character.text'")
else:
    print(f"Failed to retrieve content from the URL. Status code: {response.status_code}")