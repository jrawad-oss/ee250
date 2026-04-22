import sounddevice as sd
from scipy.io.wavfile import write

fs = 44100
seconds = 3

print("Recording...")
audio = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
sd.wait()

write("vm_test.wav", fs, audio)

print("Saved vm_test.wav")
