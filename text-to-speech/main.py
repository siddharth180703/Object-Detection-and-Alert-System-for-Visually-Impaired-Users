import os
import cv2
import pyttsx3
import numpy as np
import requests
import matplotlib.pyplot as plt
from doctr.io import DocumentFile
from doctr.models import ocr_predictor
import time

# Function to format text for better speech timing
def format_text_for_speech(text):
    text = text.replace(",", " , ")  # Adds space before and after commas
    text = text.replace(".", " . ")  # Adds space before and after periods
    text = text.replace("?", " ? ")  # Adds space before and after question marks
    text = text.replace("!", " ! ")  # Adds space before and after exclamations
    return text.strip()

# Improved Text-to-Speech with Natural Pauses
def text_to_speech(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 120)  # Adjust speed for better clarity
    engine.setProperty('volume', 1.0)  # Set volume to maximum
    voices = engine.getProperty('voices')

    # Select a more natural voice (change index if needed)
    engine.setProperty('voice', voices[0].id)

    words = text.split()  # Split text into words for better control
    for word in words:
        engine.say(word)
        
        # Adding delays for better speech rhythm
        if word in [",", ";"]:  
            time.sleep(0.3)  # Short pause for commas and semicolons
        elif word in [".", "?", "!"]:
            time.sleep(0.7)  # Longer pause for full stops, questions, exclamations
        else:
            time.sleep(0)  # Small pause between words for natural speech
        
        engine.runAndWait()

# Function to capture an image from IP Webcam
def capture_image_from_ip_webcam(ip_address, image_path="captured_image.jpg"):
    try:
        url = f"http://{ip_address}/photo.jpg"
        response = requests.get(url)
        if response.status_code == 200:
            image_arr = np.array(bytearray(response.content), dtype=np.uint8)
            image = cv2.imdecode(image_arr, -1)
            cv2.imwrite(image_path, image)
            return image_path
        else:
            raise Exception("Failed to fetch image from IP Webcam")
    except Exception as e:
        print("Error:", e)
        return None

# Define IP Webcam address (Change this to your phone's IP Webcam URL)
ip_webcam_address = "192.168.19.147:8080"  # Change this to your IP Webcam address

# Capture image from the IP Webcam
image_path = capture_image_from_ip_webcam(ip_webcam_address)

if image_path is None:
    print("Failed to capture image.")
    exit()

# Load the captured image
doc = DocumentFile.from_images(image_path)
print(f"Number of pages: {len(doc)}")

# Load OCR model
predictor = ocr_predictor(pretrained=True)

# Perform OCR on the image
result = predictor(doc)
exported_result = result.export()
extracted_text = ""

# Extract text in proper order
for page in exported_result.get('pages', []):
    for block in page.get('blocks', []):
        for line in block.get('lines', []):
            for word in line.get('words', []):
                extracted_text += word['value'] + " "

# Process the extracted text
processed_text = format_text_for_speech(extracted_text)

# Save text to a file
with open('output.txt', 'w') as f:
    f.write(processed_text)

# Display OCR-detected text on the captured image
synthetic_pages = result.synthesize()
plt.imshow(synthetic_pages[0])
plt.axis('off')
plt.show()

print("Processed Text:", processed_text)

# Convert text to speech if text is detected
if processed_text:
    text_to_speech(processed_text)
else:
    print("No text detected in the image.")

