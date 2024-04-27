import pygame
import time
import random

snake_speed = 10
#set window size
window_x = 720
window_y = 480
active = True

black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

pygame.init()

pygame.display.set_caption("Mr. Snake")
game_window = pygame.display.set_mode((window_x, window_y))
fps = pygame.time.Clock()

#start position
snake_position = [100, 50]
#starting body of snake
snake_body = [
    [100, 50],
    [90, 50],
    [80, 50],
    [70, 50],
]

#random fruit position
fruit_position = [
    random.randrange(1, (window_x//10)) * 10,
    random.randrange(1, (window_y//10)) * 10,
]
fruit_spawn = True

#set snake starting face to the right
direction = "RIGHT"
change_to = direction

#initial score
score = 0
def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render("Score : " + str(score), True, color)
    score_box = score_surface.get_rect()
    game_window.blit(score_surface, score_box)

def game_over():
    end_font = pygame.font.SysFont("times new roman", 50)
    game_over_surface = end_font.render(
        "Final Score : " + str(score), True, red
    )
    game_over_box = game_over_surface.get_rect()
    game_over_box.midtop = (window_x/2, window_y/4)

    game_window.blit(game_over_surface, game_over_box)
    pygame.display.flip()

    time.sleep(2)
    pygame.quit()
    quit()

while active:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()
            if event.key == pygame.K_UP:
                change_to = "UP"
            if event.key == pygame.K_DOWN:
                change_to = "DOWN"
            if event.key == pygame.K_LEFT:
                change_to = "LEFT"
            if event.key == pygame.K_RIGHT:
                change_to = "RIGHT"
    
    #If two inputs ignore one
    if change_to == "UP" and direction != "DOWN":
        direction = "UP"
    if change_to == "DOWN" and direction != "UP":
        direction = "DOWN"
    if change_to == "LEFT" and direction != "RIGHT":
        direction = "LEFT"
    if change_to == "RIGHT" and direction != "LEFT":
        direction = "RIGHT"

    #Moving the snake 1 = "Y/ - UP/ + DOWN" 0 = "X/ - LEFT/ + RIGHT"
    if direction == "UP":
        snake_position[1] -= 10
    if direction == "DOWN":
        snake_position[1] += 10
    if direction == "LEFT":
        snake_position[0] -= 10
    if direction == "RIGHT":
        snake_position[0] += 10
    
    #Snake growing and adding score
    snake_body.insert(0, list(snake_position))
    if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
        score += 10
        snake_speed += 2
        fruit_spawn = False
    else:
        snake_body.pop()

    #Add loop for walls
    if snake_position[0] < 0 or snake_position[0] > window_x - 10:
        snake_position[0] = 0
        snake_body.insert(0, list(snake_position))
        snake_body.pop()
    
    if not fruit_spawn:
        fruit_position = [
            random.randrange(1, (window_x//10)) * 10,
            random.randrange(1, (window_y//10)) * 10,
        ]

    fruit_spawn = True
    game_window.fill(black)

    #Draw snake
    for position in snake_body:
        pygame.draw.rect(
            game_window,
            green,
            pygame.Rect(position[0], position[1], 10, 10),
        )
    
    #Draw fruit
    pygame.draw.rect(
        game_window,
        white,
        pygame.Rect(fruit_position[0], fruit_position[1], 10, 10)
    )

    #Game Over conditions
    #Running into wall/roof
    if snake_position[1] < 0 or snake_position[1] > window_y - 10:
        game_over()
    
    #Running into snkae body
    for piece in snake_body[1:]:
        if snake_position[0] == piece[0] and snake_position[1] == piece[1]:
            game_over()
    
    #display score
    show_score(1, white, "times new roman", 20)

    #refresh game screen
    pygame.display.update()
    fps.tick(snake_speed)