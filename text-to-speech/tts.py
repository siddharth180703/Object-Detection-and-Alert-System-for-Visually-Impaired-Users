import pyttsx3
import string

def text_to_speech(text):
    engine = pyttsx3.init()

    # Set properties (optional)
    engine.setProperty('rate', 125)  # Speed of speech
    engine.setProperty('volume', 0.9)  # Volume level (0.0 to 1.0)

    # Speak directly instead of saving
    engine.say(text)

    # Run the engine
    engine.runAndWait()

def remove_punctuation(text):
    return text.translate(str.maketrans("", "", string.punctuation))

# Read the text file
with open('output.txt', 'r') as file:
    text = file.read()
    clean_text = remove_punctuation(text)
    print("Text without punctuation:", clean_text)

if __name__ == "__main__":
    text_to_speech(clean_text)  # Now it will speak directly
