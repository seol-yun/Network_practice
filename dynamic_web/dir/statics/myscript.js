const myInterval = setInterval(myTimer, 1000);

function myTimer() {
  const date = new Date();
  document.getElementById('timer').innerHTML = '현재 시간: ' + date.toLocaleTimeString() + '<br><button onclick="myTimerStop()">Stop time</button><br>';
}

function myTimerStop() {
  clearInterval(myInterval);
}
