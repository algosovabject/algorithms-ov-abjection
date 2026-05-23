from pydub import effects

voice = AudioSegment.from_file("my_scream.wav")
slowed = effects.speedup(voice, playback_speed=0.5)  # half speed
reversed_voice = voice.reverse()

mix = slowed.overlay(reversed_voice, position=1000)  
play(mix)
