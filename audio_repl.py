import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
from datetime import datetime

# Parameters
fs = 44100  # Sample rate
channels = 1  # Number of audio channels
filename = f'out_{int(datetime.now().timestamp() *1000)}_ctime_ms.wav'  # Name of the output file


# Initialize a list to hold recorded frames
recorded_frames = []

# Define the callback function for recording
def callback(indata, frames, time, status):
    recorded_frames.append(indata.copy())

def start_recording():
    stream = sd.InputStream(samplerate=fs, channels=channels, callback=callback)
    stream.start()
    print("Recording...")
    return stream

def stop_recording(stream, filename):
    stream.stop()
    stream.close()
    audio_data = np.concatenate(recorded_frames, axis=0)
    write(filename, fs, audio_data)
    print(f"Recording saved as {filename}")

## Create the stream object
#stream = sd.InputStream(samplerate=fs, channels=channels, callback=callback)
#stream.start()  # Start the stream explicitly
#print("Recording... (press Enter to stop)")
#input()  # Wait for user input to stop recording
#stream.stop()  # Stop the stream explicitly
#stream.close()  # Close the stream explicitly
def repl():
    print("Audio Recorder REPL")
    print("Type 'start' to begin recording and 'stop' to end and save.")
    stream = None
    while True:
        command = input(">>> ").strip().lower()
        if command == "start":
            if stream is not None:
                print("Recording already in progress.")
            else:
                stream = start_recording()
        elif command == "stop":
            if stream is None:
                print("No recording in progress.")
            else:
                stop_recording(stream, filename)
                stream = None
                print("Enter 'start' to start anew, 'exit' to quit.")
        elif command == "exit":
            if stream is not None:
                print("Stopping recording before exit...")
                stop_recording(stream, filename)
            break

if __name__ == "__main__":
    repl()
            

#stream = start_recording()
#
#print("lalala, i'm doing other stuff")
#input("Enter to exit...")
#
#stop_recording(stream, filename)

## Concatenate all recorded frames
#audio_data = np.concatenate(recorded_frames, axis=0)
#
## Save the recording as a WAV file
#print("Writing to file...")
#write(filename, fs, audio_data)
#print(f"Recording saved as {filename}")
