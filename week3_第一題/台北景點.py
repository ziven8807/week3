import csv
import json
import re
import requests  # 用於網路請求

# 從網路上下載第一個 JSON 資料
url_1 = 'https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-1'
response_1 = requests.get(url_1)

if response_1.status_code == 200:
    data_1 = response_1.text  # 取得第一個檔案的內容
else:
    print(f"無法從 {url_1} 下載資料")
    exit()

# 解析 JSON 資料
try:
    json_data = json.loads(data_1)
except json.JSONDecodeError:
    print("無法解析第一個 JSON 資料")
    exit()

# 提取 'results' 資料部分
results = json_data.get('data', {}).get('results', [])

# 從網路上下載第二個 JSON 資料
url_2 = 'https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-2'
response_2 = requests.get(url_2)

if response_2.status_code == 200:
    data_2 = response_2.text  # 取得第二個檔案的內容
else:
    print(f"無法從 {url_2} 下載資料")
    exit()

# 解析第二個 JSON 資料
try:
    json_data_2 = json.loads(data_2)
except json.JSONDecodeError:
    print("無法解析第二個 JSON 資料")
    exit()

# 檢查 json_data_2 是dict，並處理 'data' 欄位
district_mapping = {}
if isinstance(json_data_2, dict):
    results_2 = json_data_2.get('data', [])
    
    for attraction in results_2:
        SERIAL_NO_2 = attraction.get('SERIAL_NO', '')
        address = attraction.get('address', '')
        
        district = ''
        if address:
            match = re.search(r'(\w+區)', address)
            if match:
                district = match.group(0)
        
        district_mapping[SERIAL_NO_2] = district
else:
    print("第二個 JSON 文件結構錯誤，應該是字典格式")
    exit()

# 打開 CSV 文件進行寫入
with open('spot.csv', 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)


    # 遍歷第一個結果並寫入 CSV 文件
    for attraction in results:
        # 提取所需的欄位
        stitle = attraction.get('stitle', '')  # 景點名稱
        longitude = attraction.get('longitude', '')  # 經度
        latitude = attraction.get('latitude', '')  # 緯度

        # 查找對應的 district
        district = district_mapping.get(attraction.get('SERIAL_NO', ''), '')  # 根據 SERIAL_NO 查找區域

        # 提取圖片鏈接
        image_urls = attraction.get('filelist', '')
        image_url_list = image_urls.split('https://')  # 分割字串，提取多個圖片鏈接
        image_url = f"https://{image_url_list[1]}" if image_url_list else ''  # 取第一個圖片鏈接

        # 寫入 CSV 文件
        writer.writerow([stitle, district, longitude, latitude, image_url])

print("CSV 文件已成功生成！")














