# 指定要查询的特定キャラの名前
print("キャラの名前を入力してください")
specific_character = input()  # 你可以替换为你要查询的キャラの名前

# 创建一个字典来存储聖遺物和对应的キャラの名前
artifacts_for_specific_character = {}

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
        if current_character == specific_character:
            artifacts_for_specific_character[artifact] = current_character

# 输出特定キャラの名字的聖遺物
if artifacts_for_specific_character:
    print(f"{specific_character} の聖遺物：")
    for artifact, character in artifacts_for_specific_character.items():
        print(f"{artifact}")
else:
    print(f" {specific_character} の聖遺物がないです。")
