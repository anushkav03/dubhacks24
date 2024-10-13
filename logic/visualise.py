import matplotlib.pyplot as plt
from transcribe import *
from metrics import *

## Calling metrics on audio
words, time, wpm = speechrate(transcript, path)
num_repetitions = repetitions(transcript)
filler_count, filler_times = filler_pauses(transcript)


## Speech rate
plt.bar([path], [wpm], color='blue')
plt.ylabel('Words Per Minute (WPM)')
plt.xlabel('User Input')
plt.title('Speech Rate (WPM) for User Input')

plt.figure(figsize=(10, 6))

plt.subplot(1, 3, 1)

## Repetitions
percentage_repeated = (num_repetitions / len(words)) * 100
plt.bar(["Repeated Words"], [percentage_repeated], color='green')
plt.ylabel('Percentage (%)')
plt.title('Percentage of Repeated Words in Transcript')
plt.subplot(1, 3, 2)


plt.tight_layout()
plt.show()