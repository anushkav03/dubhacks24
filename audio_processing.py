import os
from pydub import AudioSegment


'''
input_file: path
output_file: path 
'''
def process_audio_file(input_file, output_file, target_sample_rate=16000):
    audio = AudioSegment.from_wav(input_file)
    if audio.channels != 1: # channel 1 (mono) is used for processing 
        audio = audio.set_channels(1)
    audio = audio.set_frame_rate(target_sample_rate)
    audio.export(output_file, format="wav")


# input_file = 'Stuttering Sample.wav'
# output_file = 'processed_stuttering_sample.wav'

# process_audio_file(input_file, output_file, target_sample_rate=16000)