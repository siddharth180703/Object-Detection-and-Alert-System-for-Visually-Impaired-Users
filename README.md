# AI-Powered Text-to-Speech from Image OCR & Currency Recognition System 📷🗣️💰

## Overview

This project combines **AI-powered text-to-speech (OCR-based) and currency recognition** functionalities. It captures images from an IP Webcam, extracts text or detects currency denominations, and plays an appropriate audio response. The system uses **OpenCV, Doctr for OCR, ORB for currency recognition, and pygame for audio playback.**

## Features

### 🗣️ **Text-to-Speech System**

- **Live Image Capture**: Captures images from an IP camera (phone camera) in real-time.
- **OCR-Based Text Extraction**: Uses `doctr` to extract text from images.
- **Text-to-Speech (TTS)**: Converts extracted text to speech using `pyttsx3`.
- **Natural Pauses in Speech**: Reads text fluently with proper pauses at commas and full stops.
- **Saves Extracted Text**: Stores the recognized text in `output.txt`.
- **Displays OCR-Processed Image**: Shows the captured image with detected text.

### 💰 **Currency Recognition System**

- **Feature-based Currency Detection**: Uses ORB feature detection and brute-force matching for currency recognition.
- **Audio Feedback**: Plays an MP3 file corresponding to the detected denomination.
- **Graphical Visualization**: Displays keypoint matches between the captured image and stored training images.

## Technologies Used

- **Python**
- **OpenCV** (ORB feature detection, keypoint matching, image processing)
- **Requests** (Downloading live images from an IP camera)
- **Pygame** (Audio playback for detected text and denomination)
- **Matplotlib** (Visualization of matches and OCR results)
- **Doctr** (OCR-based text extraction)

## Installation

### **Prerequisites**

Ensure you have **Python 3.7+** installed. Then, install the required dependencies:

```sh
pip install opencv-python numpy requests pygame matplotlib python-doctr torch torchvision torchaudio tensorflow
```

## Folder Structure

```
├── files/
│   ├── 100_1.jpg      # Training images for ₹100
│   ├── 500_1.jpg      # Training images for ₹500
│   ├── live_capture.jpg  # Latest captured image
│
├── audio/
│   ├── 100.mp3        # Audio for ₹100
│   ├── 500.mp3        # Audio for ₹500
│   ├── not_found.mp3  # Default message if no match found
│
├── currency_detector.py  # Currency recognition script
├── text_to_speech.py  # OCR and TTS script
├── README.md  # Project documentation
```

## How to Use

### 🗣️ **Text-to-Speech System**

1. **Start the mobile camera server** (e.g., using IP Webcam for Android) and update the `photo_url` in the script.
2. **Run the script**:
   ```sh
   python text_to_speech.py
   ```
3. Show printed or handwritten text to the camera.
4. The system will:
   - Capture the image
   - Extract the text
   - Play the extracted text as speech
   - Display the OCR-processed image

### 💰 **Currency Recognition System**

1. **Start the mobile camera server** and update the `photo_url` in the script.
2. **Run the script**:
   ```sh
   python currency_detector.py
   ```
3. Show a currency note to the camera.
4. The system will:
   - Capture the image
   - Compare it with stored training images
   - Play the corresponding denomination audio
   - Display the matched keypoints

## Troubleshooting

- If audio is not playing, ensure **pygame is installed** and the correct MP3 files exist in the `audio/` folder.
- If no keypoints are detected, check if **training images have clear patterns and features**.
- Ensure the **IP camera URL is correct** and accessible.

## Future Improvements

- Replace ORB with **deep learning (CNN) for better accuracy**.
- Implement **Tesseract OCR** to read currency text.
- Add **real-time video processing** instead of static image capture.
- Improve **text-to-speech voice quality** with deep learning models.

## License

This project is open-source and available under the **MIT License**.
