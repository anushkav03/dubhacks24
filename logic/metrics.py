from transcribe import *
from pydub import AudioSegment, silence
import re


def speechrate(transcript, path):
    words = transcript.split(" ")
    time = len(AudioSegment.from_wav(path)) / (1000 * 60) # Convert milliseconds to minutes
    wpm = len(words) / time 
    return words, time, wpm ## for testing


def repetitions(text):
    pattern = r'\b(\w+)(?:\s+\1)+\b'
    repetitions = re.findall(pattern, text.lower())
    return len(repetitions)


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


def silent_pauses(audio, threshold=1000):

    silent_segments = silence.detect_silence(audio, min_silence_len=threshold, silence_thresh=-40)
    silent_durations = [(start / 1000, end / 1000) for start, end in silent_segments]
    return silent_durations


