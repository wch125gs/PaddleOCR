# 读取文件1和文件2的内容
with open('match1.txt', 'r', encoding='utf-8') as file1:
    content1 = file1.read().splitlines()

with open('match2.txt', 'r', encoding='utf-8') as file2:
    content2 = file2.read().splitlines()

# 找到第一个相同的部分的索引
index = 0
for index, line1 in enumerate(content1):
    if line1 in content2:
        break

# 创建一个文件3来保存相同和不同的内容
with open('match3.txt', 'w', encoding='utf-8') as file3:
    for i in range(index, len(content1)):
        if content1[i] in content2:
            file3.write(f'キャラの名前：{content1[i]}\n')
        else:
            file3.write(f'おすすめの聖遺物：{content1[i]}\n')



