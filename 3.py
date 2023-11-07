import streamlit as st
from PIL import Image
from paddleocr import PaddleOCR, draw_ocr
import os
import difflib
import Levenshtein
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



# 定义语言对应的文本
language_texts = {
    'ch': {
        'title': "图像识别Web应用",
        'upload_prompt': "上传多张图片...",
        'results_header': "识别结果:",
        'visualization_caption': "可视化",
        'language': "语言选择",
        'image': '示例图像'
    },
    'en': {
        'title': "Image Recognition Web App",
        'upload_prompt': "Upload multiple images...",
        'results_header': "Recognition results:",
        'visualization_caption': "Visualization",
        'language': "Select Language",
        'image': 'Sample Image'
    },
    'japan': {
        'title': "画像認識ウェブアプリ",
        'upload_prompt': "複数の画像をアップロード...",
        'results_header': "認識結果:",
        'visualization_caption': "可視化",
        'language': "言語選択",
        'image': 'サンプル画像'
    },
    # 添加其他语言的文本
}

# 添加语言选择下拉菜单
languages = list(language_texts.keys())
selected_lang = st.selectbox("Select Language", languages)

st.title(language_texts[selected_lang]['title'])
# 显示示例图像
st.image("1.png", caption=language_texts[selected_lang]['image'], use_column_width=True)


# 添加文件上传小部件
uploaded_files = st.file_uploader(language_texts[selected_lang]['upload_prompt'],
                                  type=["jpg", "png", "jpeg"], accept_multiple_files=True)

# 设置相似度阈值
similarity_threshold = 0.7  # 根据需求调整相似度阈值


# 初始化 OCR 对象
ocr = PaddleOCR(use_angle_cls=True, lang=selected_lang)

if uploaded_files:
    for uploaded_file in uploaded_files:
        st.subheader(f"Processing {uploaded_file.name}")

        # 将上传的图像保存到临时文件
        with open("temp_image.jpg", "wb") as f:
            f.write(uploaded_file.read())

        # 进行文本识别
        result = ocr.ocr("temp_image.jpg", cls=True)
        
    
        #打印识别结果

        
        #for idx, res in enumerate(result):
            #st.write(f"内容:")
            #for line in res:
                #st.write(line[1][0])

        # 从文件 "1.text" 中读取内容
        if os.path.isfile("search_artifacts_list.txt"):
            with open("search_artifacts_list.txt", "r",encoding="utf-8") as file:
                target_texts = [line.strip() for line in file.read().strip().split()]
                # 在识别结果中查找相同的词语
                for target_text in target_texts:
                    for idx, res in enumerate(result):
                        for line in res:
                            similarity = Levenshtein.ratio(target_text, line[1][0])
                            if similarity >= similarity_threshold:
                                st.write(f"認識した聖遺物の名前は： '{line[1][0]}' ,既存の聖遺物の名前は:{target_text}, 相似度: {similarity:.2f}")
                                 # 设置搜索关键字
                                query = target_text+"gamewith"

                                # 使用Google搜索库执行搜索
                                search_results = list(search(query, num=1, stop=1, pause=2))

                                # 获取第一个搜索结果的URL
                                first_result_url = search_results[0]

                                response = requests.get(first_result_url)

                                if response.status_code == 200:
                                    soup = BeautifulSoup(response.text, 'html.parser')

                                    # 查找带有特定class属性的<div>元素
                                    genshin_saka_div = soup.find('div', class_='genshin_osusume')

                                    # 检查是否找到了目标<div>元素
                                    if genshin_saka_div:
                                        content = ""
                                        td_elements = genshin_saka_div.find_all('td')
                                        for i, td in enumerate(td_elements):
                                            # 查找所有的<a>元素
                                            a_elements = td.find_all('a')

                                            for a in a_elements:
                                                # 获取<a>元素中的文本内容
                                                text = a.get_text()
                                                content += text 
                                            if (i +1) % 2 == 0:
                                                content += "\n---------------------\n"

                                        # 去掉首尾的空白
                                        content = content.strip()

                                        st.write(f"{content}")
                                    else:
                                        content = "未找到指定的<div>元素"
                                else:
                                    st.write(f"未能从URL中检索内容。状态码：{response.status_code}")

                                break


        else:
            st.write("File 'search_artifacts_list.txt' not found")
        

       
        
        # 可视化
        result = result[0]
        image = Image.open("temp_image.jpg").convert('RGB')
        boxes = [line[0] for line in result]
        txts = [line[1][0] for line in result]
        scores = [line[1][1] for line in result]
        im_show = draw_ocr(image, boxes, txts, scores, font_path='/path/to/PaddleOCR/doc/simfang.ttf')
        im_show = Image.fromarray(im_show)

        st.image(im_show, caption=language_texts[selected_lang]['visualization_caption'], use_column_width=True)

        # 删除临时文件
        os.remove("temp_image.jpg")