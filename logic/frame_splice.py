import cv2
import os
os.chdir('C:/Users/dalto/OneDrive/Pictures/Documents/Projects/Coding Projects/Frame Rate/video/')

def extract_frames(video_path, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    cap = cv2.VideoCapture(video_path)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_filename = os.path.join(output_dir, f"frame_{frame_count}.jpg")
        cv2.imwrite(frame_filename, frame)
        frame_count += 1

    cap.release()
    print(f"Extracted {frame_count} frames at {fps} fps.")

output_dir = 'C:/Users/dalto/OneDrive/Pictures/Documents/Projects/Coding Projects/Frame Rate/photo/dl_test/'
vid_path = 'C:/Users/dalto/OneDrive/Pictures/Documents/Projects/Coding Projects/Frame Rate/video/dl_test.mp4'

extract_frames(video_path=vid_path, output_dir=output_dir)