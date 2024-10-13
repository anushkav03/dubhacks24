import shutil
import os

# Specify the source folder and destination folder
source_folder = '/private/tmp'
destination_folder = "llm-audio"

# Get a list of all files in the source folder
files = os.listdir(source_folder)

# Loop through all the files and move only .wav files to the destination folder
for file_name in files:
    # Check if the file has a .wav extension
    if file_name.lower().endswith('.mp3'):
        # Create the full file path
        source_file = os.path.join(source_folder, file_name)
        destination_file = os.path.join(destination_folder, file_name)
        
        # Move the file
        shutil.move(source_file, destination_file)

print("MP3 files moved successfully!")


from pydub import AudioSegment
import os

def convert_mp3_to_wav(directory, delete_mp3=False):
    # List all files in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".mp3"):
            # Full path to the mp3 file
            mp3_path = os.path.join(directory, filename)
            # Create the path for the wav file
            wav_path = os.path.join(directory, os.path.splitext(filename)[0] + '.wav')

            # Load mp3 and export as wav
            audio = AudioSegment.from_mp3(mp3_path)
            audio.export(wav_path, format="wav")
            print(f"Converted {mp3_path} to {wav_path}")

            # Optionally delete the original MP3 file
            if delete_mp3:
                os.remove(mp3_path)
                print(f"Deleted original MP3 file: {mp3_path}")

# Set the directory path
directory = "llm-audio"
convert_mp3_to_wav(directory, delete_mp3=True)  # Set delete_mp3=True to remove MP3 files

