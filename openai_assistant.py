from openai import OpenAI
import os
from dotenv import load_dotenv
from rich import print as rprint
from rich.text import Text
import speech_recognition as sr
import pyttsx3

# Load the environment variables from .env file
load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')

client = OpenAI(
  api_key=os.environ['OPENAI_API_KEY'],  # this is also the default, it can be omitted
)

print(f"Secret Key: {api_key}")


# Initialize the text-to-speech engine
engine = pyttsx3.init()


def recognize_speech_from_mic():
    """Capture speech from the microphone and return it as text."""
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio)
        print(f"You said: {query}")
        return query
    except sr.RequestError:
        print("API unavailable/unresponsive")
    except sr.UnknownValueError:
        print("Unable to recognize speech")
    return ""

def get_chatgpt_response(prompt):
    """Send a prompt to OpenAI's GPT and return the response."""
    response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
            {"role": "system", "content": "You are a helpful assistant named Jarvis."},
            {"role": "user", "content": prompt}
    ]
    )

    return response.choices[0].message.content.strip()

def speak_text(query):
    """Convert text to speech and play it."""
    engine.say(query)
    engine.runAndWait()

def main():
    """Main function to run the AI voice assistant."""
    while True:
        # Step 1: Recognize speech from the user
        user_input = recognize_speech_from_mic()
        if 'wake up' in user_input.lower():
            print("Jarvis is now active.")
            while True:
                user_input = recognize_speech_from_mic()
                if user_input.lower() in ["exit", "quit", "stop"]:
                    print("Exiting...")
                    break

                # Step 2: Get response from ChatGPT
                response = get_chatgpt_response(user_input)

                # Step 3: Convert response to speech
                speak_text(response)

if __name__ == "__main__":
    main()
