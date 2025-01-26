import json
import urllib.request  
from collections import defaultdict

# 從網路上下載第二個 JSON 資料（taipei-attractions-assignment-2）
url_2 = 'https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-2'
try:
    with urllib.request.urlopen(url_2) as response_2:
        data_2 = response_2.read().decode('utf-8')  # 取得第二個檔案的內容
except Exception as e:
    print(f"無法從 {url_2} 下載資料: {e}")
    exit()

# 解析第二個 JSON 資料
try:
    json_data_2 = json.loads(data_2)  # 轉換為 JSON 格式
except json.JSONDecodeError:
    print("無法解析第二個 JSON 資料")
    exit()

# 檢查 json_data_2 是dict，並處理 'data' 欄位
station_mapping = {}
mrt_attractions = defaultdict(list)  # 用來存放同一捷運站的景點

if isinstance(json_data_2, dict):
    results_2 = json_data_2.get('data', [])
    
    # 建立捷運站的 SERIAL_NO 和 MRT（捷運站名稱）的對應dict
    for station in results_2:
        SERIAL_NO_2 = station.get('SERIAL_NO', '')
        mrt_name = station.get('MRT', '')  # 使用 MRT 名稱作為捷運站名稱
        station_mapping[SERIAL_NO_2] = mrt_name
else:
    print("第二個 JSON 文件結構錯誤，應該是dict")
    exit()

# 從網路上下載第一個 JSON 資料（taipei-attractions-assignment-1）
url_1 = 'https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-1'
try:
    with urllib.request.urlopen(url_1) as response_1:
        data_1 = response_1.read().decode('utf-8')  # 取得第一個檔案的內容
except Exception as e:
    print(f"無法從 {url_1} 下載資料: {e}")
    exit()

# 解析第一個 JSON 資料
try:
    json_data_1 = json.loads(data_1)  # 轉換為 JSON 格式
except json.JSONDecodeError:
    print("無法解析第一個 JSON 資料")
    exit()

# 提取 'results' 資料部分
results_1 = json_data_1.get('data', {}).get('results', [])

# 根據 SERIAL_NO 將景點按捷運站分組
for attraction in results_1:
    SERIAL_NO = attraction.get('SERIAL_NO', '')
    stitle = attraction.get('stitle', '')  # 景點名稱

    # 根據 SERIAL_NO 查找對應的捷運站名稱
    mrt_station = station_mapping.get(SERIAL_NO, '未知站')

    # 將景點名稱按捷運站分組
    mrt_attractions[mrt_station].append(stitle)

# 生成 CSV 文件
with open('mrt.csv', 'w', newline='', encoding='utf-8') as file:
    # 寫入每個捷運站和其景點
    for mrt_station, attractions in mrt_attractions.items():
        # 使用逗號連接景點名稱
        attractions_str = ','.join(attractions)
        # 寫入一行數據：捷運站名稱, 景點列表
        file.write(f'{mrt_station},{attractions_str}\n')

print("CSV 文件已成功生成！")
