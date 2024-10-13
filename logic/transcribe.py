import whisper
from pydub import AudioSegment

path = "../tests/userSpeech.wav"

## Getting transcript and audio
audio = AudioSegment.from_wav(path)

model = whisper.load_model("small.en")
result = model.transcribe(path)
transcript = result["text"][1:]