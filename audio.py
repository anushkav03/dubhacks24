from pause_feature_extraction import *
from pause_feature_comparison import *
from audio_processing import *
import matplotlib.pyplot as plt



stuttering_sample_input_path = "/Users/adityaiyer/Downloads/test.wav"
processed_stuttering_output_path = "processed_stuttering_sample.wav"

normal_sample_input_path = "ttsmaker-file-2024-10-12-19-47-57.wav"
processed_normal_output_path = "processed_output_sample.wav"

process_audio_file(stuttering_sample_input_path, processed_stuttering_output_path, target_sample_rate=16000)
process_audio_file(normal_sample_input_path, processed_normal_output_path, target_sample_rate=16000)

imped_pause_durations = pause_detection(processed_stuttering_output_path)
imped_features= pause_feature_extraction(imped_pause_durations)

normal_pause_durations = pause_detection(processed_normal_output_path)
normal_features= pause_feature_extraction(normal_pause_durations)


imped_pause_ts = pause_comparison_time_series(imped_pause_durations)
normal_pause_ts = pause_comparison_time_series(normal_pause_durations)

plt.plot(normal_pause_ts, label="Regular Speech (Smoothed Pauses)", color='blue')
plt.plot(imped_pause_ts, label="Impaired Speech (Smoothed Pauses)", color='red')
plt.xlabel('Time')
plt.ylabel('Pause Duration (s)')
plt.legend()
plt.title('Comparison of Pause Durations Over Time')
plt.show()

dtw_comparison_score = dtw(imped_pause_durations, normal_pause_durations)
print(dtw_comparison_score)