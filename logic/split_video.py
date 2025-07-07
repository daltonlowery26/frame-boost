import os
import pandas as pd
import ffmpeg
from pathlib import Path

ffmpeg_exe = "C:/ffmpeg/bin/ffmpeg.exe"

# Define the paths
videos_folder = Path("C:/Users/dalto/OneDrive/Pictures/Documents/Projects/Coding Projects/Frame Rate/video/frame_boost/")
output_folder = Path("C:/Users/dalto/OneDrive/Pictures/Documents/Projects/Coding Projects/Frame Rate/video/splits/")
timing_csv_path = Path("C:/Users/dalto/OneDrive/Pictures/Documents/Projects/Coding Projects/Frame Rate/timings.csv")

timing_df = pd.read_csv(timing_csv_path)


# Iterate over each row in the DataFrame
for index, row in timing_df.iterrows():
    video_name = row['name']
    blackout_time = row['blackout_point']
    swing_time = row['swing_time']
    
    input_video_path = os.path.join(videos_folder, video_name)
    
    # Create the new filename with swing_time
    name_part, ext_part = os.path.splitext(video_name)
    new_filename = f"{name_part}_{swing_time}{ext_part}"
    
    output_video_path = os.path.join(output_folder, new_filename)
    
    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_video_path), exist_ok=True)
    
    if not os.path.exists(input_video_path):
        print(f"Skipping {video_name}: File not found.")
        continue
        
    
    print(f"Processing {video_name}...")
        
    # Convert blackout_time from ms to seconds for ffmpeg
    blackout_time_seconds = blackout_time / 1000.0
    
    # Use ffmpeg-python to trim the video
    try:
        (
            ffmpeg
            .input(input_video_path)
            .trim(end=blackout_time_seconds)
            .output(output_video_path, vcodec='libx264', acodec='aac')
            .overwrite_output()
            .run(cmd=ffmpeg_exe, capture_stdout=True, capture_stderr=True)
        )
    except ffmpeg.Error as e:
        print('stdout:', e.stdout.decode('utf8'))
        print('stderr:', e.stderr.decode('utf8'))
        raise e
        
    print(f"Finished processing {video_name}. Saved to {output_video_path}")


print("All videos have been processed.")
