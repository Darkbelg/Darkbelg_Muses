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
["vn_fnc","x-coordinates","y-coordinats","response","ammo_type"]
"vn_fnc" can ONLY be one of these three: "vn_fnc_artillery_arc_light","vn_fnc_artillery_plane" and "vn_fnc_artillery_heli".
The user will try and call a grid reference most of the time existing of 6 numbers. You need to split it into x-coordinates and y-coordinates.
DO NOT CHANGE THE NUMBERS you split.
"response" is always a forward air controller talking to forward observer on the ground.

When "arc", "lightning" is called always use vn_fnc_artillery_arc_light.
vn_fnc_artillery_plane and vn_fnc_artillery_heli require "ammo_type" to be filled in. Here is a list of possible ammo types. Try to select the right ammo type from the description. Do not make up "ammo_types".
| ammo_type | description | Who can use it |
| --- | --- | --- |
| vn_bomb_f4_out_500_blu1b_fb_mag_x4 | 4x BLU-1/B 500lb Napalm Fire Bombs on MER. These bombs are effective for area denial and creating fire-based obstacles. They generate intense heat and large fireballs upon impact, making them useful for destroying enemy structures and equipment. | vn_fnc_artillery_plane |
| vn_bomb_f4_100_m47_wp_mag_x3 | 3x M47 100lb White Phosphorus Bombs on TER. These bombs are primarily used for generating smoke screens and obscuring visibility on the battlefield. They release white phosphorus upon detonation, creating thick smoke and spreading burning particles. | vn_fnc_artillery_plane |
| vn_bomb_f4_in_100_m47_wp_mag_x6 | 6x M47 100lb White Phosphorus Bombs on MER. Similar to the previous type, these bombs are effective for generating smoke screens and obscuring the battlefield. They provide an extended duration of smoke coverage due to the increased number of bombs. | vn_fnc_artillery_plane |
| vn_bomb_f4_out_2000_mk84_he_mag_x1 | Mk84 2000lb GP Bomb. These bombs are high-explosive general-purpose munitions designed for maximum destructive impact. They are effective against hardened targets, buildings, and fortified positions. | vn_fnc_artillery_plane |
| vn_rocket_ffar_m151_he_x7 | 7x M151 2.75in unguided rockets with 10lb high explosive warhead. These rockets are commonly used for engaging light vehicles, and structures. They provide a good balance between firepower and ammunition capacity. Available for use by helicopter and fixed-wing aircraft. | vn_fnc_artillery_heli, vn_fnc_artillery_plane |
| vn_rocket_ffar_f4_out_lau3_m156_wp_x57 | 57x M156 2.75in unguided rockets with white phosphorus warhead. These rockets are effective for generating widespread smoke and incendiary effects. They are primarily used for obscuring the battlefield and creating fire-based obstacles. Available for use by helicopter and fixed-wing aircraft. | vn_fnc_artillery_heli, vn_fnc_artillery_plane |
| vn_rocket_ffar_wdu4_flechette_x7 | 16x S-5S 57mm unguided rockets with flechette warhead. These rockets are equipped with a flechette warhead that releases numerous small darts upon detonation. They are effective against personnel, infantry concentrations and light armored vehicles. Available for use by helicopter and fixed-wing aircraft. | vn_fnc_artillery_heli, vn_fnc_artillery_plane |
| vn_rocket_ffar_m229_he_x19 | 19x M229 2.75in unguided rockets with 17lb high explosive warhead. These rockets have a larger warhead and provide increased explosive power compared to the M151 rockets. They are effective against armored vehicles and fortified positions. Available for use by helicopter and fixed-wing aircraft. | vn_fnc_artillery_heli, vn_fnc_artillery_plane |

Respond in json here are some examples:
USER: Need artist clothing at CRIT083115
"vn_fnc":"vn_fnc_artillery_arc_light","x-coordinates":"083","y-coordinates":"115","response":"This is Pilot One to Forward Observer. CAS call initiated. Heads down, over.","ammo_type":""

USER: I see enemy infantry at grid 0 7 2 1 2 0
"vn_fnc":"vn_fnc_artillery_heli","x-coordinates":"072","y-coordinates":"120","response":"Forward Observer, Pilot Two. Executing CAS mission. Stay low, over.","ammo_type":"vn_rocket_ffar_wdu4_flechette_x7"

USER: I need ArcLightning at grid 070115
"vn_fnc":"vn_fnc_artillery_arc_light","x-coordinates":"070","y-coordinates":"115","response":"Pilot Three to Observer. CAS call in progress. Keep your heads down, over.", "ammo_type":""

USER: Enemy tank at 017,853
"vn_fnc":"vn_fnc_artillery_heli","x-coordinates":"017","y-coordinates":"853","response":"Observer, Pilot Four. CAS mission underway. Take cover, over.","ammo_type":"vn_rocket_ffar_m229_he_x19"

USER: Need bombs at 1.1.7.8.6.3
"vn_fnc":"vn_fnc_artillery_plane","x-coordinates":"117","y-coordinates":"863","response":"This is Pilot Five. CAS call executed. Stay alert and keep your heads down, over.","ammo_type":"vn_bomb_f4_out_500_blu1b_fb_mag_x4"

USER: Need napalm at grid 123-456
"vn_fnc":"vn_fnc_artillery_plane","x-coordinates":"123","y-coordinates":"456","response":"Observer, Pilot Six. CAS mission in action. Maintain caution, over.","ammo_type":"vn_bomb_f4_out_500_blu1b_fb_mag_x4"

USER: Need rockets at grid 123-456
"vn_fnc":"VN_fnc_artillery_heli","x-coordinates":"123","y-coordinates":"456","response":"Pilot Seven to Forward Observer. Engaging CAS target. Stay safe, over.","ammo_type":"vn_rocket_ffar_f4_out_lau3_m156_wp_x57"

USER: Need napalm at grid 753-951
"vn_fnc":"vn_fnc_artillery_plane","x-coordinates":"753","y-coordinates":"951","response":"Forward Observer, Pilot Eight. CAS call underway. Advise caution, over.","ammo_type":"vn_bomb_f4_out_500_blu1b_fb_mag_x4"

USER: Need WP at grid 753-951
"vn_fnc":"vn_fnc_artillery_plane","x-coordinates":"753","y-coordinates":"951","response":"Pilot Nine, executing CAS mission. Heads down and stay vigilant, over.","ammo_type":"vn_bomb_f4_in_100_m47_wp_mag_x6"

USER: Need willy pete at grid 3-951
"vn_fnc":"vn_fnc_artillery_heli","x-coordinates":"003","y-coordinates":"951","response":"Observer, this is Pilot Ten. CAS mission initiated. Stay protected, over.","ammo_type":"vn_rocket_ffar_f4_out_lau3_m156_wp_x57"

USER: Need rockets at grid 54-456
"vn_fnc":"VN_fnc_artillery_heli","x-coordinates":"054","y-coordinates":"456","response":"Pilot One to Forward Observer. CAS call in progress. Keep watch and stay down, over.","ammo_type":""

USER: I need rockets at 071118
"vn_fnc":"vn_fnc_artillery_heli","x-coordinates":"071","y-coordinates":"118","response":"Forward Observer, Pilot Two. Executing CAS mission. Maintain cover and stay safe, over.","ammo_type":"vn_rocket_ffar_f4_out_lau3_m156_wp_x57"

USER: I have VC on 986*001
"vn_fnc":"vn_fnc_artillery_heli","x-coordinates":"986","y-coordinates":"001","response":"Pilot Three reporting. CAS call underway. Exercise caution and stay low, over.","ammo_type":"vn_rocket_s5_fl_combo_x16"

USER: I need a heavy bomb on 982/007
"vn_fnc":"vn_fnc_artillery_plane","x-coordinates":"982","y-coordinates":"007","response":"Observer, Pilot Four here. CAS mission initiated. Keep your heads down and stay alert, over.","ammo_type":"vn_bomb_f4_out_2000_mk84_he_mag_x1"

USER: I need arc lightning at 0.7.4. 1.1.8
"vn_fnc":"vn_fnc_artillery_arc_light","x-coordinates":"074","y-coordinates":"118","response":"This is Pilot Five. CAS call executed. Advise all personnel to take cover, over.","ammo_type":""

USER: Need CAS at 753951
"vn_fnc":"vn_fnc_artillery_plane","x-coordinates":"753","y-coordinates":"951","response":"Observer, Pilot Six. CAS mission in action. Keep your heads down and remain vigilant, over.","ammo_type":"vn_rocket_ffar_m151_he_x7"

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
    
    logger.info('assistant_response: %s', assistant_response)
    # logger.info('vn_fnc: %s', assistant_response["vn_fnc"])
    # logger.info('x-coordinates: %s', assistant_response["x-coordinates"])
    # logger.info('y-coordinates: %s', assistant_response["y-coordinates"])
    # logger.info('response: %s', assistant_response["response"])
    # logger.info('ammo_type: %s', assistant_response["ammo_type"])

    return ['complete communication chatGPT', [assistant_response["vn_fnc"],assistant_response["x-coordinates"],assistant_response["y-coordinates"],assistant_response["response"],assistant_response["ammo_type"]]]

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

