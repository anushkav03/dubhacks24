from pydub import AudioSegment
# # from fastdtw import fastdtw
# from dtw import *
import librosa
import numpy as np
import os


def pause_detection(audio_file, sr=22050, frame_length=2048, hop_length=512, threshold=0.02, min_pause_duration=0.2):
    # Load the audio file
    y, sr = librosa.load(audio_file, sr=sr)

    # Compute the energy of each frame
    energy = np.array([
        np.sum(np.abs(y[i:i+frame_length])**2)
        for i in range(0, len(y), hop_length)
    ])
    
    # Normalize energy
    energy_normalized = energy / np.max(energy)

    # Find frames where energy is below the threshold
    pause_frames = np.where(energy_normalized < threshold)[0]

    frame_duration = hop_length / sr
    pause_durations = []
    pause_start = None
    
    # Minimum number of consecutive frames below threshold to qualify as a pause
    min_pause_frames = int(min_pause_duration / frame_duration)

    # Iterate over the pause frames and calculate the duration of each pause
    for i in range(len(pause_frames) - 1):
        # Check if consecutive pause frames are detected
        if pause_start is None:
            pause_start = pause_frames[i]

        # If the next pause frame is not consecutive, calculate the pause length
        if pause_frames[i + 1] - pause_frames[i] > 1:
            pause_end = pause_frames[i]
            pause_length = (pause_end - pause_start + 1) * frame_duration
            
            if (pause_end - pause_start + 1) >= min_pause_frames:
                pause_durations.append(pause_length)
            
            pause_start = None

    # If there was a pause at the end of the audio
    if pause_start is not None:
        pause_end = pause_frames[-1]
        pause_length = (pause_end - pause_start + 1) * frame_duration
        if (pause_end - pause_start + 1) >= min_pause_frames:
            pause_durations.append(pause_length)

    print(f'pause_durations: {pause_durations}')
    return pause_durations



def pause_feature_extraction(pause_durations):
    total_pause_duration = np.sum(pause_durations)
    pause_frequency = len(pause_durations)
    average_pause_length = np.mean(pause_durations) if pause_frequency > 0 else 0
    max_pause_length = np.max(pause_durations) if pause_frequency > 0 else 0
    pause_distribution = pause_durations  # Raw list for analyzing distribution if needed

    features = {
        'Total Pause Duration (s)': total_pause_duration,
        'Pause Frequency': pause_frequency,
        'Average Pause Length (s)': average_pause_length,
        'Max Pause Length (s)': max_pause_length,
        'Pause Distribution': pause_distribution
    }

    print(f'features{features}')
    
    return features


pause_durations = pause_detection('processed_stuttering_sample.wav')
pause_feature_extraction(pause_durations)