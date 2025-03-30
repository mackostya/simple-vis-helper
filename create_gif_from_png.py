import os
import re
from PIL import Image


def natural_sort_key(text):
    """
    Breaks the text into alphanumeric chunks, converting digits to integers
    to ensure numeric sorting (e.g., 2 < 10, not '10' < '2').
    """
    return [int(chunk) if chunk.isdigit() else chunk.lower() for chunk in re.split(r"(\d+)", text)]


def create_gif(input_folder, output_gif, duration=500):
    """
    Reads images from the input_folder, sorts them 'naturally', and creates a GIF.

    :param input_folder: Directory containing image files
    :param output_gif: Path to save the output GIF
    :param duration: Duration for each frame in milliseconds (default 500ms)
    """
    # Get list of image files that end with PNG/JPG/JPEG/BMP/GIF
    images = [f for f in os.listdir(input_folder) if f.lower().endswith(("png", "jpg", "jpeg", "bmp", "gif"))]

    # Sort images in "natural" order (e.g. 1, 2, 10 rather than 1, 10, 2)
    images.sort(key=natural_sort_key)

    if not images:
        print("No image files found in the specified directory.")
        return

    # Load images
    image_list = [Image.open(os.path.join(input_folder, img)) for img in images]

    # Create duration list
    durations = [duration] * len(image_list)
    # Make the last frame appear longer, if desired
    durations[-1] = 2000  # 2 seconds for the last frame

    # Save as GIF
    image_list[0].save(output_gif, save_all=True, append_images=image_list[1:], duration=durations, loop=0)
    print(f"GIF saved as {output_gif}")


if __name__ == "__main__":
    input_directory = r"your_path_to_folder_with_pngs"
    output_file = "output.gif"
    frame_duration = 50
    create_gif(input_directory, output_file, frame_duration)
