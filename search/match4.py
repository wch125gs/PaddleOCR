# 读取原始内容
with open('match3.txt', 'r', encoding='utf-8') as file:
    lines = file.read().splitlines()

# 创建一个字典来存储分组后的内容
grouped_content = {}

# 初始化当前的角色名字
current_character = None

# 遍历每一行
for line in lines:
    if "キャラの名前：" in line:
        current_character = line.replace("キャラの名前：", '')
    elif "おすすめの聖遺物：" in line:
        if current_character is not None:
            if current_character not in grouped_content:
                grouped_content[current_character] = []
            grouped_content[current_character].append(line.replace("おすすめの聖遺物：", ''))

# 将结果写入新文件
with open('match4.txt', 'w', encoding='utf-8') as file:
    for character, artifacts in grouped_content.items():
        file.write(f'キャラの名前：{character}\n')
        for artifact in artifacts:
            file.write(f'おすすめの聖遺物：{artifact}\n')
