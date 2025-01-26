import requests
from bs4 import BeautifulSoup
from datetime import datetime
import csv

# PTT 的看板頁面 URL
url = 'https://www.ptt.cc/bbs/Lottery/index.html'  # 彩券版

# 送出請求並獲取頁面內容
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
response = requests.get(url, headers=headers)

# 確保返回 200 狀態碼
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 找到文章的列表，通常會在 <div class="r-ent"> 標籤裡，要記得
    posts = soup.find_all('div', class_='r-ent')

    # 開啟 CSV 檔案來寫入資料
    with open('ptt_lottery_posts.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        for post in posts:
            # 標題
            title_tag = post.find('a')
            if title_tag:
                title = title_tag.text.strip()
            else:
                title = None
            
            # 刊登時間
            date_tag = post.find('div', class_='date')
            if date_tag:
                date_str = date_tag.text.strip()  # 獲取時間字串
                
                # PTT 時間是 MM/DD 格式，並且手動補充當前年份
                current_year = datetime.now().year
                formatted_date = f"{date_str}/{current_year}"
                
                # 轉換為 datetime 物件，並格式化為完整日期
                try:
                    # 使用 strptime 解析 MM/DD/YYYY 格式
                    date_obj = datetime.strptime(formatted_date, '%m/%d/%Y')
                    # 獲取星期幾，轉換為完整的日期格式
                    formatted_date = date_obj.strftime('%a %b %d %H:%M:%S %Y')
                except ValueError:
                    formatted_date = None
            else:
                formatted_date = None
            
            # Like/Dislike 統計
            like_dislike_tag = post.find('div', class_='nrec')
            if like_dislike_tag:
                like_dislike_count = like_dislike_tag.text.strip()
                if like_dislike_count == '爆':  # 出現"爆"代表很多人讚同
                    like_dislike_count = '爆'
                elif like_dislike_count == 'X':  # 如果是 'X' 則表示沒有反對
                    like_dislike_count = 'X'
                elif like_dislike_count == '':  # 如果為空則表示沒有人按讚
                    like_dislike_count = 0  # 沒有按讚就給 0
            else:
                like_dislike_count = 0  # 沒有按讚就給 0

            # 寫入每篇文章的資料到 CSV
            writer.writerow([title, like_dislike_count, formatted_date])
else:
    print(f"無法獲取頁面, 狀態碼: {response.status_code}")
