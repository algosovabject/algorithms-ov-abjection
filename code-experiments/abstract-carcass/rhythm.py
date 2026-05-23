import random

click = sine_wave(1000, 0.05)  # tiny blip
silence = AudioSegment.silent(duration=50)

# build a random beat sequence
beat = AudioSegment.silent(duration=0)
for _ in range(100):
    if random.random() > 0.7:
        beat += click
    else:
        beat += silence

play(beat)
