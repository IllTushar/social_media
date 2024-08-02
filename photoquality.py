import os
import cv2
import numpy as np


def assess_image_quality(image_path):
    # Check if the file exists
    if not os.path.isfile(image_path):
        return "File not found."

    # Try to read the image
    image = cv2.imread(image_path)
    if image is None:
        return "Failed to load image."

    # Initialize quality report
    quality_report = {}

    # Check resolution
    height, width = image.shape[:2]
    resolution = f"{width}x{height}"
    quality_report['Resolution'] = resolution

    # Define minimum resolution for "perfect" quality
    min_resolution_width = 1920
    min_resolution_height = 1080

    if width >= min_resolution_width and height >= min_resolution_height:
        quality_report['Resolution Quality'] = 'Perfect'
    else:
        quality_report['Resolution Quality'] = 'Not Perfect'

    # Check sharpness (Laplacian variance)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    sharpness = cv2.Laplacian(gray, cv2.CV_64F).var()
    quality_report['Sharpness Score'] = sharpness

    # Define a minimum sharpness score for "perfect" quality
    min_sharpness_score = 100  # This is an example threshold; adjust as needed

    if sharpness >= min_sharpness_score:
        quality_report['Sharpness Quality'] = 'Perfect'
    else:
        quality_report['Sharpness Quality'] = 'Not Perfect'

    # Check file size
    file_size = os.path.getsize(image_path)
    quality_report['File Size (bytes)'] = file_size

    # Define a minimum file size for "perfect" quality (example: 500 KB)
    min_file_size = 500 * 1024  # 500 KB

    if file_size >= min_file_size:
        quality_report['File Size Quality'] = 'Perfect'
    else:
        quality_report['File Size Quality'] = 'Not Perfect'

    # Check noise (optional step)
    denoised_image = cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 21)
    noise_level = np.mean(cv2.absdiff(image, denoised_image))
    quality_report['Noise Level'] = noise_level

    # Define a maximum noise level for "perfect" quality
    max_noise_level = 10  # This is an example threshold; adjust as needed

    if noise_level <= max_noise_level:
        quality_report['Noise Quality'] = 'Perfect'
    else:
        quality_report['Noise Quality'] = 'Not Perfect'

    # Determine final quality
    if all(value == 'Perfect' for key, value in quality_report.items() if 'Quality' in key):
        quality_report['Final Quality'] = 'Perfect'
    else:
        quality_report['Final Quality'] = 'Not Perfect'

    return quality_report


if __name__ == '__main__':
    # Define the path to the image file
    image_path = r'C:\Users\gtush\Pictures\Screenshots\Screenshot (1).png'

    quality_report = assess_image_quality(image_path)
    print(quality_report)
