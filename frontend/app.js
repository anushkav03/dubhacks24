let recorder, audioChunks;
let speechRecognition = new webkitSpeechRecognition() || new SpeechRecognition();
speechRecognition.lang = 'en-US';
speechRecognition.interimResults = false;

const startButton = document.getElementById('start');
const stopButton = document.getElementById('stop');
const userIcon = document.getElementById('userIcon');
const pollyIcon = document.getElementById('pollyIcon');

startButton.addEventListener('click', () => {
    startRecording();
    speechRecognition.start();
    userIcon.style.backgroundColor = 'green';  // Change user icon to green while speaking
});

stopButton.addEventListener('click', () => {
    stopRecording();
    speechRecognition.stop();
    userIcon.style.backgroundColor = '#ccc';  // Reset user icon color after stopping
});

speechRecognition.onresult = async function(event) {
    const userSpeech = event.results[0][0].transcript;
    console.log('User said:', userSpeech);
    await interactWithPolly(userSpeech);
};

function startRecording() {
    navigator.mediaDevices.getUserMedia({ audio: true }).then(stream => {
        recorder = new MediaRecorder(stream);
        audioChunks = [];

        recorder.ondataavailable = e => {
            audioChunks.push(e.data);
        };

        recorder.onstop = () => {
            const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
            const audioUrl = URL.createObjectURL(audioBlob);
            saveAudioFile(audioBlob);
        };

        recorder.start();
    });
}

function stopRecording() {
    if (recorder) {
        recorder.stop();
    }
}

function saveAudioFile(blob) {
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = 'userSpeech.wav';
    link.click();
}

async function interactWithPolly(text) {
    pollyIcon.style.backgroundColor = 'green';  // Change Polly icon to green while responding

    const response = await fetch('/polly', { 
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text })
    });
    
    const responseData = await response.blob();
    const pollyAudioUrl = URL.createObjectURL(responseData);
    const pollyAudio = new Audio(pollyAudioUrl);

    pollyAudio.play();
    pollyAudio.onended = () => {
        pollyIcon.style.backgroundColor = '#ccc';  // Reset Polly icon color after response
    };
}
