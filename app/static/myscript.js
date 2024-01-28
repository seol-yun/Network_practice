let latestId = null; // 가장 최근에 가져온 데이터의 id를 저장하는 변수
let skip = 0; // 기본적으로 가져올 데이터의 개수
let offset = 10; // 가져올 데이터의 시작 위치
let maxCount = 10; // 최대로 표시할 아이템 개수

async function fetchRequestWithError() {
    try {
        const url = `https://localhost:8443/pastebin/api/pastes/?id=${latestId || ''}&skip=${skip}&offset=${offset}`;
        const response = await fetch(url);
        if (response.status >= 200 && response.status < 400) {
            const data = await response.json();
            if (data.length > 0) {
                latestId = data[data.length - 1].id; // 최신 데이터의 id를 업데이트
                skip += data.length; // skip 값을 업데이트하여 중복을 방지

                for (var key in data) {
                    ndiv = document.createElement('div');
                    ndiv.innerHTML = `<h3> ${data[key]['title']} </h3><p> ${data[key]['content']}</p><hr>`;
                    pdiv = document.getElementById('pastes');
                    pdiv.insertBefore(ndiv, pdiv.firstChild); // 역순으로 삽입 여기서 추가되므로 >=임

                    // 10개를 넘으면 가장 오래된 아이템을 제거
                    if (pdiv.children.length >= maxCount) {
                        pdiv.removeChild(pdiv.lastChild);
                    }
                }
            } else {
                console.log('No new Data here');
            }
        } else {
            console.log(`${response.statusText}: ${response.status} error`);
        }
    } catch (error) {
        console.log(error);
    }
}
fetchint = setInterval(fetchRequestWithError, 1 * 1000);