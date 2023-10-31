# 特定聖遺物的名称
print("聖遺物の名前を入力してください")
specific_artifact = input()  # 你可以替换为你要查找的聖遺物名称

# 创建一个字典来存储キャラの名前和对应的聖遺物
characters_with_specific_artifact = {}

# 读取生成的文件
with open('match4.txt', 'r', encoding='utf-8') as file:
    lines = file.read().splitlines()

# 初始化当前的キャラの名前
current_character = None

# 遍历每一行
for line in lines:
    if line.startswith('キャラの名前：'):
        current_character = line.replace('キャラの名前：', '')
    elif line.startswith('おすすめの聖遺物：'):
        artifact = line.replace('おすすすめの聖遺物：', '')
        if specific_artifact in artifact:
            characters_with_specific_artifact[current_character] = artifact

# 输出包含特定聖遺物的キャラの名前
if characters_with_specific_artifact:
    print(f"おすすめ聖遺物'{specific_artifact}' のキャラの名前：")
    for character, artifact in characters_with_specific_artifact.items():
        print(f"{character}: {artifact}")
else:
    print(f"おすすめ聖遺物 '{specific_artifact}' のキャラの名前がないです。")
