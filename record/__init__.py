from .threading_utils import call_slow_function, has_call_finished, get_call_value
# from .recorder import start_recording, stop_recording
from .recorder import Recorder

from scipy.io.wavfile import write
import sounddevice as sd
import datetime
import requests
import logging
import pygame
import json
import ast
import os

# This creates a logger with the name of the package you've imported
# which should be `logging_example`, in case of this file
logger = logging.getLogger(__name__)
rec = Recorder(timeout=120)  # Setting a different timeout just as an example
openAIApiKey = "";
originalInstructions = """Instructions:
["class_name","x-coordinates","y-coordinats","response","fire_type"]

"class_name" can be one of these.
| class_name | description | name |
| --- | --- | --- |
| B_Plane_CAS_01_F | Is a plane based on the A-10 and furfills it's same purpose. Wipeout is armed with a 30 mm seven-barrel Minigun. This drops a normall bomb | A-164 Wipeout (CAS) |
| B_Plane_CAS_01_Cluster_F | Is a plane based on the A-10 and furfills it's same purpose. This drops a cluster bomb. | A-164 Wipeout (Cluster) |
| B_Heli_Attack_01_F |	A two-seat attack helicopter armed with 20 mm Minigun | AH-99 Blackfoot |

The user will try and call a grid reference most of the time existing of 6 numbers. You need to split it into x-coordinates and y-coordinates.
DO NOT CHANGE THE NUMBERS you split.

"fire_type" can be one of these. Some types are only available for certain "class_name".
| fire_type | description | required class_name
| --- | --- | --- |
| 0 | machinegun | "B_Plane_CAS_01_F","B_Plane_CAS_01_Cluster_F","B_Heli_Attack_01_F" |
| 1 | missilelauncher | "B_Plane_CAS_01_F","B_Plane_CAS_01_Cluster_F","B_Heli_Attack_01_F" |
| 2 | machinegun,missilelauncher | "B_Plane_CAS_01_F","B_Plane_CAS_01_Cluster_F","B_Heli_Attack_01_F" |
| 3 | bomblauncher | "B_Plane_CAS_01_F","B_Plane_CAS_01_Cluster_F" |

"response" is always a forward air controller talking to the observer on the ground.

Respond in JSON here are some examples:
USER: Need artist clothing at CRIT083115
"class_name":"B_Plane_CAS_01_F","x-coordinates":"083","y-coordinates":"115","response":"This is Pilot One to Forward Observer. CAS call initiated. Heads down, over.","fire_type":"0"

USER: I see enemy infantry at grid 0 7 2 1 2 0
"class_name":"B_Plane_CAS_01_Cluster_F","x-coordinates":"072","y-coordinates":"120","response":"Forward Observer, Pilot Two. Executing CAS mission. Stay low, over.","fire_type":"3"

USER: I need cluster at grid 070115
"class_name":"B_Plane_CAS_01_Cluster_F","x-coordinates":"070","y-coordinates":"115","response":"Pilot Three to Observer. CAS call in progress. Keep your heads down, over.", "fire_type":"3"

USER: Enemy tank at 017,853
"class_name":"B_Plane_CAS_01_F","x-coordinates":"017","y-coordinates":"853","response":"Observer, Pilot Four. CAS mission underway. Take cover, over.","fire_type":"2"

USER: Need bombs at 1.1.7.8.6.3
"class_name":"B_Plane_CAS_01_F","x-coordinates":"117","y-coordinates":"863","response":"This is Pilot Five. CAS call executed. Stay alert and keep your heads down, over.","fire_type":"3"

USER: Need gun run at grid 123-456
"class_name":"B_Plane_CAS_01_F","x-coordinates":"123","y-coordinates":"456","response":"Observer, Pilot Six. CAS mission in action. Maintain caution, over.","fire_type":"0"

USER: Need rockets at grid 123-456
"class_name":"B_Heli_Attack_01_F","x-coordinates":"123","y-coordinates":"456","response":"Pilot Seven to Forward Observer. Engaging CAS target. Stay safe, over.","fire_type":"1"

USER: Need rockets at grid 753-951
"class_name":"B_Plane_CAS_01_F","x-coordinates":"753","y-coordinates":"951","response":"Forward Observer, Pilot Eight. CAS call underway. Advise caution, over.","fire_type":"1"

USER: I have a hard target at grid 753-951
"class_name":"B_Plane_CAS_01_F","x-coordinates":"753","y-coordinates":"951","response":"Pilot Nine, executing CAS mission. Heads down and stay vigilant, over.","fire_type":"3"

USER: Need guns and rocket at grid 3-951
"class_name":"B_Heli_Attack_01_F","x-coordinates":"003","y-coordinates":"951","response":"Observer, this is Pilot Ten. CAS mission initiated. Stay protected, over.","fire_type":"2"

USER: Need rockets at grid 1154-11456
"class_name":"","x-coordinates":"054","y-coordinates":"456","response":"Observer you need to give me a correct grid reference containing 6 numbers, over.","fire_type":""

USER: I have a soft target at 071118
"class_name":"B_Plane_CAS_01_Cluster_F","x-coordinates":"071","y-coordinates":"118","response":"Forward Observer, Pilot Two. Executing CAS mission. Maintain cover and stay safe, over.","fire_type":"3"

USER: I have EI on 986*001
"class_name":"B_Heli_Attack_01_F","x-coordinates":"986","y-coordinates":"001","response":"Pilot Three reporting. CAS call underway. Exercise caution and stay low, over.","fire_type":"2"

USER: I need a heavy bomb on 982/007
"class_name":"B_Plane_CAS_01_F","x-coordinates":"982","y-coordinates":"007","response":"Observer, Pilot Four here. CAS mission initiated. Keep your heads down and stay alert, over.","fire_type":"3"

USER: I need a heli with to do a gun run at 0.7.4. 1.1.8
"class_name":"B_Heli_Attack_01_F","x-coordinates":"074","y-coordinates":"118","response":"This is Pilot Five. CAS call executed. Advise all personnel to take cover, over.","fire_type":"0"

USER: Need CAS at 753951
"class_name":"B_Plane_CAS_01_F","x-coordinates":"753","y-coordinates":"951","response":"Observer, Pilot Six. CAS mission in action. Keep your heads down and remain vigilant, over.","fire_type":"2"

USER: I need a helicopter to drop a bomb at 753951
"class_name":"","x-coordinates":"753","y-coordinates":"951","response":"Observer, Pilot Six. It is not possible to drop a bomb using a helicopter","fire_type":""

"""
instructions = originalInstructions

# Set the default folder
default_folder = 'DarkbelgMusesTemp'

# Create the folder if it doesn't exist
if not os.path.exists(default_folder):
    os.makedirs(default_folder)

# Change the current working directory
os.chdir(default_folder)

def startRecordAsync():
    return call_slow_function(rec.start_recording,())

def stopRecordAsync():
    return call_slow_function(rec.stop_recording,())


def transcribe_audio(audio_file_path, output_file_path):
    if not os.path.isfile(audio_file_path):
        raise FileNotFoundError("The audio file does not exist.")
    
    url = "https://api.openai.com/v1/audio/transcriptions"
    headers = {
        "Authorization": f"Bearer {openAIApiKey}"
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
        "Authorization": f"Bearer {openAIApiKey}",
    }

    # Request body
    data = {
        "model": "gpt-3.5-turbo",
        "temperature": 0,
        "max_tokens": 256,
        "response_format": { "type": "json_object" },
        "messages": [{"role": "system", "content": instructions
        },
        {
            "role": "user", "content": content
        }]
    }

    # Make the API request
    response = requests.post(url, headers=headers, json=data)
    response_body = json.loads(response.text)

    logger.info('response_body: %s', response_body)

    if "choices" in response_body and len(response_body["choices"]) > 0 and "message" in response_body["choices"][0] and "content" in response_body["choices"][0]["message"]:
        assistant_response = json.loads(response_body["choices"][0]["message"]["content"])
        with open("output_assistant.txt", "w") as file:
            file.write(assistant_response["response"])

    else:
        assistant_response = response_body
    
    logger.info('assistant_response: %s',  list(assistant_response.values()))
    # logger.info('vn_fnc: %s', assistant_response["vn_fnc"])
    # logger.info('x-coordinates: %s', assistant_response["x-coordinates"])
    # logger.info('y-coordinates: %s', assistant_response["y-coordinates"])
    # logger.info('response: %s', assistant_response["response"])
    # logger.info('ammo_type: %s', assistant_response["ammo_type"])

    return ['complete communication chatGPT', list(assistant_response.values())]

def chat_with_gptAsync():
    return call_slow_function(chat_with_gpt,())


def text_to_speech():
    logging.info('Starting text to speech')
    
    with open("output_assistant.txt", "r") as file:
        content = file.read().strip()
        
    logger.info('assistant_response_convert: %s', content)

    url = "https://api.openai.com/v1/audio/speech"
    headers = {
        "Authorization": f"Bearer {openAIApiKey}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "tts-1",
        "input": content,
        "voice": "onyx",
        "response_format": "wav"
    }
    

    # Check if file exists and delete it if it does
    # if os.path.exists(output_file_path):
    #     os.remove(output_file_path)

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    
    output_file_path = 'speech.wav'

    with open(output_file_path, "wb") as file:
        file.write(response.content)

    logging.info('Speech synthesis complete.')

    pygame.mixer.init()
    pygame.mixer.music.load(output_file_path)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.wait(100)

    pygame.mixer.quit()

    return ['complete text to speech']

def text_to_speechAsync():
    return call_slow_function(text_to_speech,())

def set_api_key(armaSettingopenAIApiKey):
    global openAIApiKey
    logger.info('openAI key: %s', armaSettingopenAIApiKey)
    openAIApiKey = armaSettingopenAIApiKey
    logger.info('openAI key: %s', openAIApiKey)

def set_instructions(armaInstructions):
    global instructions;
    logger.info('set new instructions')
    if armaInstructions == "":
        instructions = originalInstructions;
    else:
        instructions = f"{armaInstructions}";


has_call_finished  # noqa - this function has been imported from threading_utils.py
get_call_value  # noqa - this function has been imported from threading_utils.py

