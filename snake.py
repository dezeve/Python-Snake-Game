import pygame, sys, random
from pygame.math import Vector2
import utils.constants as constants

game_name = constants.GAME_NAME

snake_color = constants.SNAKE_COLOR
background_color = constants.BACKGROUND_COLOR
fruit_color = constants.FRUIT_COLOR

frame_rate = constants.FRAME_RATE

cell_number = constants.CELL_NUMBER
cell_size = constants.CELL_SIZE

class Snake:
    def __init__(self):
        self.body = [Vector2(5,10), Vector2(6,10), Vector2(7,10)]
        self.direction = Vector2(-1,0)
        self.new_block = False

    def draw_snake(self, snake_color):
        for block in self.body:
            snake_rect = pygame.Rect(block.x * cell_size, block.y * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, snake_color, snake_rect)

    def movement_snake(self):
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert (0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
             body_copy = self.body[:-1]
             body_copy.insert (0, body_copy[0] + self.direction)
             self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

class Fruit:
    def __init__(self):
        self.randomize()
    
    def draw_fruit(self, fruit_color):
        fruit_rect = pygame.Rect(self.pos.x * cell_size, self.pos.y * cell_size, cell_size, cell_size)
        pygame.draw.rect(screen, fruit_color, fruit_rect)
    
    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)

class Main:
    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit()
    
    def update(self):
        self.snake.movement_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.fruit.draw_fruit(fruit_color)
        self.snake.draw_snake(snake_color)
        
    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()

    def game_over(self):
        pygame.quit()
        sys.exit()

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()
        
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

pygame.init()

clock = pygame.time.Clock()

screen = pygame.display.set_mode((cell_size * cell_number, cell_size * cell_number))
pygame.display.set_caption(game_name)

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

main_game = Main()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            main_game.game_over()
        
        if event.type == SCREEN_UPDATE:
            main_game.update()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0,-1)
            if event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1, 0)
            if event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0,1)
            if event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1, 0)

    screen.fill(background_color) 
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(frame_rate)
