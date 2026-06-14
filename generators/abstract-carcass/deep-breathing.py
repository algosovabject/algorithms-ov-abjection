import numpy as np
from pydub import AudioSegment
from pydub.playback import play

# basic sine wave generator
def sine_wave(freq, duration, sample_rate=44100, amp=0.5):
    t = np.linspace(0, duration, int(sample_rate*duration), endpoint=False)
    waveform = (amp * np.sin(2 * np.pi * freq * t) * 32767).astype(np.int16)
    return AudioSegment(
        waveform.tobytes(), 
        frame_rate=sample_rate, 
        sample_width=2, 
        channels=1
    )

# example: two clashing tones
drone1 = sine_wave(100, 10)  
drone2 = sine_wave(99.5, 10)  
mix = drone1.overlay(drone2)  

play(mix)