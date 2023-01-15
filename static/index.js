const showImage = document.querySelector(".showImage");

// 取得圖片
async function getHeadshot() {
  const response = await fetch("api/headshot", {
    method: "GET",
    headers: { "Content-Type": "application/json" },
  });
  const getPhoto = await response.json();
  if (getPhoto.data != null) {
    for (let i = 0; i < getPhoto.data.length; i++) {
      let photo = getPhoto.data[i].photo;
      let text = getPhoto.data[i].text;

      const allText = document.createElement("div");
      allText.setAttribute("class", "text");
      const textElement = document.createTextNode(text);

      const allImage = document.createElement("img");
      allImage.setAttribute("src", "https://d3njnkd7r25n5m.cloudfront.net/" + photo);

      const line = document.createElement("hr");

      showImage.appendChild(line);
      showImage.appendChild(allText);
      allText.appendChild(textElement);
      showImage.appendChild(allImage); 
    }
  }
}
getHeadshot();
// 輸入文字內容
let inputValue;
const word = document.getElementById("word");
word.addEventListener("input", () => {
  if (word.value == "") {
    inputValue = false;
  } else {
    inputValue = true;
  }
});

// 上傳圖片
const confirmUpload = document.querySelector(".confirmUpload");
confirmUpload.addEventListener("click", () => {
  if (!inputValue) {
    alert("請輸入文字");
    return;
  } else {
    const choosePhoto = document.getElementById("choosePhoto").files[0];
    const inputWord = document.getElementsByClassName("textWord")[0].value;
    if (inputWord == "") {
      alert("請輸入文字");
      return;
    } else if (choosePhoto == null) {
      alert("請選擇要上傳的圖片");
      return;
    } else {
      let formData = new FormData();
      formData.append("headshot", choosePhoto);
      formData.append("word", inputWord);
      fetch("/api/headshot", {
        method: "POST",
        body: formData,
      })
        .then(function (response) {
          return response.json();
        })
        .then(function (upload) {
          if (upload.ok) {
            alert("上傳成功");
          } else {
            alert("上傳失敗");
          }
        });
    }
  }
});