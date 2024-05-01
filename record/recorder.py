import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
from datetime import datetime
import threading
import logging

class Recorder:
    def __init__(self, timeout=60):  # Set default timeout to 60 seconds
        self.timeout = timeout
        self.fs = 44100  # Sample rate
        self.channels = 2
        self.recording = False
        self.frames = []
        self.timer = None
        logging.info("Recorder initialized")

    def callback(self, indata, frames, time, status):
        if self.recording:
            self.frames.append(indata.copy())

    def start_recording(self):
        if self.recording:
            logging.info("Attempt to start recording failed: Already recording")
            return

        self.frames = []
        self.recording = True
        self.stream = sd.InputStream(
            samplerate=self.fs,
            channels=self.channels,
            callback=self.callback
        )
        self.stream.start()
        logging.info("Recording started")

        # Set up the timeout to stop recording after specified time
        self.timer = threading.Timer(self.timeout, self.stop_recording)
        self.timer.start()
        return 'start recording'

    def stop_recording(self):
        if not self.recording:
            logging.info("Attempt to stop recording failed: No recording in progress")
            return

        if self.timer:
            self.timer.cancel()
            self.timer = None
            
        self.stream.stop()
        self.recording = False
        logging.info("Recording stopped")

        recorded_audio = np.concatenate(self.frames, axis=0)
        write('output.wav', self.fs, recorded_audio)
        logging.info("Recording saved as output.wav")
        return 'stopped recording'
