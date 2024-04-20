from scipy.io.wavfile import write
import sounddevice as sd
import logging
logger = logging.getLogger(__name__)

def __init__(self):
    self.recording = False
    self.myrecording = None
    self.fs = 44100  # Sample rate
    self.channels = 2
    logger.info("Recorder initialized")

def start_recording(self, duration_sec=5):
    if self.recording:
        logger.info("Recording is already in progress")
        return
    
    logger.info("Recording started")
    self.duration_sec = duration_sec
    self.myrecording = sd.rec(
        int(self.duration_sec * self.fs), 
        samplerate=self.fs, channels=self.channels
    )
    self.recording = True
    return 'recording started'

def stop_recording(self):
    if not self.recording:
        logger.info("No recording in progress to stop")
        return
    
    sd.wait()  # Ensure recording is completed
    self.recording = False
    logger.info("Recording finished")

    # Write the recording to a file
    write('output.wav', self.fs, self.myrecording)
    logger.info("File written")

    return 'complete recording'
