grain_size = 100  # ms
voice = AudioSegment.from_file("my_whisper.wav")

grains = [voice[i:i+grain_size] for i in range(0, len(voice), grain_size)]
random.shuffle(grains)
glitch = sum(grains[:50])

play(glitch)
