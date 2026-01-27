// عداد الزوار
let count = localStorage.getItem("visits");
count = count ? Number(count) + 1 : 1;
localStorage.setItem("visits", count);
document.getElementById("count").innerText = count;

// لغتين
let ar = true;
function switchLang() {
  const text = document.getElementById("text");
  if (ar) {
    text.innerHTML = "💖 L'âme est pure 💖<br>☝️ Il n'y a de Dieu qu'Allah ☝️";
  } else {
    text.innerHTML = "💖 الروح ما فيهاش 💖<br>☝️ أشهد أن لا إله إلا الله ☝️";
  }
  ar = !ar;
}