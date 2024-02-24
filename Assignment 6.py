import os
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from prettytable import PrettyTable

def extract_gps_dictionary(filename):
    try:
        with Image.open(filename) as img:
            exif_data = img._getexif()
    except IOError as e:
        print(f"Error opening {filename}: {e}")
        return None, None

    gps_data = {}
    basic_exif_data = {}

    if exif_data:
        for tag_id, value in exif_data.items():
            tag_name = TAGS.get(tag_id, tag_id)
            if tag_name == "GPSInfo":
                for key, val in value.items():
                    sub_tag = GPSTAGS.get(key, key)
                    gps_data[sub_tag] = val
            elif tag_name in ["DateTimeOriginal", "Make", "Model"]:
                basic_exif_data[tag_name] = value

    return gps_data, basic_exif_data

def convert_to_decimal_degrees(value, ref):
    degrees, minutes, seconds = value
    decimal_degrees = degrees + (minutes / 60.0) + (seconds / 3600.0)
    if ref in ['S', 'W']:
        decimal_degrees *= -1
    return decimal_degrees

def process_images(directory):
    results = []
    for filename in sorted(os.listdir(directory)):
        if filename.lower().endswith('.jpg'):
            full_path = os.path.join(directory, filename)
            print(f"Processing: {filename}")
            gps_data, exif_data = extract_gps_dictionary(full_path)

            datetime_original = exif_data.get("DateTimeOriginal", "NA")
            make = exif_data.get("Make", "NA")
            model = exif_data.get("Model", "NA")

            if gps_data and 'GPSLatitude' in gps_data and 'GPSLongitude' in gps_data:
                lat = convert_to_decimal_degrees(gps_data['GPSLatitude'], gps_data['GPSLatitudeRef'])
                lon = convert_to_decimal_degrees(gps_data['GPSLongitude'], gps_data['GPSLongitudeRef'])
                results.append([filename, f"{lat:.6f}", f"{lon:.6f}", datetime_original, make, model])
            else:
                print(f"No GPS Data for {filename}")
                results.append([filename, "No GPS Data", "No GPS Data", datetime_original, make, model])
        else:
            print(f"Skipped: {filename} (not a .jpg file)")

    return results

def generate_report(results):
    table = PrettyTable(['File-Name', 'Lat', 'Lon', 'TimeStamp', 'Make', 'Model'])
    for row in results:
        table.add_row(row)
    print(table)

if __name__ == "__main__":
    directory = input("Enter the path to the directory containing JPEG files: ")
    if os.path.isdir(directory):
        results = process_images(directory)
        generate_report(results)
    else:
        print("The specified path does not exist or is not a directory.")
