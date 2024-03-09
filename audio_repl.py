import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
from datetime import datetime
from time import time
import json
import struct
import socket

# kernel parameters
HOST = '127.0.0.1' # data.acquisition.host
PORT = 6767
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

id = 1 # event id?

# Parameters
FS = 44100  # Sample rate
channels = 1  # Number of audio channels

# Initialize a list to hold recorded frames
recorded_frames = []

# Define the callback function for recording
def callback(indata, frames, time, status):
    recorded_frames.append(indata.copy())

def start_audio_recording():
    global id
    stream = sd.InputStream(samplerate=FS, channels=channels, callback=callback)
    stream.start()
    filename = f'out_start_mus_{int(datetime.now().timestamp() * 1e6)}_id_{str(id).zfill(3)}.wav'
    print("Recording audio...")
    return stream, filename 

def stop_audio_recording(stream, filename):
    stream.stop()
    stream.close()
    audio_data = np.concatenate(recorded_frames, axis=0)
    write(filename, FS, audio_data)
    print(f"Audio recording saved as {filename}")

def start():
    global id
    stream, filename = start_audio_recording()
    data_to_send = {
      "id": id,
      "timestamp": int(time() * 1e6),
      "event": "start_experiment",
      "value": "start_audio"
    }
    print(f"data = {data_to_send}") # debug
    event = json.dumps(data_to_send).encode("utf-8")
    msg = struct.pack("!I", len(event)) + event
    sock.sendall(msg)
    id += 1
    print("start message sent to kernel")
    return stream, filename

def stop(stream, filename):
    global id
    data_to_send = {
      "id": id,
      "timestamp": int(time() * 1e6),
      "event": "end_experiment",
      "value": "stop_audio"
    }
    print(f"data = {data_to_send}") # debug
    event = json.dumps(data_to_send).encode("utf-8")
    msg = struct.pack("!I", len(event)) + event
    sock.sendall(msg)
    id += 1
    print("stop message sent to kernel, ending audio...")
    stop_audio_recording(stream, filename)
    print("done")

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
                stream, filename = start()
        elif command == "stop":
            if stream is None:
                print("No recording in progress.")
            else:
                stop(stream, filename)
                stream = None
                print("Enter 'start' to start anew, 'exit' to quit.")
        elif command == "exit":
            if stream is not None:
                print("Stopping recording before exit...")
                stop(stream, filename)
            break

if __name__ == "__main__":
    repl()
