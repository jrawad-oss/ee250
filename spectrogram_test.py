from scipy.io import wavfile
from scipy import signal
import numpy as np
import matplotlib.pyplot as plt

wav_file = "bird_clip.wav"

sample_rate, audio = wavfile.read(wav_file)

# If stereo, take one channel
if len(audio.shape) > 1:
    audio = audio[:, 0]

# Convert integers to float if needed
audio = audio.astype(np.float32)

frequencies, times, spectrogram = signal.spectrogram(audio, fs=sample_rate)

plt.figure(figsize=(10, 5))
plt.pcolormesh(times, frequencies, 10 * np.log10(spectrogram + 1e-10), shading="gouraud")
plt.ylabel("Frequency [Hz]")
plt.xlabel("Time [sec]")
plt.title("Spectrogram")
plt.colorbar(label="Intensity [dB]")
plt.tight_layout()
plt.savefig("vm_spectrogram.png")
plt.show()

print("Saved vm_spectrogram.png")
