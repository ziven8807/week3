// 切換選單顯示/隱藏
function toggleMenu() {
  const menu = document.querySelector(".menu");
  const hamburger = document.querySelector(".hamburger");
  const closeMenu = document.querySelector(".close-menu");

  // 切換菜單顯示狀態
  menu.classList.toggle("show");

  // 切換顯示漢堡圖示與 "X"
  hamburger.classList.toggle("active"); // 隱藏漢堡圖示
  closeMenu.classList.toggle("active"); // 顯示或隱藏 "X"
}

// 當 DOM 完全加載後綁定事件
document.addEventListener("DOMContentLoaded", function () {
  const hamburger = document.querySelector("#hamburger"); // 取得漢堡圖示
  const closeMenu = document.querySelector("#close-menu"); // 取得 "X" 圖示

  if (hamburger) {
    hamburger.addEventListener("click", toggleMenu); // 綁定點擊事件
  }

  if (closeMenu) {
    closeMenu.addEventListener("click", toggleMenu); // "X" 圖示點擊也綁定 toggleMenu
  }
});
