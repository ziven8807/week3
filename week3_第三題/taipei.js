fetch(
  "https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-1"
)
  .then((response) => response.json())
  .then((data) => {
    console.log("Data received:", JSON.stringify(data, null, 2)); // 打印完整的返回資料

    const attractions = data.data.results; // 獲取所有的景點資料

    attractions.forEach((item, index) => {
      console.log(`Item ${index}:`, JSON.stringify(item, null, 2)); // 打印每個項目的詳細資料

      // 獲取所有的 .image-item 元素
      const items = document.querySelectorAll(".image-item");

      if (items[index]) {
        const img = items[index].querySelector(".image"); // 獲取圖片區域
        const textDiv = items[index].querySelector(".text"); // 獲取文字區域

        // 打印圖片 URL 和文字內容
        console.log("Image URL for item", index, ":", item.filelist); // 輸出圖片列表欄位
        console.log("Text for item", index, ":", item.stitle); // 輸出文字內容

        // 處理 filelist 字串，將圖片 URL 提取出來
        const imageUrls = item.filelist
          .split("https://")
          .filter((url) => url)
          .map((url) => "https://" + url);
        console.log("Parsed image URLs for item", index, ":", imageUrls); // 打印所有解析出來的圖片 URL

        // 確保獲取到圖片 URL
        if (img && imageUrls.length > 0) {
          img.src = imageUrls[0]; // 更新圖片（這裡選擇使用第一個圖片 URL）
        } else {
          console.error("Image URL not found for item", index); // 如果沒有找到圖片，則報錯
        }

        // 更新文字內容
        if (textDiv && item.stitle) {
          textDiv.textContent = item.stitle; // 更新文字內容
        } else {
          console.error("Text not found for item", index); // 如果沒有找到文字，則報錯
        }
      }
    });
  })
  .catch((error) => console.error("Error loading the JSON file:", error)); // 載入資料時發生錯誤
