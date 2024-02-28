import pygame
from pygame.color import Color
from pygame.image import load
from pygame.math import Vector2
from pygame.locals import *
from pygame.mixer import Sound
import random


# Method for game status text
# Takes the surface,text,font and color
def print_text(surface, text, font, color=Color("tomato")):
    # Creates surface with .render()
    text_surface = font.render(text, True, color)

    # Represents a rectangle for the surface
    rect = text_surface.get_rect()
    # Positions to the center of the screen
    rect.center = Vector2(surface.get_size()) / 2

    # Draws on the screen
    surface.blit(text_surface, rect)


# Method for menu text
# Similar to print_text function
def menu_text(surface, text, font, color=Color("white")):
    font = pygame.font.Font(
        r"C:\Users\18022\Desktop\game_project\Files\VEGASX-Regular.ttf", 130)
    # Create surface with .render()
    text_surface = font.render(text, True, color)

    # Represents a rectangle for the surface
    rect = text_surface.get_rect()

    # Positions to the center of the screen
    rect.center = Vector2(600, 75)

    # Draws on the screen
    surface.blit(text_surface, rect)


# Method to help load sound
def load_sound(name):
    path = f"C:\\Users\\18022\\Desktop\\game_project\\Dev\\AlienInvasion\\assets\\sprites\\sound\\{name}.wav"
    return Sound(path)


# Reuseable function for image loading
def load_sprite(name, with_alpha=True):
    path = f"C:\\Users\\18022\\Desktop\\game_project\\Dev\\AlienInvasion\\assets\\sprites\\{name}.png"
    loaded_sprite = load(path)

    # Returns a better format for pygame
    if with_alpha:
        return loaded_sprite.convert_alpha()
    else:
        return loaded_sprite.convert()


# Create a wrap_position()
def wrap_position(position, surface):
    x, y = position
    w, h = surface.get_size()
    # Modulo operator makes sure position never leaves the area
    # of the given surface
    return Vector2(x % w, y % h)

# Function to generate random set of coodinates


def get_random_position(surface):
    return Vector2(
        random.randrange(surface.get_width()),
        random.randrange(surface.get_height()),
    )

# Function to generate a random value
# Between min_speed and max_speed
# and random angle between 0-360 degrees


def get_random_velocity(min_speed, max_speed):
    speed = random.randint(min_speed, max_speed)
    angle = random.randrange(0, 360)
    return Vector2(speed, 0).rotate(angle)
