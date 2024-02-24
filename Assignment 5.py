import os
from PIL import Image
from prettytable import PrettyTable

def get_image_info(file_path):
    """Extracts image information using PIL."""
    try:
        with Image.open(file_path) as img:
            return os.path.basename(file_path), img.format, img.size[0], img.size[1], img.mode
    except IOError:
        return None

def main():
    directory_path = input("Enter the directory path containing image files: ")
    if not os.path.isdir(directory_path):
        print("Provided path is not a directory.")
        return

    # Initialize PrettyTable
    table = PrettyTable(['File', 'Ext', 'Format', 'Width', 'Height', 'Mode'])

    # Iterate through each file in the directory
    for filename in os.listdir(directory_path):
        full_path = os.path.join(directory_path, filename)
        if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif')):
            info = get_image_info(full_path)
            if info:
                file_name, format, width, height, mode = info
                ext = os.path.splitext(filename)[1].upper()
                table.add_row([file_name, ext, format, width, height, mode])

    print(table)

if __name__ == "__main__":
    main()
