from pydub import AudioSegment
from pydub.playback import play
import random

# Load in raw sounds
whisper = AudioSegment.from_file("whisper1.wav")
scream = AudioSegment.from_file("scream1.wav")
moan = AudioSegment.from_file("moan1.wav")

# Create a noisy backdrop (by layering and detuning)
backdrop = whisper.low_pass_filter(800).overlay(moan.reverse())

# Random loop of voices
voices = [whisper, scream, moan]
loop = AudioSegment.silent(duration=0)

for _ in range(8):  # 8 fragments long
    choice = random.choice(voices)
    slice = choice[0:2000]  # 2 sec fragment
    loop += slice + AudioSegment.silent(duration=500)

# Final track = backdrop + loop
track = backdrop.overlay(loop)

# Export for sharing
track.export("ritual_sketch_01.wav", format="wav")
