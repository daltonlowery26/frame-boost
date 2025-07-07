import ffmpeg
from pathlib import Path

# conversion extension
ffmpeg_exe = "C:/ffmpeg/bin/ffmpeg.exe"

def convert_to_h264(input_file, output_file):
    try:
        (
            ffmpeg
            .input(input_file)
            .filter('scale', w=-2, h='trunc(ih/2)*2')
            .output(output_file, vcodec='libx264', acodec='aac')
            .run(cmd=ffmpeg_exe, overwrite_output=True, capture_stderr=True)
        )
        print(f"Successfully converted {input_file} to {output_file}")
    except ffmpeg.Error as e:
        print(f"Error converting {input_file}:")
        print(e.stderr.decode())


if __name__ == "__main__":
    input_folder = Path("C:/Users/dalto/OneDrive/Pictures/Documents/Projects/Coding Projects/Frame Rate/video/frame_boost/")
    video_extensions = ['.mp4']

    for file_path in input_folder.iterdir():
        if file_path.stem.endswith('_c'):
            continue

        output_file = file_path.with_name(f"{file_path.stem}_c{file_path.suffix}")
            
        print(f"Found video: {file_path.name}. Starting conversion...")
        convert_to_h264(str(file_path), str(output_file))