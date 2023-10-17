import streamlit as st
from PIL import Image
from paddleocr import PaddleOCR, draw_ocr
import os
import difflib


# 定义语言对应的文本
language_texts = {
    'ch': {
        'title': "图像识别Web应用",
        'upload_prompt': "上传多张图片...",
        'results_header': "识别结果:",
        'visualization_caption': "可视化",
        'language': "语言选择"
    },
    'en': {
        'title': "Image Recognition Web App",
        'upload_prompt': "Upload multiple images...",
        'results_header': "Recognition results:",
        'visualization_caption': "Visualization",
        'language': "Select Language"
    },
    'japan': {
        'title': "画像認識ウェブアプリ",
        'upload_prompt': "複数の画像をアップロード...",
        'results_header': "認識結果:",
        'visualization_caption': "可視化",
        'language': "言語選択"
    },
    # 添加其他语言的文本
}

# 添加语言选择下拉菜单
languages = list(language_texts.keys())
selected_lang = st.selectbox("Select Language", languages)

st.title(language_texts[selected_lang]['title'])


# 添加文件上传小部件
uploaded_files = st.file_uploader(language_texts[selected_lang]['upload_prompt'],
                                  type=["jpg", "png", "jpeg"], accept_multiple_files=True)

# 圣遗物适用人物
Recommended_Artifacts = [
    {
        'character': 'ベネット',
        'artifact_name': '旧貴族の銀瓶',
        'main_attributes': ['HP%', '炎元素ダメージ'],
        'sub_attributes': 'HP%/元素チャージ/会心系',
    },
    {
        'character': 'ベネット',
        'artifact_name': '旧貴族の仮面',
        'main_attributes': ['与える治療効果', '会心率', '会心ダメージ'],
        'sub_attributes': 'HP%/元素チャージ/会心系',
    },
    {
        'character': 'ベネット',
        'artifact_name': '旧貴族の花',
        'main_attributes': ['HP%'],
        'sub_attributes': 'HP%/元素チャージ/会心系',
    },
    {
        'character': 'ベネット',
        'artifact_name': '旧貴族の羽根',
        'main_attributes': ['攻撃力%'],
        'sub_attributes': 'HP%/元素チャージ/会心系',
    },
    {
        'character': 'ベネット',
        'artifact_name': '旧貴族の時計',
        'main_attributes': ['HP', '元素チャージ'],
        'sub_attributes': 'HP%/元素チャージ/会心系',
    },
    {
        'character': '夜蘭',
        'artifact_name': '威厳の鍔',
        'main_attributes': ['HP%'],
        'sub_attributes': '会心系/HP%/元素チャージ',
    },
    {
        'character': '夜蘭',
        'artifact_name': '雷雲の印籠',
        'main_attributes': ['HP%','元素チャージ'],
        'sub_attributes': '会心系/元素チャージ/HP',
    },
    {
        'character': '雷電将軍',
        'artifact_name': '雷雲の印籠',
        'main_attributes': ['攻撃力%','元素チャージ'],
        'sub_attributes': '会心系/攻撃力%/元素熟知',
    },
]

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

        # 获取第一行的文字内容
        line_texts = [element[1][0] for element in result[0] if isinstance(element, list) and len(element) > 1 and len(element[1]) > 0]
        first_line_texts = line_texts[0]

        # 获取第三行的文字内容
        third_line_texts = line_texts[2]

        # 判断是否有识别结果
        if first_line_texts and len(first_line_texts) >= 0:
            artifact_name = first_line_texts
            main_attribute =  third_line_texts

            best_match = None
            best_match_similarity = 0.8

           # 存储匹配结果的列表
            matches = []

            # 遍历所有推荐的圣遗物信息
            for recommendation in Recommended_Artifacts:
                # 计算圣遗物名称的相似度
                artifact_similarity = difflib.SequenceMatcher(None, artifact_name, recommendation['artifact_name']).ratio()

                # 遍历推荐圣遗物的主属性
                for main_attribute in recommendation.get('main_attributes', []):
                    # 计算主属性的相似度
                    main_attribute_similarity = difflib.SequenceMatcher(None, main_attribute, main_attribute).ratio()

                    # 计算总体相似度
                    total_similarity = (artifact_similarity + main_attribute_similarity) / 2

                    # 存储匹配结果
                    matches.append({'recommendation': recommendation, 'total_similarity': total_similarity})

            # 根据相似度降序排列匹配结果
            sorted_matches = sorted(matches, key=lambda x: x['total_similarity'], reverse=True)

            # 输出前三个匹配结果
            st.subheader("判断结果:")
            if sorted_matches:
                for i, match in enumerate(sorted_matches[:3]):
                    recommendation = match['recommendation']
                    total_similarity = match['total_similarity']

                    st.write(f"Top {i + 1}")
                    st.write(f"適合度: {total_similarity:.2%}")
                    st.write(f"人物名称: {recommendation['character']}")
                    st.write(f"聖遺物名称: {recommendation['artifact_name']}")
                    if 'main_attributes' in recommendation:
                        st.write(f"メイン属性: {', '.join(recommendation['main_attributes'])}")
                    if 'sub_attributes' in recommendation:
                        st.write(f"サブ属性: {recommendation['sub_attributes']}")
                    st.write("--------------")
            else:
                st.write("未找到匹配的人物")

    
        # 打印识别结果
        
        #for idx, res in enumerate(result):
            #st.write(f"内容:")
            #for line in res:
                #st.write(line[1][0])
        
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