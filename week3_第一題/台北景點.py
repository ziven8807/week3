import csv
import json
import re  # 用於正則表達式

# 讀取第一個 .txt 文件（taipei-attractions-assignment-1）
with open('taipei-attractions-assignment-1', 'r', encoding='utf-8') as txt_file:
    data = txt_file.read()  # 讀取文件中的全部內容

# 解析 JSON 資料
try:
    json_data = json.loads(data)  # 轉換為 JSON 格式
except json.JSONDecodeError:
    print("無法解析 JSON 資料")
    exit()

# 提取 'results' 資料部分，它是一個列表（array）
results = json_data.get('data', {}).get('results', [])

# 讀取第二個 .txt 文件（taipei-attractions-assignment-2）來取得 SERIAL_NO 來判斷 district的位置
district_mapping = {}
with open('taipei-attractions-assignment-2', 'r', encoding='utf-8') as txt_file_2:
    data_2 = txt_file_2.read()  # 讀取第二個文件中的全部內容

# 解析第二個文件的 JSON 資料
try:
    json_data_2 = json.loads(data_2)  # 轉換為 JSON 格式
except json.JSONDecodeError:
    print("無法解析第二個 JSON 資料")
    exit()

# 檢查 json_data_2 是dict，並處理 'data' 欄位
if isinstance(json_data_2, dict):
    # 確保處理的是 'data' 欄位，這裡 'data' 是一個array
    results_2 = json_data_2.get('data', [])
    
    for attraction in results_2:
        SERIAL_NO_2 = attraction.get('SERIAL_NO', '')
        address = attraction.get('address', '')
        
        # 從地址中提取區域（只保留區域名，ex -> '北投區'）
        district = ''
        if address:
            # 使用正則表達式從地址中提取包含"區"的部分
            match = re.search(r'(\w+區)', address)
            if match:
                district = match.group(0)  # 提取區域名稱
        
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
        # 查找對應的 district
        district = district_mapping.get(attraction.get('SERIAL_NO', ''), '')  # 根據 SERIAL_NO 查找區域
        longitude = attraction.get('longitude', '')  # 經度
        latitude = attraction.get('latitude', '')  # 緯度
        # 提取圖片鏈接（假設圖片鏈接在 'filelist' 欄位中，多個圖片使用 ' ' 分隔）
        image_urls = attraction.get('filelist', '')
        image_url_list = image_urls.split('https://')  # 分割字串，提取多個圖片鏈接
        image_url = f"https://{image_url_list[1]}" if image_url_list else ''  # 取第一個圖片鏈接

        # 寫入 CSV 文件
        writer.writerow([stitle, district, longitude, latitude, image_url])

print("CSV 文件已成功生成！")















