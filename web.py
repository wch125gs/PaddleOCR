import streamlit as st
from PIL import Image
from paddleocr import PaddleOCR, draw_ocr
import os
import difflib
import Levenshtein
from googlesearch import search
import re
import requests
from bs4 import BeautifulSoup



# 设置搜索关键字
query = "聖遺物一覧gamewith"

# 使用Google搜索库执行搜索
search_results = list(search(query, num=1, stop=1, pause=2))

# 获取第一个搜索结果的URL
first_result_url = search_results[0]

# 从URL中提取内容
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
        'title': "光学字符识别Web应用",
        'upload_prompt': "上传图片...",
        'results_header': "识别结果:",
        'visualization_caption': "可视化",
        'language': "语言选择",
        'image': '示例图像'
    },
    'en': {
        'title': "Optical Character Recognition Web Application",
        'upload_prompt': "Upload the image...",
        'results_header': "Recognition results:",
        'visualization_caption': "Visualization",
        'language': "Select Language",
        'image': 'Sample Image'
    },
    'japan': {
        'title': "光学文字認識ウェブアプリケーション",
        'upload_prompt': "画像をアップロード...",
        'results_header': "認識結果:",
        'visualization_caption': "可視化",
        'language': "言語選択",
        'image': 'サンプル画像'
    },
    # 添加其他语言的文本
}
# 定义圣遗物部位
artifacts = {"理の冠","空の杯","時の砂","生の花","死の羽"}

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

        # Initialize lists to store classified lines
        部位_list = []
        メイン属性_list = []
        サーブ属性_list = []
        max_lines = 5
        line_count = 0
        
        # Initialize variables to track the current context
        current_context = None
        
        # Keywords to check for the start of a new context
        keywords = ["空の杯", "理の冠", "生の花", "死の羽", "時の砂"]
        text = "" 

        #打印识别结果    
        for idx, res in enumerate(result):
            st.write(f"内容:")
            for line in res:
                #st.write(line[1][0])
                text += line[1][0] + "\n"
        # Split the text into lines and filter out empty lines
        non_empty_lines = [line.strip() for line in text.splitlines() if line.strip()]

        # Join the non-empty lines back into a single string
        result_text = '\n'.join(non_empty_lines)
        
        # Split the text into lines
        lines = result_text.split("\n")
        
        # Initialize variables to track the current context
        current_context = None
        
        # Keywords to check for the start of a new context
        keywords = ["空の杯", "理の冠", "生の花", "死の羽", "時の砂"]
        
        # Iterate through each line
        for i in range(len(lines)):
            line = lines[i]
        
            # Check for keywords indicating the start of a new context
            if any(keyword in line for keyword in keywords):
                current_context = "部位"
                # Check if there are at least two more lines
                if i + 2 < len(lines):
                    main_name = lines[i + 1]
                    main_num = lines[i + 2]
                    部位_list.append(line)
                    メイン属性_list.append(main_name)
                    メイン属性_list.append(main_num)
                else:
                    print(f"{line} -> 部位 (情報不足)")
            elif "+" in line:
                current_context = "サーブ属性"
                サーブ属性_list.append(line)
                line_count += 1
                # Check if the maximum number of lines is reached
                if line_count == max_lines:
                    break
        st.write("部位リスト:")
        st.write(部位_list)
        
        st.write("\nメイン属性リスト:")
        st.write(メイン属性_list)
        
        st.write("\nサーブ属性リスト:")
        st.write(サーブ属性_list[1:])


        # 从文件 "1.text" 中读取内容
        if os.path.isfile("search_artifacts_list.txt"):
            with open("search_artifacts_list.txt", "r",encoding="utf-8") as file:
                target_texts = [line.strip() for line in file.read().strip().split()]
                # 在识别结果中查找相同的词语
                for target_text in target_texts:
                    for idx, res in enumerate(result):
                        for line in res:
                            similarity = Levenshtein.ratio(line[1][0],target_text)
                            if similarity >= similarity_threshold:
                                st.write(f"認識した聖遺物の名前は： '{line[1][0]}' ,既存の聖遺物の名前は:{target_text}, 相似度: {similarity:.2f}")
                                # 设置搜索关键字
                                query = target_text+"gamewith"
                 # 在识别结果中查找相同的词语
                for target_text1 in artifacts:
                    for idx, res in enumerate(result):
                        for line in res:
                            similarity = Levenshtein.ratio(line[1][0],target_text1)
                            if similarity >= similarity_threshold:
                                #st.write(f"認識した聖遺物の部位は： '{line[1][0]}' ,既存の聖遺物の部位は:{target_text1}, 相似度: {similarity:.2f}")

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
                                                if (i +1) % 2 != 0:
                                                    content += text  
                                                    # 设置搜索关键字
                                                    query = text + "gamewith"
                                                    # 使用Google搜索库执行搜索
                                                    search_results = list(search(query, num=1, stop=1, pause=2))
                                                    # 获取第一个搜索结果的URL
                                                    first_result_url = search_results[0]
                                                    response = requests.get(first_result_url)
                                                    # 从URL中提取内容
                                                    if response.status_code == 200:
                                                        soup = BeautifulSoup(response.text, 'html.parser')
                                                        # 提取<div class="genshin saka">中的文本内容
                                                        genshin_saka_div = soup.find('div', class_='genshin_osusumesei_table')
                                                        if genshin_saka_div:                               
                                                            td_elements = genshin_saka_div.find_all('td')
                                                            for j,td in enumerate(td_elements):
                                                                text = td.get_text()
                                                                  # 如果当前文本与目标文本匹配
                                                                if text == target_text1:
                                                                    # 获取当前文本和下一个文本
                                                                    next_text = td_elements[j + 1].get_text(strip=True) if j + 1 < len(td_elements) else None

                                                                    # 输出当前文本和下一个文本
                                                                    #st.write(f"文本内容: {text}, 下一个文本内容: {next_text}")
                                                                    content += text + " " + next_text + " "
                                                                # 去掉首尾的空白
                                                                content = content.strip()
                                                               
                                                                
                                                        else:
                                                            content = "未找到指定的<div>元素"


                                            if (i +1) % 2 == 0:
                                                content += "\n---------------------\n"

                                        # 去掉首尾的空白
                                        content = content.strip()

                                        st.write(f"聖遺物セットの観点で考えるとおすすめのキャラは：{content}")
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
