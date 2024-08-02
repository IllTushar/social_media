from removebg import RemoveBg
import os
import time


def remove_background_with_removebg(image_path, output_path, api_key):
    # Initialize RemoveBg instance with your API key
    removebg = RemoveBg(api_key, "error.log")

    # Remove the background from the image
    removebg.remove_background_from_img_file(image_path)

    # Wait for a short period to ensure the output file is saved
    time.sleep(5)  # Sleep for 5 seconds

    # Check the directory of the input image
    input_dir = os.path.dirname(image_path)

    # List files in the directory to find the output file
    files = os.listdir(input_dir)
    print(f"Files in directory: {files}")

    # Look for files with '_no_bg' suffix
    output_image_path = None
    for file in files:
        if file.endswith('_no_bg.png'):
            output_image_path = os.path.join(input_dir, file)
            break

    # Check if the output image exists and rename it to the specified output path
    if output_image_path and os.path.exists(output_image_path):
        os.rename(output_image_path, output_path)
    else:
        print(f"Expected output file not found: {output_image_path}")


if __name__ == '__main__':
    # Example usage
    api_key = "87a4tgufMMc7Cyb4WTxdGYwa"
    remove_background_with_removebg(r'C:\Users\gtush\Desktop\HospitalList\aceclofenac-100-mg-paracetamol-325-mg-10-tablet-1_1.png',
                                    r'C:\Users\gtush\Desktop\HospitalList\output_image.png', api_key)
