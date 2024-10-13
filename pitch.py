import parselmouth
import numpy as np
import matplotlib.pyplot as plt

# Load the audio file
sound = parselmouth.Sound("processed_stuttering_sample.wav")

# Extract pitch information (time step of 0.01 s by default)
pitch = sound.to_pitch()

# Extract pitch values and corresponding time stamps
pitch_values = pitch.selected_array['frequency']  # Pitch values in Hertz
time_values = pitch.xs()  # Time stamps

# Filter out undefined pitch values (i.e., unvoiced regions)
pitch_values = np.where(pitch_values == 0, np.nan, pitch_values)

# Plotting the pitch contour
plt.plot(time_values, pitch_values, label="Pitch (Hz)")
plt.xlabel("Time (s)")
plt.ylabel("Pitch (Hz)")
plt.title("Pitch Contour")
plt.legend()
plt.show()
