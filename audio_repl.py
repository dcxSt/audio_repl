import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
from datetime import datetime

# Parameters
FS = 44100  # Sample rate
channels = 1  # Number of audio channels

# Initialize a list to hold recorded frames
recorded_frames = []

# Define the callback function for recording
def callback(indata, frames, time, status):
    recorded_frames.append(indata.copy())

def start_audio_recording():
    stream = sd.InputStream(samplerate=FS, channels=channels, callback=callback)
    stream.start()
    filename = f'out_{int(datetime.now().timestamp() * 1000)}_ctime_start_ms.wav'
    print("Recording audio...")
    return stream, filename 

def stop_audio_recording(stream, filename):
    stream.stop()
    stream.close()
    audio_data = np.concatenate(recorded_frames, axis=0)
    write(filename, FS, audio_data)
    print(f"Audio recording saved as {filename}")

## Create the stream object
#stream = sd.InputStream(samplerate=FS, channels=channels, callback=callback)
#stream.start()  # Start the stream explicitly
#print("Recording... (press Enter to stop)")
#input()  # Wait for user input to stop recording
#stream.stop()  # Stop the stream explicitly
#stream.close()  # Close the stream explicitly
def repl():
    print("Audio Recorder REPL")
    print("Type 'start' to begin recording and 'stop' to end and save.")
    stream = None
    filename = None
    while True:
        command = input(">>> ").strip().lower()
        if command == "start":
            if stream is not None:
                print("Recording already in progress.")
            else:
                stream, filename = start_audio_recording()
        elif command == "stop":
            if stream is None:
                print("No recording in progress.")
            else:
                stop_audio_recording(stream, filename)
                stream = None
                print("Enter 'start' to start anew, 'exit' to quit.")
        elif command == "exit":
            if stream is not None:
                print("Stopping recording before exit...")
                stop_audio_recording(stream, filename)
            break

if __name__ == "__main__":
    repl()