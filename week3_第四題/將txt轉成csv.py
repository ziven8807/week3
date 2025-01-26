
import csv
import json

# 讀取 .txt 文件
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

# 打開 CSV 文件進行寫入
with open('spot.csv', 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)


    # 遍歷結果並寫入 CSV 文件
    for attraction in results:
        # 提取所需的欄位
        stitle = attraction.get('stitle', '')  # 景點名稱

        
        # 提取圖片鏈接（假設圖片鏈接在 'filelist' 欄位中，多個圖片使用 ' ' 分隔）
        image_urls = attraction.get('filelist', '')
        image_url_list = image_urls.split('https://')  # 分割字串，提取多個圖片鏈接
        image_url = f"https://{image_url_list[1]}" if image_url_list else ''  # 取第一個圖片鏈接

        # 寫入 CSV 文件
        writer.writerow([stitle, image_url])

print("CSV 文件已成功生成！")
