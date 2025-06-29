import ffmpeg

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
        print("Error during conversion:")
        print(e.stderr.decode())

convert_to_h264('C:/Users/dalto/OneDrive/Pictures/Documents/Projects/Coding Projects/Frame Rate/video/frame_boot/dl_test.mp4', 'C:/Users/dalto/OneDrive/Pictures/Documents/Projects/Coding Projects/Frame Rate/video/frame_boot/dl_test.mp4')