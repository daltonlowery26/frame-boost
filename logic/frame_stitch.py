import cv2
import os
import re

frames_dir = 'C:/Users/dalto/OneDrive/Pictures/Documents/Projects/Coding Projects/Frame Rate/photo/dl_test_inter/'
og_video = 'C:/Users/dalto/OneDrive/Pictures/Documents/Projects/Coding Projects/Frame Rate/video/origin/dl_test.mp4'
output_video = 'c:/Users/dalto/OneDrive/Pictures/Documents/Projects/Coding Projects/Frame Rate/video/frame_boost/dl_test.mp4'

# file list
frame_files = [
    os.path.join(frames_dir, f)
    for f in os.listdir(frames_dir)
    if f.lower().endswith(('.png', '.jpg', '.jpeg'))
]

# frame num
num_frames = len(frame_files)

# get original video time for fps calc
cap = cv2.VideoCapture(og_video)
if not cap.isOpened():
    raise IOError(f"Cannot open video file: {og_video}")
fps_og = cap.get(cv2.CAP_PROP_FPS)
frame_count_og = cap.get(cv2.CAP_PROP_FRAME_COUNT)
duration = frame_count_og / fps_og if fps_og > 0 else 1
cap.release()

# fps
fps = num_frames / duration if duration > 0 else 30

# sort properly
def sort_key(f):
    match = re.search(r'(\d+)', os.path.basename(f))
    return int(match.group(1)) if match else -1

# key to sort
frame_files.sort(key=sort_key)

# frame read
frame = cv2.imread(frame_files[0])
height, width, layers = frame.shape

# writer object and output
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_video, fourcc, fps, (width, height))

# loop through images
for file in frame_files:
    img = cv2.imread(file)
    out.write(img)

out.release()