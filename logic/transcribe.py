import whisper
from pydub import AudioSegment

path = "tests/repeatSpeech.wav"

## Getting transcript and audio
audio = AudioSegment.from_wav(path)

model = whisper.load_model("small.en")
result = model.transcribe(path)
transcript = result["text"][1:]

## Getting better transcript with filler words; use huggingface modified whisper
#filler_result = model.transcribe(path, verbose=True)

