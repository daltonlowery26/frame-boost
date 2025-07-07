import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
from PIL import Image
import os

interpolator = hub.load("https://tfhub.dev/google/film/1")

def load_image(image_path):
    try:
        img = Image.open(image_path).convert('RGB')
        img = np.array(img).astype(np.float32) / 255.0
        return img
    except FileNotFoundError:
        print(f"Image Not Found: {image_path}")
        return None

def save_image(image_array, output_path):
    img = Image.fromarray((image_array * 255.0).astype(np.uint8))
    img.save(output_path)


def interpolate_frames(frame1_path, frame2_path, output_dir, base_name, frame_num):
    frame1_np = load_image(frame1_path)
    frame2_np = load_image(frame2_path)

    if frame1_np is None or frame2_np is None:
        return

    frame1_batch = np.expand_dims(frame1_np, axis=0)
    frame2_batch = np.expand_dims(frame2_np, axis=0)

    time_tensor = np.full(shape=(1, 1), fill_value=0.5, dtype=np.float32)

    # start, end when to split
    input_data = {
        'x0': frame1_batch,
        'x1': frame2_batch,
        'time': time_tensor
    }

    interpolated_result = interpolator(input_data)
    interpolated_frame_np = interpolated_result['image'][0].numpy()

    interpolated_frame_name = f"{base_name}_{frame_num}.png"
    interpolated_frame_path = os.path.join(output_dir, interpolated_frame_name)

    save_image(interpolated_frame_np, interpolated_frame_path)
    print(f"Generated: {interpolated_frame_path}")


def process_frames(input_dir, output_dir):
  
    # Filter files to ensure they have the expected format 'name_number.extension'
    valid_files = [f for f in os.listdir(input_dir) if '_' in f and len(f.split('_')) > 1 and os.path.splitext(f.split('_')[1])[0].isdigit()]
    files = sorted(valid_files, key=lambda x: int(os.path.splitext(x.split('_')[1])[0]))

    if not files:
        print(f"No valid image files found in {input_dir}")
        return


    output_frame_counter = 0
    for i in range(len(files) - 1):
        frame1_name = files[i]
        frame2_name = files[i+1]
        frame1_path = os.path.join(input_dir, frame1_name)
        
        # og frame save
        original_frame_np = load_image(frame1_path)
        if original_frame_np is not None:
            new_frame_name = f"frame_{output_frame_counter}.jpg"
            save_image(original_frame_np, os.path.join(output_dir, new_frame_name))
            print(f"Saved original frame: {os.path.join(output_dir, new_frame_name)}")
            output_frame_counter += 1

        # middle frame save
        interpolate_frames(
            frame1_path=os.path.join(input_dir, frame1_name),
            frame2_path=os.path.join(input_dir, frame2_name),
            output_dir=output_dir,
            base_name='frame',
            frame_num=output_frame_counter
        )
        output_frame_counter += 1

    # Save the last original frame
    if files:
        last_frame_path = os.path.join(input_dir, files[-1])
        last_frame_np = load_image(last_frame_path)
        if last_frame_np is not None:
            new_frame_name = f"frame_{output_frame_counter}.jpg"
            save_image(last_frame_np, os.path.join(output_dir, new_frame_name))
            print(f"Saved last original frame: {os.path.join(output_dir, new_frame_name)}")


def process_pitch_folders(base_directory, output):
    for player_name in os.listdir(base_directory):
        player_path = os.path.join(base_directory, player_name)
        
        # ensure player path exists
        if not os.path.isdir(player_path):
            continue
        
        print(f"Processing Player: {player_name}")


        for pitch_name in os.listdir(player_path):
            pitch_path = os.path.join(player_path, pitch_name)
            print(pitch_path)
            if not os.path.isdir(pitch_path):
                continue
            
            print(f"  -> Processing Pitch: {pitch_name}")

            # 30fps -> 60 fps
            output_path_1 = os.path.join(pitch_path, '1')
            os.makedirs(output_path_1, exist_ok=True)
            process_frames(input_dir=pitch_path, output_dir=output_path_1)

            # 60 fps -> 120fps 
            output_path_2 = os.path.join(output_path_1, '2')
            final_output_dir = os.path.join(output, player_name, pitch_name)
            os.makedirs(final_output_dir, exist_ok=True)
            process_frames(input_dir=output_path_1, output_dir=final_output_dir)



if __name__ == "__main__":

    input_directory = '/content/drive/MyDrive/frame_rate'
    output_directory = '/content/drive/MyDrive/boosted'

    process_pitch_folders(base_directory=input_directory, output=output_directory)
    print("Processing complete.")