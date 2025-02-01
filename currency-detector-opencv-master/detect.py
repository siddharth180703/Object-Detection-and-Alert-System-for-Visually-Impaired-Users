import cv2
import numpy as np
import os
import requests
import pygame  # To play audio
from matplotlib import pyplot as plt

# Initialize pygame mixer for audio playback
pygame.mixer.init()

# Phone camera URL (Update with your IP)
photo_url = "http://192.168.19.147:8080/photo.jpg"  # Replace with correct IP
print(photo_url)

# Folder to save images
image_path = "files/live_capture.jpg"

# ORB feature detector
orb = cv2.ORB_create(nfeatures=1000)

# Directory containing training images
training_dir = "files/"

# Initialize an empty dictionary for storing denomination images
denomination_images = {}

# Load all training images dynamically
for file in os.listdir(training_dir):
    if file.endswith(".jpg"):
        # Extract denomination from filename (Ensure it’s only the numeric part)
        denom = file.split('_')[0].strip()  # Strip removes unwanted spaces

        if denom.isdigit():  # Ensure only valid numbers are considered
            if denom not in denomination_images:
                denomination_images[denom] = []
            denomination_images[denom].append(os.path.join(training_dir, file))

print("Loaded denominations:", denomination_images.keys())  # Debugging statement

# Function to download image from phone camera
def download_latest_photo():
    try:
        response = requests.get(photo_url, stream=True, timeout=5)
        if response.status_code == 200:
            with open(image_path, 'wb') as file:
                file.write(response.content)
            return True  # Image successfully downloaded
    except Exception as e:
        print(f"Error downloading image: {e}")
    return False

# Function to detect currency denomination
def detect_currency():
    global image_path

    # Load test image
    test_img = cv2.imread(image_path)
    if test_img is None:
        print("Failed to load image")
        return

    # Extract keypoints and descriptors
    kp1, des1 = orb.detectAndCompute(test_img, None)
    if des1 is None:
        print("No keypoints detected in test image")
        return

    bf = cv2.BFMatcher()

    for denom, image_paths in denomination_images.items():
        for img_path in image_paths:
            train_img = cv2.imread(img_path)
            kp2, des2 = orb.detectAndCompute(train_img, None)

            if des2 is None:
                continue  # Skip if no keypoints found

            # Brute Force Matcher
            all_matches = bf.knnMatch(des1, des2, k=2)

            # Apply ratio test
            good_matches = []
            for m, n in all_matches:
                if m.distance < 0.8 * n.distance:  # Relaxed ratio for better matching
                    good_matches.append([m])

            if len(good_matches) > 50:  # Increased minimum match threshold
                print(f"\nDetected Denomination: Rs. {denom}")

                # Verify correct denomination value before using it
                print(f"Denomination extracted: {denom}")  # Debugging line

                audio_file = f"audio/{denom}.mp3"
                if not os.path.exists(audio_file):  # Check if file exists
                    print(f"Audio file not found: {audio_file}")
                    audio_file = "audio/not_found.mp3"  # Fallback

                print(f"Attempting to load and play audio: {audio_file}")  # Debugging line

                try:
                    pygame.mixer.music.load(audio_file)
                    pygame.mixer.music.play()
                    while pygame.mixer.music.get_busy():  # Wait for the music to finish
                        pygame.time.Clock().tick(10)
                except Exception as e:
                    print(f"Error playing audio: {e}")

                # Display matched keypoints
                img_matches = cv2.drawMatchesKnn(test_img, kp1, train_img, kp2, good_matches, None)
                plt.imshow(img_matches)
                plt.show()

                return  # Stop checking after the first successful match

    # If no match is found
    print("No Matches Found")
    audio_file = "audio/not_found.mp3"
    print(f"Attempting to load and play audio: {audio_file}")  # Debugging line
    try:
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():  # Wait for the music to finish
            pygame.time.Clock().tick(10)
    except Exception as e:
        print(f"Error playing audio: {e}")

# Function to manually trigger photo capture and processing
def capture_and_process():
    print("Waiting for photo capture...")
    if download_latest_photo():
        print("New photo detected! Processing...")
        detect_currency()
    else:
        print("Failed to capture new photo.")

# Start processing
capture_and_process()
