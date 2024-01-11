import pygame
import sys

pygame.init()

# Load apple eating sound effect
apple_eat_sound_path = "media/apple.wav"
apple_eat_sound = pygame.mixer.Sound(apple_eat_sound_path)

# Play the sound
apple_eat_sound.play(6)

# Add a delay to allow the sound to play before exiting
pygame.time.delay(5000)  # 5000 milliseconds (5 seconds)

# Quit Pygame
pygame.quit()
sys.exit()
