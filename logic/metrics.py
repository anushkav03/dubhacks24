from transcribe import *

## Speech rate (WPM) ; stuttering etc. associated with low speech rate
# Remove filler words to avoid artificially inflating word count?

def speechrate(transcript, path):
    words = transcript.split(" ")
    time = len(AudioSegment.from_wav(path)) / (1000 * 60) # Convert milliseconds to minutes
    wpm = len(words) / time 
    #return words, time, wpm ## for testing
    return wpm


#words, time, wpm = speechrate(transcript, path)

#print(f"words: {words}")
#print(transcript)
#print(f"num words: {len(words)}")
#print(f"time: {time}")
#print(f"wpm: {wpm}")
    
