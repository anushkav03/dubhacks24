import os
import numpy as np
import matplotlib.pyplot as plt
from pydub import AudioSegment
from transcribe import *
from metrics import *

# Directories containing audio files
directory_1 = 'llm-audio'
# directory_2 = 'path_to_directory_2'

# Initialize dictionaries to store results for each directory
results = {
    "dir1": {"paths": [], "speech_rates": [], "repetition_percentages": [], "filler_counts": []} ,
    "dir2": {"paths": [], "speech_rates": [], "repetition_percentages": [], "filler_counts": []}
}

# Function to process and generate metrics for each audio file
def process_directory(directory, dir_key):
    for filename in os.listdir(directory):
        if filename.endswith(".wav"):
            path = os.path.join(directory, filename)
            audio = AudioSegment.from_wav(path)
            
            # Transcribe audio
            model = whisper.load_model("small.en")
            result = model.transcribe(path)
            transcript = result["text"][1:]
            
            # Compute metrics
            words, time, wpm = speechrate(transcript, path)
            num_repetitions = repetitions(transcript)
            filler_count, filler_times = filler_pauses(transcript)
            
            # Calculate percentages
            percentage_repeated = (num_repetitions / len(words)) * 100
            
            # Store results
            results[dir_key]["paths"].append(filename)
            results[dir_key]["speech_rates"].append(wpm)
            results[dir_key]["repetition_percentages"].append(percentage_repeated)
            results[dir_key]["filler_counts"].append(filler_count)

# Process both directories
process_directory(directory_1, "dir1")
#process_directory(directory_2, "dir2")

# Visualization and saving as PNG
bar_width = 0.35
index = np.arange(len(results["dir1"]["paths"]))

# Save directory for the PNGs
save_directory = "path_to_save_directory"
os.makedirs(save_directory, exist_ok=True)

# Subplot 1: Speech Rate (WPM)
plt.figure(figsize=(14, 8))
plt.bar(index, results["dir1"]["speech_rates"], bar_width, label='Directory 1', color='blue')
plt.bar(index + bar_width, results["dir2"]["speech_rates"], bar_width, label='Directory 2', color='lightblue')
plt.ylabel('Words Per Minute (WPM)')
plt.title('Speech Rate Comparison')
plt.xticks(index + bar_width / 2, results["dir1"]["paths"], rotation=90)
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(save_directory, 'speech_rate_comparison.png'))
plt.close()

# Subplot 2: Repetitions Percentage
plt.figure(figsize=(14, 8))
plt.bar(index, results["dir1"]["repetition_percentages"], bar_width, label='Directory 1', color='green')
plt.bar(index + bar_width, results["dir2"]["repetition_percentages"], bar_width, label='Directory 2', color='lightgreen')
plt.ylabel('Percentage (%)')
plt.title('Repeated Words Percentage Comparison')
plt.xticks(index + bar_width / 2, results["dir1"]["paths"], rotation=90)
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(save_directory, 'repetition_percentage_comparison.png'))
plt.close()

# Subplot 3: Filler Words Count
plt.figure(figsize=(14, 8))
plt.bar(index, results["dir1"]["filler_counts"], bar_width, label='Directory 1', color='red')
plt.bar(index + bar_width, results["dir2"]["filler_counts"], bar_width, label='Directory 2', color='lightcoral')
plt.ylabel('Count')
plt.title('Filler Words Count Comparison')
plt.xticks(index + bar_width / 2, results["dir1"]["paths"], rotation=90)
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(save_directory, 'filler_words_count_comparison.png'))
plt.close()

print(f"Visualizations saved in {save_directory}")
