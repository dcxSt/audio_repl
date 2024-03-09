import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, filtfilt
import argparse
import matplotlib.pyplot as plt


def bandpass(data, lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    y = filtfilt(b, a, data)
    return y

parser = argparse.ArgumentParser(description='Filter options')
parser.add_argument('fname', type=str, help='Path to file, manditory')
parser.add_argument('--lo', type=float, help='Lowcut freq (Hz), defaults to 300')
parser.add_argument('--hi', type=float, help='Highcut freq (Hz), defaults to 3400')
args = parser.parse_args()
assert args.fname[-4:]=='.wav', 'incorrect file format, must be wav file'


# load wav file
fs, data = wavfile.read(args.fname)
print(data.shape, type(data[0]))
if data.ndim > 1:
    data = data[:, 0]

# Vocal range freq
lowcut = 300.0 if not args.lo else args.lo # Hz
highcut = 3400.0 if not args.hi else args.hi # Hz
print(f"lowcut {lowcut}")
print(f"highcut {highcut}")

# Apply band-pass filter
filtered = bandpass(data, lowcut, highcut, fs).astype(np.float32)
print(filtered.shape, type(filtered[0]))

plt.subplots(figsize=(8,8))
plt.subplot(211)
plt.plot(data, label='data')
plt.plot(filtered, label='filtered')
plt.subplot(212)
plt.loglog(abs(np.fft.rfft(data))**2, label='unfiltered psd')
plt.loglog(abs(np.fft.rfft(filtered))**2, label='filtered psd')
plt.legend()
plt.show(block=False)
plt.pause(0.5)
input('[Enter] to continue')

fname_out = args.fname[:-4] + "_filtered" + args.fname[-4:]
wavfile.write(fname_out, fs, filtered)

