import csv
import json

# 開啟 CSV 檔案
with open('spot.csv', mode='r', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file)
    
    # 將 CSV 內容轉換成字典列表
    data = [{"name": row[0], "image_url": row[1]} for row in csv_reader]

# 將字典列表寫入 JSON 檔案
with open('spot.json', mode='w', encoding='utf-8') as json_file:
    json.dump(data, json_file, indent=4, ensure_ascii=False)

print("CSV 轉換為 JSON 完成！")
