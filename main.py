import pygame
import random
import os

x = pygame.init()

pygame.mixer.init()

# Defining Colors

white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
yellow = (255,255,51)
green = (51,255,51)

# Creating Game screen

screen_width = 800
screen_height = 700
gamewindow = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake game with Ani")

# Welcome background

bgimg1 = pygame.image.load("welcome.png")
bgimg1 = pygame.transform.scale(bgimg1, (screen_width, screen_height)).convert_alpha()
bgimg2 = pygame.image.load("bg.jpg")
bgimg2 = pygame.transform.scale(bgimg2, (screen_width, screen_height)).convert_alpha()
bgimg3 = pygame.image.load("gameover.png")
bgimg3 = pygame.transform.scale(bgimg3, (screen_width, screen_height)).convert_alpha()


font = pygame.font.SysFont(None, 55)


# Showing Text in Game window
def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gamewindow.blit(screen_text, [x, y])


clock = pygame.time.Clock()


# Polting Snake

def plot_snake(gamewindow, color, snake_list, snake_size):
    for x, y in snake_list:
        pygame.draw.rect(gamewindow, green, [x, y, snake_size, snake_size])


# Welcome Screen

def welcome():
    exit_game = False

    while not exit_game:

        gamewindow.fill(white)
        gamewindow.blit(bgimg1, (0, 0))
        text_screen("Welcome to snake game",red, 200, 200)
        text_screen("Press space bar to play the game",red, 100, 300)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                exit_game = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.load('bgsong.mp3')
                    pygame.mixer.music.play()
                    gameloop()

        pygame.display.update()
        clock.tick(60)


# Creating the  Game Loop

def gameloop():
    # Game variable

    exit_game = False
    game_over = False
    fps = 60
    velocity_x = 0
    velocity_y = 0
    initial_velocity = 5
    # Snake Head
    snake_x = 55
    snake_y = 45
    snake_size = 15
    # Snake Food

    food_x = random.randint(20, screen_width / 2)
    food_y = random.randint(20, screen_height / 2)
    food_size = 15

    # Score
    score = 0

    # For increasing Snake size
    snake_list = []
    snake_length = 1

    # high Score
    if (not os.path.exists("high_score")):
        with open("high_score.txt", "w") as f:
            f.write("0")

    with open("high_score.txt", "r") as f:
        high_score = f.read()

    while not exit_game:

        if game_over:
            with open("high_score.txt", "w") as f:
                f.write(str(high_score))

            gamewindow.fill(white)
            gamewindow.blit(bgimg3,(0,0))
            text_screen("Game over !!! Press enter to continue", red, 80, 230)
            text_screen("Your Score is : " + str(score), red, 200, 290)
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        pygame.mixer.music.load('bgsong.mp3')
                        pygame.mixer.music.play()
                        gameloop()

        else:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = initial_velocity
                        velocity_y = 0

                    if event.key == pygame.K_LEFT:
                        velocity_x = -initial_velocity
                        velocity_y = 0

                    if event.key == pygame.K_UP:
                        velocity_y = -initial_velocity
                        velocity_x = 0

                    if event.key == pygame.K_DOWN:
                        velocity_y = initial_velocity
                        velocity_x = 0

            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y

            if abs(snake_x - food_x) < 7 and abs(snake_y - food_y) < 7:

                score = score + 10
                print("Score = ", score)
                food_x = random.randint(20, screen_width / 2)
                food_y = random.randint(20, screen_height / 2)
                snake_length = snake_length + 5

                if score > int(high_score):
                    high_score = score

            gamewindow.fill(white)
            gamewindow.blit(bgimg2, (0, 0))
            text_screen("Score = " + str(score) + "  High Score :" + str(high_score), red, 5, 5)
            pygame.draw.rect(gamewindow, red, [food_x, food_y, food_size, food_size])

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snake_list.append(head)

            if len(snake_list) > snake_length:
                del snake_list[0]

            if head in snake_list[:-1]:
                game_over = True
                pygame.mixer.music.load('gameover.mp3')
                pygame.mixer.music.play()

            if snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height:
                game_over = True
                pygame.mixer.music.load('gameover.mp3')
                pygame.mixer.music.play()

            plot_snake(gamewindow, black, snake_list, snake_size)
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()


welcome()

gameloop()
