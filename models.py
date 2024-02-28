# Import required resources
import pygame
from pygame.math import Vector2
from pygame.transform import rotozoom
from utilities import load_sprite, wrap_position, get_random_velocity, load_sound

# Constant vector called UP
UP = Vector2(0, -1)

# Global pause variable
paused = False


class GameObject:
    """A class to represent all game objects"""
    # Constructor of class with arguments below

    def __init__(self, position, sprite, velocity):
        self.position = Vector2(position)
        self.sprite = sprite
        # Calculate radius as half of sprite image
        self.radius = sprite.get_width() / 2
        self.velocity = Vector2(velocity)

    # Function draws objects sprite to surface(passed as an argument)
    def draw(self, surface):
        blit_position = self.position - Vector2(self.radius)
        surface.blit(self.sprite, blit_position)

    # Function updates position of object
    def move(self, surface):
        self.position = wrap_position(self.position + self.velocity, surface)

    # Func that will detect collisions
    def collides_with(self, other_obj):
        if isinstance(other_obj, Rocket):
            other_obj_position = Vector2(other_obj.rect.center)
        else:
            other_obj_position = other_obj.position

        distance = self.position.distance_to(other_obj_position)
        return distance < self.radius + other_obj.radius

# Spaceship class that inherits from GameObject.


class Spaceship(GameObject):
    # Variables for the ships movement
    MANEUVERABILITY = 5
    ACCELERATION = 0.07
    BULLET_SPEED = 6
    ROCKET_SPEED = 10

    def __init__(self, position, create_bullet_callback, create_rocket_callback):
        # Callback to add the bullet to the list of all bullets
        self.create_bullet_callback = create_bullet_callback
        # Callback to add the rocket to the list of all rockets
        self.create_rocket_callback = create_rocket_callback
        # Load in the sound method
        self.laser_sound = load_sound("spacegunshot")
        self.rocket_sound = load_sound("laserrocket")
        # For the thruster
        self.thruster_active = False  # Add this line
        self.thruster_sprite = load_sprite("Thruster1")
        # Make a copy of the original UP vector
        self.direction = Vector2(UP)
        super().__init__(position, load_sprite("spaceship"), Vector2(0))

    # Method for changing ships direction
    def rotate(self, clockwise=True):
        sign = 1 if clockwise else -1
        angle = self.MANEUVERABILITY * sign
        self.direction.rotate_ip(angle)

    # Function to update drawing of ship
    def draw(self, surface):
        # Calculate the angle
        angle = self.direction.angle_to(UP)
        # Rotates using rotozoom
        rotated_surface = rotozoom(self.sprite, angle, 1.0)
        # Recalculate blit based on rotated_surface
        rotated_surface_size = Vector2(rotated_surface.get_size())
        # Returns a vector half the length of orignial
        blit_position = self.position - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_position)

        # Draw the thruster when it's active
        if self.thruster_active:
            thruster_angle = angle + 90  # Add 180 degrees to the rotation angle
            thruster_rotated = rotozoom(
                self.thruster_sprite, thruster_angle, 1.0)
            thruster_size = Vector2(thruster_rotated.get_size())
            thruster_offset = self.direction * -30  # Adjust this value if necessary
            thruster_position = self.position + thruster_offset - thruster_size * 0.5
            surface.blit(thruster_rotated, thruster_position)
            self.thruster_active = False

    # Function for ships acceleration

    def accelerate(self, forward=True):
        if forward:
            self.velocity += self.direction * self.ACCELERATION
        else:
            self.velocity -= self.direction * self.ACCELERATION
        self.thruster_active = True  # Set the flag when accelerating

    # Function for ship to go in reverse

    def reverse(self):
        self.velocity -= self.direction * self.ACCELERATION

    # Function to shoot bullets
    def shoot(self):
        # Calculate velocity(direction of ship times bullet_speed, add velocity to bullet)
        bullet_velocity = self.direction * self.BULLET_SPEED + self.velocity
        # Instance of Bullet class, same location as spaceship
        bullet = Bullet(self.position, bullet_velocity)
        # Add bullets to all the bullets in game
        self.create_bullet_callback(bullet)
        self.laser_sound.play()

    # Function to shoot rockets
    def shoot_rocket(self):
        ship_speed = self.velocity.length()
        # Pass self.direction instead of angle
        rocket = Rocket(self.position, self.direction, ship_speed)
        self.create_rocket_callback(rocket)
        self.rocket_sound.play()


# A class for the asteroids
class Asteroid(GameObject):
    def __init__(self, position, create_asteriod_callback, size=3):
        self.create_asteroid_callback = create_asteriod_callback
        self.size = size
        # Load sound for asteroid explosion
        self.explosion_sound = load_sound("explosion")
        self.rocket_explosion = load_sound("badexplosion")

        size_to_scale = {
            3: 1,
            2: 0.5,
            1: 0.25,
        }
        scale = size_to_scale[size]
        sprite = rotozoom(load_sprite("graysmall"), 0, scale)

        super().__init__(position, sprite,
                         get_random_velocity(1, 3))

    def split(self):
        self.explosion_sound.play()  # New code
        if self.size > 1:
            for _ in range(2):
                asteroid = Asteroid(
                    self.position, self.create_asteroid_callback, self.size - 1
                )
                self.create_asteroid_callback(asteroid)

    def rocket_split(self):
        self.rocket_explosion.play()


# A class for the bullets
class Bullet(GameObject):
    def __init__(self, position, velocity):
        super().__init__(position, load_sprite("Bullet"), velocity)

    # Added this to bullet class, wrapping would not work correctly otherwise.
    # This makes so only bullets disappear after leaving screen.
    def move(self, surface):
        self.position = self.position + self.velocity


# A class for the rockets
class Rocket(pygame.sprite.Sprite):
    def __init__(self, ship_position, ship_direction, ship_speed):
        super().__init__()
        self.image_orig = pygame.image.load(
            r"C:\Users\18022\Desktop\game_project\Dev\AlienInvasion\assets\sprites\Rocket.png").convert_alpha()
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = 20
        self.position = Vector2(ship_position)
        self.rect.center = self.position
        self.rotation = ship_direction.angle_to(Vector2(0, -1))
        self.image = pygame.transform.rotate(self.image_orig, self.rotation)

        self.speed = ship_speed + 10
        self.velocity = Vector2(0, -self.speed).rotate(-self.rotation)

    def update(self):
        self.position += self.velocity
        self.rect.x = self.position.x
        self.rect.y = self.position.y

    def move(self, surface):
        self.position += self.velocity
        self.rect.center = self.position

    def draw(self, surface):
        surface.blit(self.image, self.rect)
