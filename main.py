import sys
import pygame
import pygame.font
from models import Asteroid, Spaceship, GameObject, Rocket
from scoreboards import HUD
from utilities import load_sprite, get_random_position, print_text, load_sound


class SpaceGame:
    """Overall class to manage game assets and behavior"""
    # Variable to for asteroids minimal starting distance from ship
    min_asteroid_distance = 250

    # Constructor of class with arguments below

    def __init__(self):
        """Initalize the game, and create game resources"""
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 1000))
        self.background = load_sprite("BG4_2", False)
        self.bullets = []
        self.rocket = []
        self.rockets = pygame.sprite.Group()
        self.ship_moving = load_sound("spaceshipacceleration")
        self.ship_reverse = load_sound("truckbackupsound")
        self.ship_moving.set_volume(0.1)
        self.font = pygame.font.Font(None, 36)
        self.font_name = 'Dev\AlienInvasion\assets\sprites\Alien Future.ttf', 114
        self.text_color = (255, 255, 255)
        self.font = pygame.font.Font(None, 64)
        self.sm_font = pygame.font.Font(None, 32)
        self.clock = pygame.time.Clock()
        self.message = ""
        self.pause = False
        # self.rockets = Rocket
        # The (550, 550) are coordinates of ship starting position
        self.spaceship = Spaceship(
            (550, 550), self.bullets.append, self.rocket.append)
        pygame.display.set_caption("Asteroid Alley")
        self.hud = HUD(self.screen)
        self.score = 0
        self.ammo = 10
        self.health = 100
        self.game_music = load_sound("BattleintheStars")
        self.channel_1 = pygame.mixer.Channel(1)
        self.channel_1.set_volume(0.2)
       

        # Get the Asteroids from models
        self.asteroids = []
        for _ in range(3):
            while True:
                position = get_random_position(self.screen)
                if (position.distance_to(self.spaceship.position) > self.min_asteroid_distance):
                    break
            self.asteroids.append(
                Asteroid(position, self.asteroids.append))

    # Main loop of the game

    def run_game(self):
        """Start the main loop for the game"""
        game_music_started = False
        while True:
            self._check_events()
            self.rockets.update()
            self._process_game_logic()
            self._get_game_objects()
            self._update_screen()
            if not game_music_started:
                self.channel_1.play(self.game_music, loops=-1, fade_ms=5000)
                print("Started playing music...")
                game_music_started = True

    def _check_events(self):
        """Respond to keypresses and mouse events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE

            ):
                quit()

                # Add button for shooting bullets
            elif (
                self.spaceship
                # Bullet is generated only when space bar is pressed
                and event.type == pygame.KEYDOWN
                and event.key == pygame.K_SPACE
            ):
                self.spaceship.shoot()

            # CHANGED HERE
            elif (
                self.spaceship
                # Rocket is generated only when 'r' key is pressed
                and event.type == pygame.KEYDOWN
                and event.key == pygame.K_r


            ):
                self.spaceship.shoot_rocket()

            # Configure letter "p" to pause the game
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                self.run_game = False
                self.pause = True

                # Loop to control pausing and unpausing
                while self.pause:
                    self.pause = True
                    self.message = "Pause"
                    for event in pygame.event.get():
                        print_text(self.screen, self.message, self.font)
                        if event.type == pygame.QUIT or (
                            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
                        ):
                            quit()

                        # Player needs to type 'c' to continue game
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_c:

                            self.pause = False
                            self.message = ""
                            self.run_game = True

                        pygame.display.update()

        # Code for various functions when certain keys are pushed
        is_key_pressed = pygame.key.get_pressed()

        """# if block for all key commands"""
        # if not self.pause:
        if self.spaceship:
            # To spin right
            if is_key_pressed[pygame.K_RIGHT]:
                self.spaceship.rotate(
                    clockwise=True)
            # To spin left
            if is_key_pressed[pygame.K_LEFT]:
                self.spaceship.rotate(clockwise=False)
            # Quit game by pressing 'q'
            if is_key_pressed[pygame.K_q]:
                sys.exit()
            # Accelerate ship with up arrow
            if is_key_pressed[pygame.K_UP]:
                self.spaceship.accelerate()
            # Play the ship accerlating sound
            if is_key_pressed[pygame.K_UP]:
                self.ship_moving.play(-1)
            elif not is_key_pressed[pygame.K_UP]:
                self.ship_moving.stop()
            # Ship accelerates in reverse
            if is_key_pressed[pygame.K_DOWN]:
                self.spaceship.reverse()
            # Ship reverse sound effect
            if is_key_pressed[pygame.K_DOWN]:
                self.ship_reverse.play()
            # Reverse method
            elif not is_key_pressed[pygame.K_DOWN]:
                self.ship_reverse.stop()

    def _get_game_objects(self):
        # Helper method for used by drawing and moving logic
        game_objects = [*self.asteroids, *self.bullets, *self.rocket]

        if self.spaceship:
            game_objects.append(self.spaceship)
        return game_objects

    def _process_game_logic(self):
        """Update spaceship with move method"""
        for game_object in self._get_game_objects():
            game_object.move(self.screen)

        # Use .collides_with() to check collisions
        if self.spaceship:
            for asteroid in self.asteroids:
                if asteroid.collides_with(self.spaceship):
                    self.spaceship = None
                    # Message if you lost the game
                    self.message = "You lost!"
                    break

        # Bullets colliding with asteroids
        for bullet in self.bullets[:]:
            # Create a copy below
            for asteroid in self.asteroids[:]:
                if asteroid.collides_with(bullet):
                    self.asteroids.remove(asteroid)
                    self.bullets.remove(bullet)
                    asteroid.split()
                    break

        # Rockets colliding with asteroids
        for rocket in self.rocket[:]:
            # Create a copy below
            for asteroid in self.asteroids[:]:
                if asteroid.collides_with(rocket):
                    self.asteroids.remove(asteroid)
                    self.rocket.remove(rocket)
                    asteroid.rocket_split()
                    break

        # Remove bullets once they leave the screen
        # First line creates a copy like above
        for bullet in self.bullets[:]:
            if not self.screen.get_rect().collidepoint(bullet.position):
                self.bullets.remove(bullet)

                # Remove rockets once they leave the screen
        # Remove rockets once they leave the screen
        for rocket in self.rocket[:]:
            if not self.screen.get_rect().collidepoint(rocket.position):
                self.rockets.remove(rocket)

     # Check if all asteroids are destroyed
        if not self.asteroids:
            print_text(self.screen, "You Won!", self.font)
            pygame.display.flip()
            # Wait for 3 seconds before closing the window
            self.running = False
            return

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen"""

        # Draw background and set position
        self.screen.blit(self.background, (0, 0))

        # Draw game objects
        for game_object in self._get_game_objects():
            game_object.draw(self.screen)

         # Draw the HUD with the current score, ammo, and health
        self.hud.draw_hud(self.score, self.ammo, self.health)

        # Display message on the screen
        print_text(self.screen, self.message, self.font)

        # Make the most recently drawn screen visible
        pygame.display.flip()
        self.clock.tick(60)


if __name__ == "__main__":
    # Make an instance of the class, and run the game
    ai = SpaceGame()
    ai.run_game()
