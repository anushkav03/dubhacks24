# import shutil
# import os

# # Specify the source folder and destination folder
# source_folder = '/Users/mishtu/Downloads'
# destination_folder = "llm-audio"

# # Get a list of all files in the source folder
# files = os.listdir(source_folder)

# # Loop through all the files and move only .wav files to the destination folder
# for file_name in files:
#     # Check if the file has a .wav extension
#     if file_name.lower().endswith('.mp3'):
#         # Create the full file path
#         source_file = os.path.join(source_folder, file_name)
#         destination_file = os.path.join(destination_folder, file_name)
        
#         # Move the file
#         shutil.move(source_file, destination_file)

# print("WAV files moved successfully!")
