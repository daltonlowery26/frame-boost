import cv2
import os
import re

def sort_key(f): # sort frames into correct order
    match = re.search(r'(\d+)', os.path.basename(f))
    return int(match.group(1)) if match else -1

def create_video_from_frames(frames_dir, og_video_path, output_video_path):
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_video_path), exist_ok=True)

    # Get list of frame files
    try:
        frame_files = [
            os.path.join(frames_dir, f)
            for f in os.listdir(frames_dir)
            if f.lower().endswith(('.png', '.jpg', '.jpeg'))
        ]
    except FileNotFoundError:
        print(f"Skipping: Frames directory not found at {frames_dir}")
        return

    if not frame_files:
        print(f"Skipping: No image frames found in {frames_dir}")
        return

    # Sort frames numerically
    frame_files.sort(key=sort_key)
    num_frames = len(frame_files)

    # Get original video properties to calculate duration
    cap = cv2.VideoCapture(og_video_path)
    if not cap.isOpened():
        print(f"Skipping: Cannot open original video {og_video_path}")
        return
    fps_og = cap.get(cv2.CAP_PROP_FPS)
    frame_count_og = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count_og / fps_og if fps_og > 0 else 0
    cap.release()

    if duration == 0:
        print(f"Skipping: Could not determine duration for {og_video_path}")
        return

    # Calculate new FPS and get frame dimensions
    new_fps = num_frames / duration
    first_frame = cv2.imread(frame_files[0])
    height, width, _ = first_frame.shape

    # Setup video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_path, fourcc, new_fps, (width, height))

    print(f"Processing {frames_dir} -> {output_video_path} at {new_fps:.2f} FPS")

    # Write frames to video
    for file in frame_files:
        img = cv2.imread(file)
        out.write(img)

    out.release()
    print("Done.")


if __name__ == "__main__":
    boost_base_dir = 'C:/Users/dalto/OneDrive/Pictures/Documents/Projects/Coding Projects/Frame Rate/photo/boost'
    origin_base_dir = 'C:/Users/dalto/OneDrive/Pictures/Documents/Projects/Coding Projects/Frame Rate/video/origin'
    output_base_dir = 'C:/Users/dalto/OneDrive/Pictures/Documents/Projects/Coding Projects/Frame Rate/video/frame_boost'

    # Loop through each pitcher's folder
    for pitcher_name in os.listdir(boost_base_dir):
        pitcher_dir = os.path.join(boost_base_dir, pitcher_name)
        if not os.path.isdir(pitcher_dir):
            continue

        # Loop through each pitch folder for the current pitcher
        for pitch_name in os.listdir(pitcher_dir):
            frames_dir = os.path.join(pitcher_dir, pitch_name)
            if not os.path.isdir(frames_dir):
                continue

            # Construct paths for original and output videos
            og_video_path = os.path.join(origin_base_dir, pitcher_name, f"{pitch_name}.mp4")
            output_video_path = os.path.join(output_base_dir, pitcher_name, f"{pitch_name}_b.mp4")

            # Process the frames for this pitch
            create_video_from_frames(frames_dir, og_video_path, output_video_path)