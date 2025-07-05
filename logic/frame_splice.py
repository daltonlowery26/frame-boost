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


video_root = 'C:/Users/dalto/OneDrive/Pictures/Documents/Projects/Coding Projects/Frame Rate/video/origin/'
photo_root = 'C:/Users/dalto/OneDrive/Pictures/Documents/Projects/Coding Projects/Frame Rate/photo/splice/'
video_extensions = ('.mp4')


if not os.path.exists(photo_root):
    os.makedirs(photo_root)

# loop through video directory
for dirpath, _, filenames in os.walk(video_root):
    for filename in filenames:
        if filename.lower().endswith(video_extensions):
            video_path = os.path.join(dirpath, filename)

            relative_dir = os.path.relpath(dirpath, video_root)
            video_name_without_ext = os.path.splitext(filename)[0]
            output_dir = os.path.join(photo_root, relative_dir, video_name_without_ext)

            print(f"Processing '{video_path}'...")
            extract_frames(video_path=video_path, output_dir=output_dir)


print("All videos processed.")