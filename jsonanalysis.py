import json

file_path = "zh_cn.json"

# 打开并读取JSON文件
with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# 现在 'data' 是一个包含所有键值对的字典
# 你可以遍历这些键值对，或者直接访问特定条目
for key, value in list(data.items()):  # 只打印前五个条目作为示例
    print(f"{key}: {value}")