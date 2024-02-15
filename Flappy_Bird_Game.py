import random  # For generating random numbers
import sys  # We will use sys.exit to exit the program
import pygame
from pygame.locals import *  # Basic pygame imports

# Global Variables for the game
framepersecond = 32
window_width = 289
window_height = 450
window = pygame.display.set_mode((window_width, window_height))
elevation = window_height * 0.8
game_images = {}
bird_player = "images/bird.png"
background_img = "images/background.png"
pipe_img = "images/pipe.png"


def welcomeScreen():
    """
    Shows welcome images on the screen
    """
    # Load font
    font = pygame.font.SysFont(None, 36)

    horizontal = float(window_width / 2.5)
    vertical = int((window_height - game_images["player"].get_height()) / 3)
    basex = 0
    while True:
        for event in pygame.event.get():
            # if user clicks on cross button, close the game
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            # If the user presses space or up key, start the game for them
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            else:
                window.blit(game_images["background"], (0, 0))
                window.blit(game_images["player"], (horizontal, vertical))
                window.blit(game_images["base"], (basex, elevation))
                # Display "begin the game" text
                line1 = "Press Space or"
                line2 = "Up to begin the game"
                text_surface1 = font.render(line1, True, (0, 0, 0))
                text_surface2 = font.render(line2, True, (0, 0, 0))
                text_width1, text_height1 = text_surface1.get_size()
                text_width2, text_height2 = text_surface2.get_size()
                text_x1 = (window_width - text_width1) / 2
                text_x2 = (window_width - text_width2) / 2
                text_y1 = (
                    vertical + game_images["player"].get_height() + 10
                )  # Adjust the 10 value as needed
                text_y2 = text_y1 + text_height1 + 5  # Adjust the 5 value as needed
                window.blit(text_surface1, (text_x1, text_y1))
                window.blit(text_surface2, (text_x2, text_y2))
                pygame.display.update()
                FPSCLOCK.tick(framepersecond)


def mainGame():
    score = 0
    horizontal = int(window_width / 5)
    vertical = int(window_width / 2)
    basex = 0

    # Create 2 pipes for blitting on the screen
    newPipe1 = createPipe()
    newPipe2 = createPipe()

    # my List of upper pipes
    upperPipes = [
        {"x": window_width + 200, "y": newPipe1[0]["y"]},
        {"x": window_width + 200 + (window_width / 2), "y": newPipe2[0]["y"]},
    ]
    # my List of lower pipes
    lowerPipes = [
        {"x": window_width + 200, "y": newPipe1[1]["y"]},
        {"x": window_width + 200 + (window_width / 2), "y": newPipe2[1]["y"]},
    ]

    pipeVelX = -4

    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1

    playerFlapAccv = -8  # velocity while flapping
    playerFlapped = False  # It is true only when the bird is flapping
    crashed = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if not crashed:
                if event.type == KEYDOWN and (
                    event.key == K_SPACE or event.key == K_UP
                ):
                    if vertical > 0:
                        playerVelY = playerFlapAccv
                        playerFlapped = True
            else:
                if event.type == KEYDOWN and (
                    event.key == K_SPACE or event.key == K_UP
                ):
                    return

        if not crashed:
            crashTest = isGameOver(
                horizontal, vertical, upperPipes, lowerPipes
            )  # This function will return true if the player is crashed
            if crashTest:
                crashed = True

        # Game logic if not crashed
        if not crashed:
            # check for score
            playerMidPos = horizontal + game_images["player"].get_width() / 2
            for pipe in upperPipes:
                pipeMidPos = pipe["x"] + game_images["pipe"][0].get_width() / 2
                if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                    score += 1
                    print(f"Your score is {score}")

            if playerVelY < playerMaxVelY and not playerFlapped:
                playerVelY += playerAccY

            if playerFlapped:
                playerFlapped = False
            playerHeight = game_images["player"].get_height()
            vertical = vertical + min(playerVelY, elevation - vertical - playerHeight)

            # move pipes to the left
            for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
                upperPipe["x"] += pipeVelX
                lowerPipe["x"] += pipeVelX

            # Add a new pipe when the first is about to cross the leftmost part of the screen
            if 0 < upperPipes[0]["x"] < 5:
                newpipe = createPipe()
                upperPipes.append(newpipe[0])
                lowerPipes.append(newpipe[1])

            # if the pipe is out of the screen, remove it
            if upperPipes[0]["x"] < -game_images["pipe"][0].get_width():
                upperPipes.pop(0)
                lowerPipes.pop(0)

        # Lets blit our sprites now
        window.blit(game_images["background"], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            window.blit(game_images["pipe"][0], (upperPipe["x"], upperPipe["y"]))
            window.blit(game_images["pipe"][1], (lowerPipe["x"], lowerPipe["y"]))

        window.blit(game_images["base"], (basex, elevation))
        window.blit(game_images["player"], (horizontal, vertical))
        displayScore(score)  # Always display score
        if crashed:
            displayMessage("Game Over")  # Display message when crashed
        pygame.display.update()
        FPSCLOCK.tick(framepersecond)


def displayScore(score):
    myDigits = [int(x) for x in list(str(score))]
    width = 0
    for digit in myDigits:
        width += game_images["numbers"][digit].get_width()
    Xoffset = (window_width - width) / 2

    for digit in myDigits:
        window.blit(game_images["numbers"][digit], (Xoffset, window_height * 0.12))
        Xoffset += game_images["numbers"][digit].get_width()


def displayMessage(message):
    font = pygame.font.SysFont(None, 50)
    text = font.render(message, True, (0, 0, 0))
    window.blit(
        text,
        (
            window_width / 2 - text.get_width() / 2,
            window_height / 3 - text.get_height() / 2,
        ),
    )


def isGameOver(horizontal, vertical, upperPipes, lowerPipes):
    if vertical > elevation - 25 or vertical < 0:
        return True

    for pipe in upperPipes:
        pipeHeight = game_images["pipe"][0].get_height()
        if (
            vertical < pipeHeight + pipe["y"]
            and abs(horizontal - pipe["x"]) < game_images["pipe"][0].get_width()
        ):
            return True

    for pipe in lowerPipes:
        if (vertical + game_images["player"].get_height() > pipe["y"]) and abs(
            horizontal - pipe["x"]
        ) < game_images["pipe"][0].get_width():
            return True

    return False


def createPipe():
    """
    Generate positions of two pipes(one bottom straight and one top rotated ) for blitting on the screen
    """
    pipeHeight = game_images["pipe"][0].get_height()
    offset = window_height / 3
    y2 = offset + random.randrange(
        0, int(window_height - game_images["base"].get_height() - 1.2 * offset)
    )
    pipeX = window_width + 10
    y1 = pipeHeight - y2 + offset
    pipe = [{"x": pipeX, "y": -y1}, {"x": pipeX, "y": y2}]  # upper Pipe  # lower Pipe
    return pipe


if __name__ == "__main__":
    # This will be the main point from where our game will start
    pygame.init()  # Initialize all pygame's modules
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption("Flappy Bird by CodeWithHarry")
    game_images["numbers"] = (
        pygame.image.load("images/0.png").convert_alpha(),
        pygame.image.load("images/1.png").convert_alpha(),
        pygame.image.load("images/2.png").convert_alpha(),
        pygame.image.load("images/3.png").convert_alpha(),
        pygame.image.load("images/4.png").convert_alpha(),
        pygame.image.load("images/5.png").convert_alpha(),
        pygame.image.load("images/6.png").convert_alpha(),
        pygame.image.load("images/7.png").convert_alpha(),
        pygame.image.load("images/8.png").convert_alpha(),
        pygame.image.load("images/9.png").convert_alpha(),
    )

    game_images["base"] = pygame.image.load("images/base.png").convert_alpha()
    game_images["pipe"] = (
        pygame.transform.rotate(pygame.image.load(pipe_img).convert_alpha(), 180),
        pygame.image.load(pipe_img).convert_alpha(),
    )

    game_images["background"] = pygame.image.load(background_img).convert()
    game_images["player"] = pygame.image.load(bird_player).convert_alpha()

    while True:
        welcomeScreen()  # Shows welcome screen to the user until he presses a button
        mainGame()  # This is the main game function
