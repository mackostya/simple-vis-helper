## The code stimulated by the

from PIL import Image
import os


def create_gif(input_folder, output_gif, duration=500):
    """
    Reads images from the input_folder, sorts them alphabetically, and creates a GIF animation.

    :param input_folder: Directory containing image files
    :param output_gif: Path to save the output GIF
    :param duration: Duration for each frame in milliseconds (default 500ms)
    """
    # Get list of image files sorted alphabetically
    images = sorted([f for f in os.listdir(input_folder) if f.lower().endswith(("png", "jpg", "jpeg", "bmp", "gif"))])

    if not images:
        print("No image files found in the specified directory.")
        return

    # Load images
    image_list = [Image.open(os.path.join(input_folder, img)) for img in images]

    # Save as GIF
    image_list[0].save(output_gif, save_all=True, append_images=image_list[1:], duration=duration, loop=0)
    print(f"GIF saved as {output_gif}")


if __name__ == "__main__":
    input_directory = r"your_path_to_folder_with_pngs"
    output_file = "output.gif"
    frame_duration = 50
    create_gif(input_directory, output_file, frame_duration)
