import time
import random
import statistics
import numpy as np
import subprocess
import pygame
import os

from scipy.io import wavfile

random.seed(2012)

# CONSTANTS (weights in grams)
GOAL = 50000
NUM_RATS = 20
INITIAL_MIN_WT = 200 
INITIAL_MAX_WT = 600
INITIAL_MODE_WT = 300
MUTATE_ODDS = 0.01
MUTATE_MIN = 0.5
MUTATE_MAX = 1.2
LITTER_SIZE = 8
LITTERS_PER_YEAR = 10
GENERATION_LIMIT = 500

# ensure even number of rats for breeding pairs:
if NUM_RATS % 2 != 0:
    NUM_RATS += 1

# initialize population
def population(num_rats, min_wt, max_wt, mode_wt):
    """Initialize a population with triangular distribution of weights."""
    return[int(random.triangular(min_wt, max_wt, mode_wt))\
           for i in range(num_rats)]

# define fitness for breeding
def fitness(population, goal):
    """Measure population fitness based on attribute mean vs target."""
    ave = statistics.mean(population)
    return ave / goal

# the culling
def select(population, to_retain):
    """Cull a poplation to retain certain number only."""
    sorted_population = sorted(population)
    to_retain_by_sex = to_retain//2
    members_per_sex = len(sorted_population)//2
    females = sorted_population[:members_per_sex]
    males = sorted_population[members_per_sex:]
    selected_females = females[-to_retain_by_sex:]
    selected_males = males[-to_retain_by_sex:]
    
    return selected_males, selected_females

# breed
def breed(males, females, litter_size):
    """Crossover genes among members"""
    random.shuffle(males)
    random.shuffle(females)
    children = []
    for male, female in zip(males, females):
        for child in range(litter_size):
            child = random.randint(female, male)
            children.append(child)
    
    return children

# mutate the children
def mutate(children, mutate_odds, mutate_min, mutate_max):
    """Randomly alter rat weights using input odds and fractional changes."""
    for index, rat in enumerate(children):
        if mutate_odds >=random.random():
            children[index] = round(rat * random.uniform(mutate_min, mutate_max))
    
    return children

def main():
    """Initialize population, select, breed, and mutate, display results."""
    generations = 0
    parents = population(NUM_RATS, INITIAL_MIN_WT, INITIAL_MAX_WT, INITIAL_MODE_WT)
    print("initial population weights = {}".format(parents))
    popl_fitness = fitness(parents, GOAL)
    print("initial population fitness = {}".format(popl_fitness))
    print("number to retain = {}".format(NUM_RATS))

    ave_wt = []
    fitness_history = []
    audio_segments = []

    while popl_fitness < 1 and generations < GENERATION_LIMIT:
        selected_males, selected_females = select(parents, NUM_RATS)
        children = breed(selected_males, selected_females, LITTER_SIZE)
        children = mutate(children, MUTATE_ODDS, MUTATE_MIN, MUTATE_MAX)
        parents = selected_males + selected_females + children
        popl_fitness = fitness(parents, GOAL)
        print("Generation {} fitness = {:.4f}".format(generations, popl_fitness))

        fitness_history.append(popl_fitness)

        time.sleep(1.3)
        
        ave_wt.append(int(statistics.mean(parents)))
        generations += 1
    
    print("average weight per generation = {}".format(ave_wt))
    print("\nnumber of generations = {}".format(generations))
    print("number of years = {}" .format(int(generations / LITTERS_PER_YEAR)))

    # test line for proper index function
    # print(fitness_history)

    # --- AUDIO GENERATION SETTINGS ---
    sample_rate = 44100  # Standard audio quality
    duration = 1.3       # How long each gen's tone lasts

    # Step 1: Generate a unique tone math array for each generation's score
    for score, current_gen_ave_wt in zip(fitness_history, ave_wt):
        freq = 100 + (score * 1000)
        
        # This defines the timeline, leave in
        t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
        
        # Perverting the sine waves
        # error = abs(current_gen_ave_wt - GOAL)
        progress = current_gen_ave_wt / GOAL
        progress = min(progress, 1.0)
        instability = progress
        drift_std = 0.2 + instability * 6
        
        # Random mutation
        drift = np.random.normal(
            0, 
            drift_std,
            len(t)
        )

        # Systemic instability
        if current_gen_ave_wt > GOAL:

            transgression = max(0, current_gen_ave_wt - GOAL)
            convulsion = transgression / GOAL

            drift += np.sin(
                np.linspace(0,30,len(t))
            ) * convulsion * 20

        instantaneous_freq = freq + drift
        saturation = 1 + instability * 8

        phase = np.cumsum(
        instantaneous_freq / sample_rate
        )

        # Memory corruption
        # if current_gen_ave_wt > GOAL:
        #   phase += np.random.normal(
        #       0,
        #       convulsion * 0.03,
        #       len(phase)
        #   )

        # Seizure
        if current_gen_ave_wt > GOAL:
           glitches = np.random.rand(len(phase)) < 0.005

           phase[glitches] += np.random.uniform(
               -3,
               3,
               glitches.sum()
           )

        base = np.sin(2*np.pi*phase)
        tone = np.tanh(base * saturation)
        audio_segments.append(tone)

    # Step : Combine all generation tones into a single track and save
    if audio_segments:
        
        # Glue all the separate array chunks into one continuous timeline
        full_track = np.concatenate(audio_segments)
        
        # Convert data to 16-bit integers so media players can read it
        full_track_scaled = np.int16(full_track * 32767)

        # Save the continuous timeline as your WAV file
        wavfile.write(
            "releases/rats/audio/rats.wav",
            sample_rate,
            full_track_scaled
        )
        
        print("\nTomb for 500,000 mutant rats.")
    
    make_visuals(fitness_history)
    make_video()

# --- VISUAL GENERATION SETTINGS ---
def make_visuals(fitness_history):

    pygame.init()

    WIDTH = 1280
    HEIGHT = 720

    screen = pygame.Surface((WIDTH, HEIGHT))

    os.madedirs("frames", exist_ok=True)

    values = np.array(fitness_history)

    values = (
        values - values.min()
    ) / (
        values.max() - values.min()
    )
    
    for frame, value in enumerate(values):

        screen.fill((0,0,0))

        radius = init(30 + value * 220)

        instability = value

        points = []

        for angle in np.linspace(
            0,
            2*np.pi,
            220,
            endpoint=False
        ):
            
            wobble = np.random.normal(
                0,
                instability * 40
            )

            r = radius + wobble
            
            x = WIDTH//2 + np.cos(angle) * r
            v = HEIGHT//2 + np.sin(angle) * r

            points.append((x,y))

        brightness = int(255 * (1-value))

        pygame.draw.polygon(
            screen,
            (brightness,brightness,brightness),
            points,
            widht=3
        )

        pygame.image.save(
            screen,
            f"frames/frame_{frame:06d}.png"
        )

    pygame.quit()

# --- AUDIO/VISUAL OUTPUT ---
def make_video():

    subprocess.run([
    "ffmpeg",
    "-framerate","30",
    "-i","frames/frame_%06d.png",
    "-i","releases/rats/audio/rats.wav",
    "-c:v","libx264",
    "-pix_fmt","yuv420p",
    "releases/rats/video/rats.mp4"
    ])

if __name__ == '__main__':
   start_time = time.time()
   main()
   end_time = time.time()
   duration = end_time - start_time
#    print("\nRuntime for this program was {} seconds.".format(duration))
