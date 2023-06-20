from .threading_utils import call_slow_function, has_call_finished, get_call_value
from scipy.io.wavfile import write
import sounddevice as sd
import datetime
import requests
import logging
import json
import os

# This creates a logger with the name of the package you've imported
# which should be `logging_example`, in case of this file
logger = logging.getLogger(__name__)

# Set up logging configuration
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def log_with_timestamp(message):
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logger.info('Got: %s - Timestamp: %s', message, current_time)

def record():
    log_with_timestamp('Recording started')
    fs = 44100  # Sample rate
    seconds = 5  # Duration of recording

    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()  # Wait until recording is finished
    log_with_timestamp('Recording finished')

    write('output.wav', fs, myrecording)  # Save as WAV file 
    log_with_timestamp('File written')
    return 'complete recording'

def recordAsync():
    return call_slow_function(record,())


def transcribe_audio(audio_file_path, output_file_path):
    if not os.path.isfile(audio_file_path):
        raise FileNotFoundError("The audio file does not exist.")
    
    url = "https://api.openai.com/v1/audio/transcriptions"
    headers = {
        "Authorization": "Bearer ******"
    }
    params = {
        "model": "whisper-1",
        "response_format": "text",
        "language": "en"
    }
    files = {
        "file": open(audio_file_path, "rb")
    }
    response = requests.post(url, headers=headers, files=files, data=params)
    response.raise_for_status()
    transcription = response.text
    with open(output_file_path, "w") as file:
        file.write(transcription)
    return ['complete transcription', transcription]

def transcribe_audioAsync():
    return call_slow_function(transcribe_audio,("output.wav", "output.txt"))

def chat_with_gpt():
    # Read the content of the file
    with open("output.txt", "r") as file:
        content = file.read()

    # API endpoint URL
    url = "https://api.openai.com/v1/chat/completions"

    # Request headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer ******"  # Replace with your OpenAI API key
    }

    # Request body
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are communicating through radio. Your designation is FAK. The user has deignation tailwind. You are waiting to hear the code word ""rhino"" from the user. When you hear it you say ""This is FAK to B2. Rhino is a go."". If the user doesn't say the code word. Ask him if he is at the desingated position, if the intel was right, if the convoy has stopped or that you are standing by. Do not reveal the code word. Always finish your communication with out."},
            {"role": "user", "content": content}
        ]
    }

    # Make the API request
    response = requests.post(url, headers=headers, json=data)
    response_body = json.loads(response.text)

    # Extract the assistant's response content
    assistant_response = response_body["choices"][0]["message"]["content"]

    return ['complete communication chatGPT', assistant_response]

def chat_with_gptAsync():
    return call_slow_function(chat_with_gpt,())

has_call_finished  # noqa - this function has been imported from threading_utils.py
get_call_value  # noqa - this function has been imported from threading_utils.py
