function shortenUrl() {
  const input = document.getElementById('urlInput');
  const result = document.getElementById('resultDisplay');
  const shortUrl = document.getElementById('shortUrl');

  if (input.value.trim()) {
    // 실제로는 서버에 요청을 보내야 함
    const randomCode = Math.random().toString(36).substring(2, 8);
    shortUrl.href = `http://bit.ly/${randomCode}`;
    shortUrl.textContent = `bit.ly/${randomCode}`;
    result.style.display = 'block';

    // 성공 애니메이션
    result.style.animation = 'slideIn 0.5s ease-out';
  }
}

function copyUrl() {
  const shortUrl = document.getElementById('shortUrl');
  navigator.clipboard.writeText(shortUrl.href).then(() => {
    alert('URL이 클립보드에 복사되었습니다!');
  });
}

// 엔터 키로 단축하기
document.getElementById('urlInput').addEventListener('keypress', function (e) {
  if (e.key === 'Enter') {
    shortenUrl();
  }
});
