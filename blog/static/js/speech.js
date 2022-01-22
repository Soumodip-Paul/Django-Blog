function recogniseText() {
    window.SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (window.SpeechRecognition && window.navigator.onLine) {
        const recognition = new SpeechRecognition();
        recognition.interimResults = true;
        
        recognition.addEventListener('result', e => {
            const transcript = Array.from(e.results)
            .map(result => result[0])
            .map(result => result.transcript)
            .join('')
            
            document.querySelector('input#qs').value = transcript
            // console.log(transcript);
        });
        recognition.addEventListener('start', e => {
            document.getElementById('pulseRing').classList.toggle('pulse-ring')
        })
        recognition.addEventListener('end', e => {
            document.getElementById('pulseRing').classList.toggle('pulse-ring')
            document.querySelector('form#searchForm').submit()
        });
        recognition.start();
    }
    else {
        showAlert('You are Offline', "Turn on internet to use voice search")
    }
}