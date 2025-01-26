fetch(
  "https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-1"
)
  .then((response) => response.json())
  .then((data) => {
    console.log("Data received:", JSON.stringify(data, null, 2)); // 打印完整的返回資料

    const attractions = data.data.results; // 獲取所有的景點資料

    // 取得所有的 .image-item 元素（也就是 promotion1~3 和 Title1 ~ 10）
    const items = document.querySelectorAll(".image-item");

    // 遍歷資料並插入每一個item
    attractions.forEach((item, index) => {
      if (items[index]) {
        // 獲取每個項目的圖片和文字區域
        const img = items[index].querySelector(".image"); // 獲取圖片區域
        const textDiv = items[index].querySelector(".text"); // 獲取文字區域

        // 處理 filelist 字串，將圖片 URL 提取出來
        const imageUrls = item.filelist
          .split("https://")
          .filter((url) => url)
          .map((url) => "https://" + url);

        // 確保獲取到圖片 URL
        if (img && imageUrls.length > 0) {
          img.src = imageUrls[0]; // 使用第一個圖片 URL 更新圖片
        } else {
          console.error("Image URL not found for item", index); // 如果找不到圖片，則報錯
        }

        // 更新文字內容
        if (textDiv && item.stitle) {
          textDiv.textContent = item.stitle; // 更新文字內容
        } else {
          console.error("Text not found for item", index); // 如果找不到文字，則報錯
        }
      }
    });

    // 獲取 Load More 按鈕和容器元素
    const loadMoreBtn = document.getElementById("load-more-btn");
    const container = document.querySelector("body"); // 可以選擇其他容器，這裡選擇 body

    // 目前顯示的資料索引，從上一輪 "Load More" 點擊後的最後index開始
    let currentIndex = items.length;

    // 按下 Load More 按鈕時執行的func
    loadMoreBtn.addEventListener("click", function () {
      // 創建一個新的 big-and-mid-image-container 元素
      const newContainer = document.createElement("div");
      newContainer.classList.add("big-and-mid-image-container");

      // 設定新的item數量（假設每次載入 10 個）
      const newItems = attractions.slice(currentIndex, currentIndex + 10); // 從 data 中切取下一批資料

      // 按照每 5 個顯示 5 個中圖和 3 個大圖來插入新內容
      newItems.forEach((item, index) => {
        const titleIndex = currentIndex + index + 1; // 計算標題的編號

        let itemHTML = "";
        // 根據索引決定是大圖還是中圖
        const imageUrls = item.filelist
          .split("https://")
          .filter((url) => url)
          .map((url) => "https://" + url);
        const imageUrl = imageUrls.length > 0 ? imageUrls[0] : ""; // 取第一個圖片 URL

        if (index % 5 === 0) {
          // index1與5是大圖
          itemHTML = `
            <div class="big-image-item image-item title-${titleIndex}">
              <img src="${imageUrl}" alt="Title ${titleIndex}" class="big-image image" />
              <div class="big-image-text text">${item.stitle}</div>
            </div>
          `;
        } else {
          // 除了1與5整除的index以外是中圖
          itemHTML = `
            <div class="mid-image-item image-item title-${titleIndex}">
              <img src="${imageUrl}" alt="Title ${titleIndex}" class="mid-image image" />
              <div class="mid-image-text text">${item.stitle}</div>
            </div>
          `;
        }

        // 將創建的 HTML 結構插入新的容器
        newContainer.innerHTML += itemHTML;
      });

      // 更新 currentIndex，確保下次點擊時是接續在已顯示的item後面
      currentIndex += 10;

      // 把新的容器元素插入到頁面的最後
      container.appendChild(newContainer);

      // 按下按鈕會自動滾動到頁面底部
      window.scrollTo({
        top: document.body.scrollHeight,
        behavior: "smooth",
      });
    });
  })
  .catch((error) => console.error("Error loading the JSON file:", error)); // 載入資料時出錯的話
