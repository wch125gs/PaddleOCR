# 打开并读取1.txt文件
with open('search_character.txt', 'r', encoding='utf-8') as file1:
    content1 = file1.read()


# 打开并读取2.txt文件
with open('search_artifacts_list.txt', 'r', encoding='utf-8') as file2:
    content2 = file2.read()


# 检查文件2中的文本是否在文件1中
for phrase2 in content2.split():
    if phrase2 in content1:
        print(f"match artifacts:{phrase2}")





