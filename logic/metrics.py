from transcribe import *
from pydub import AudioSegment, silence
import re

## SPEECH RATE (WPM) ; stuttering etc. associated with low speech rate
# Remove filler words to avoid artificially inflating word count?

def speechrate(transcript, path):
    words = transcript.split(" ")
    time = len(AudioSegment.from_wav(path)) / (1000 * 60) # Convert milliseconds to minutes
    wpm = len(words) / time 
    return words, time, wpm ## for testing
    #return wpm

## REPETITIONS ; count number of repetition instances with regex. A word is a repetition if 
## it matches what's directly behind it.
# Rudimentary implementation: improve later with partial repetition counting as well. Note
# transcription will also have to be updated to include filler words etc. for this to work, changing regex
# alone won't be enough

def repetitions(text):
    pattern = r'\b(\w+)(?:\s+\1)+\b'
    repetitions = re.findall(pattern, text.lower())
    return len(repetitions)

## FILLED PAUSES ; filler words
filler_words = ["hm", "hmm", "um", "uh", "like", "so", "well", "right"]

def filler_pauses(transcript):
    count = 0
    filler_times = []
    words = transcript.split(" ")
    for word in words:
        if word.lower() in filler_words:
            count += 1
            filler_times.append((word["start"], word["end"]))
    return count, filler_times

## SILENT PAUSES ; pauses in speech that are longer than a certain threshold (e.g., 2 seconds)
## and below a certain loudness threshold
# Get start and end times for segments in seconds ; for easier understanding when plotting

def silent_pauses(audio, threshold=1000):

    silent_segments = silence.detect_silence(audio, min_silence_len=threshold, silence_thresh=-40)
    silent_durations = [(start / 1000, end / 1000) for start, end in silent_segments]
    return silent_durations


print(silent_pauses(audio))

words, time, wpm = speechrate(transcript, path)

count, filler_times = filler_pauses(transcript)
print("count: ", count, " filler_times: ", filler_times)

print(f"words: {words}")
print(transcript)
print(f"num words: {len(words)}")
print(f"time: {time}")
print(f"wpm: {wpm}")
    
