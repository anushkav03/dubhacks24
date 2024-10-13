from pydub import AudioSegment
from fastdtw import fastdtw
import librosa
import numpy as np
import os


# time series analysis
def pause_comparison_time_series(pause_duration_lst, window_size = 5):
    return np.convolve(pause_duration_lst, np.ones(window_size)/window_size, mode='valid')


# dyanmic time warping
def dtw(regular_lst, impediment_lst):
    pause_durations_regular = np.array(regular_lst)
    pause_durations_impaired = np.array(impediment_lst)

    # Ensure both arrays are 1-D
    pause_durations_regular = pause_durations_regular.reshape(-1)
    pause_durations_impaired = pause_durations_impaired.reshape(-1)


    # Compute DTW distance
    distance, path = fastdtw(pause_durations_regular, pause_durations_impaired)
    print(f"DTW distance: {distance}")
    return distance


