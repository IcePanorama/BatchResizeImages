import os
import re
import sys

from PIL import Image


def resize_images(input_folder, output_folder, size):
    pattern = r"-\d+x\d+"
    os.makedirs(output_folder, exist_ok=True)

    for subdir in subdirs:
        input_subdir = os.path.join(input_folder, subdir)
        output_subdir = os.path.join(output_folder, subdir)
        os.makedirs(output_subdir, exist_ok=True)

        images = os.listdir(input_subdir)

        for image_name in images:
            image_path = os.path.join(input_subdir, image_name)
            img = Image.open(image_path)

            resized_img = img.resize((size, size), Image.NEAREST)

            filename, extension = os.path.splitext(image_name)
            filename = re.split(pattern, filename)[0]
            new_filename = f"{filename}-{size}x{size}{extension}"

            output_path = os.path.join(output_subdir, new_filename)
            resized_img.save(output_path)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Invalid usage. Please pass in the path of the input dir as a string.")
        exit(1)

    input_dir = sys.argv[1]
    output_dirs = {
        '128x128': ('./128x128', 128),
        '64x64': ('./64x64', 64),
        '32x32': ('./32x32', 32)
    }

    subdirs = next(os.walk(input_dir))[1]

    for size in output_dirs.keys():
        if input_dir in output_dirs.keys() and \
                output_dirs[input_dir][1] <= output_dirs[size][1]:
            continue

        resize_images(
            input_dir, output_dirs[size][0], output_dirs[size][1])

    print("Images resized and saved successfully.")
