import pygame
from utilities import menu_text, load_sprite, load_sound
import button
from main import SpaceGame


class MainMenu:
    def __init__(self):
        pygame.init()
        pygame.mixer.init(frequency=22050, size=16, channels=4)
        self.game_started = False
        # Draw the title screen
        self.screen_width = 1200
        self.screen_height = 1000
        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height))
        ...
        # Title screen music
        self.title_music = load_sound("TitleScreen")
        self.channel_2 = pygame.mixer.Channel(2)
        self.channel_2.set_volume(0.2)
        # First cut screen intial message music
        self.cutscene_music = load_sound("cutscreensong1")
        self.channel_3 = pygame.mixer.Channel(3)
        self.channel_3.set_volume(0.2)

        # Background of menu screen
        self.background = load_sprite("starryBG", False)
        self.background = pygame.transform.scale(self.background, (1200, 1000))
        # Images for menu screen
        self.image_asteroid1 = load_sprite("MenuAsteroid1")
        self.image_asteroid2 = load_sprite("MenuAsteroid1")
        self.image_planet = load_sprite("Planet")
        self.image_spaceship = load_sprite("spaceship")  # Add this line
        ...
        # Scale and position the images
        self.image_planet = pygame.transform.scale(self.image_planet, (700, 700))
        self.image_asteroid1 = pygame.transform.scale(self.image_asteroid1, (200, 200))
        self.image_asteroid2 = pygame.transform.scale(self.image_asteroid2, (200, 200))
        self.image_spaceship = pygame.transform.scale(self.image_spaceship, (45, 45))
        self.image_spaceship = pygame.transform.rotate(self.image_spaceship, -60)
        # Leave the message and fonts empty strings
        # To display different options
        self.message = ""
        self.font = ""
        # Have the color be white
        self.color = (255, 255, 255)
        self.menu = True

        # Size and font for buttons
        self.button_font = pygame.font.Font(
            r"C:\Users\18022\Desktop\game_project\Dev\AlienInvasion\assets\sprites\Alien Future.ttf", 75)
        self.text_quit = self.button_font.render('Quit', True, self.color)
        self.text_start = self.button_font.render('Start', True, self.color)

        # Create button instances
        self.start_button = button.Button(450, 200, self.text_start, 0.5)
        self.exit_button = button.Button(750, 200, self.text_quit, 0.5)

    
    def show_story_overview(self):
        # Fill the screen with black.
        self.screen.fill((0, 0, 0))

        self.channel_3.play(self.cutscene_music, loops=-1)  # Start the cutscene music

        # Define the story text.
        story_text = (
            "In a galaxy far away, your spaceship is stranded\n"
            "in an asteroid field. Your mission is to navigate\n"
            "through the field, destroy the asteroids, and survive.\n"
            "\n"
            "Good luck!"
        )

        # Render the story text.
        font = pygame.font.Font(None, 36)
        lines = story_text.split("\n")
        for i, line in enumerate(lines):
            rendered_text = font.render(line, True, (255, 255, 255))
            self.screen.blit(rendered_text, (50, 50 + 40 * i))

        # Display "Press any key to continue" below the story text.
        continue_text = font.render("Press any key to continue...", True, (255, 255, 255))
        self.screen.blit(continue_text, (50, 50 + 40 * len(lines)))

        # Update the display.
        pygame.display.flip()
        # Wait for the user to press a key.
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (
                    event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
                ):
                    quit()
                elif event.type == pygame.KEYDOWN:  # Any key was pressed.
                    self.channel_3.stop()  # Stop the cutscene music
                    return  # End this method and continue with the game.

    def _menu_screen(self):
        self.channel_2.play(self.title_music, loops=-1)  # Start the title music
 
        # Method for button from Button file
        self.exit_button.draw2(self.background)
        self.start_button.draw2(self.background)

        # blit for menu images
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.image_asteroid1, (800, 100))
        self.screen.blit(self.image_asteroid2, (1000, 300))
        self.screen.blit(self.image_planet, (-100, 500))
        self.screen.blit(self.image_spaceship, (500, 450))  # Add this line


        pygame.display.flip()

        run = True
        while run:
            self.menu = True
            self.message = "Asteroid Chaos"
            menu_text(self.screen, self.message, self.font)

            if self.exit_button.draw2(self.screen):
                quit()

            if self.start_button.draw2(self.screen):
                if not self.game_started:
                    self.channel_2.stop()
                    self.show_story_overview()  # Show the story overview after "Start" is clicked.
                    obj1 = SpaceGame()
                    obj1.run_game()
                    self.game_started = True
                    run = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT or (
                    event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE

                ):
                    quit()

                pygame.display.flip()
