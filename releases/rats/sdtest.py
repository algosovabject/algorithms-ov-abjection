import numpy as np
import sounddevice as sd

sample_rate = 44100

t = np.linspace(0, 1, sample_rate, endpoint=False)

tone = np.sin(2*np.pi*440*t)

sd.play(tone, sample_rate)
sd.wait()

print("Done")