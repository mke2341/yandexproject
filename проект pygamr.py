import pygame
import sys
import random
import time


class Game():
    def __init__(self): #инициализация окна 
        self.screen_width = 720
        self.screen_height = 500
        self.fps = pygame.time.Clock()
        self.score = 0

    def errors_checking(self): #проверяем на ошибки 
        check_errors = pygame.init()
        if check_errors[1] > 0:
            sys.exit()
        else:
            print('OK')

    def surf(self): #окно 
        self.play_surface = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Змейка')

    def event_loop(self, change_to): #клавиши
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    change_to = "RIGHT"
                elif event.key == pygame.K_LEFT or event.key == ord('a'):
                    change_to = "LEFT"
                elif event.key == pygame.K_UP or event.key == ord('w'):
                    change_to = "UP"
                elif event.key == pygame.K_DOWN or event.key == ord('s'):
                    change_to = "DOWN"
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        return change_to

    def new_screen(self): #обновление окна
        pygame.display.flip()
        game.fps.tick(20)

    def show_score(self, choice=1): #очки 
        s_font = pygame.font.SysFont('Arial', 24)
        s_surf = s_font.render(
            'Score: {0}'.format(self.score), True, pygame.Color(0, 0, 0))
        s_rect = s_surf.get_rect()
        if choice == 1:
            s_rect.midtop = (80, 10)
        else:
            s_rect.midtop = (360, 120)
        self.play_surface.blit(s_surf, s_rect)

    def game_over(self): #конец игры 
        go_font = pygame.font.SysFont('Arial', 72)
        go_surf = go_font.render('Game over', True, pygame.Color(255, 0, 0))
        go_rect = go_surf.get_rect()
        go_rect.midtop = (360, 15)
        self.play_surface.blit(go_surf, go_rect)
        self.show_score(0)
        pygame.display.flip()
        time.sleep(3)
        pygame.quit()
        sys.exit()


class Snake():
    def __init__(self, snake_color): #змея создается
        self.snake_head_pos = [100, 50] 
        self.snake_body = [[100, 50], [90, 50], [80, 50]]
        self.snake_color = snake_color
        self.direction = "RIGHT"
        self.change_to = self.direction

    def moving(self): #движение змеи
        if any((self.change_to == "RIGHT" and not self.direction == "LEFT",
                self.change_to == "LEFT" and not self.direction == "RIGHT",
                self.change_to == "UP" and not self.direction == "DOWN",
                self.change_to == "DOWN" and not self.direction == "UP")):
            self.direction = self.change_to

    def change_head_position(self): #изменение головы
        if self.direction == "RIGHT":
            self.snake_head_pos[0] += 10
        elif self.direction == "LEFT":
            self.snake_head_pos[0] -= 10
        elif self.direction == "UP":
            self.snake_head_pos[1] -= 10
        elif self.direction == "DOWN":
            self.snake_head_pos[1] += 10

    def snake_snake(self, score, food_pos, screen_width, screen_height): #еда 
        self.snake_body.insert(0, list(self.snake_head_pos))
        if (self.snake_head_pos[0] == food_pos[0] and
                self.snake_head_pos[1] == food_pos[1]):
            food_pos = [random.randrange(1, screen_width/10)*10,
                        random.randrange(1, screen_height/10)*10]
            score += 1
        else:
            self.snake_body.pop()
        return score, food_pos

    def draw_snake(self, play_surface, surface_color): #змея рисуется
        play_surface.fill(surface_color)
        for pos in self.snake_body:
            pygame.draw.rect(
                play_surface, self.snake_color, pygame.Rect(
                    pos[0], pos[1], 10, 10))

    def check_obstacles(self, game_over, screen_width, screen_height): #врезания головы змеи
        if any((
            self.snake_head_pos[0] > screen_width-10
            or self.snake_head_pos[0] < 0,
            self.snake_head_pos[1] > screen_height-10
            or self.snake_head_pos[1] < 0
                )):
            game_over()
        for block in self.snake_body[1:]:
            if (block[0] == self.snake_head_pos[0] and
                    block[1] == self.snake_head_pos[1]):
                game_over()


class Food():
    def __init__(self, food_color, screen_width, screen_height): #еда
        self.food_color = food_color
        self.food_size_x = 10
        self.food_size_y = 10
        self.food_pos = [random.randrange(1, screen_width/10)*10,
                         random.randrange(1, screen_height/10)*10]

    def draw_food(self, play_surface): #картинка еды 
        pygame.draw.rect(
            play_surface, self.food_color, pygame.Rect(
                self.food_pos[0], self.food_pos[1],
                self.food_size_x, self.food_size_y))


game = Game()
snake = Snake(pygame.Color(139, 0, 0))
food = Food(pygame.Color(0, 255, 0), game.screen_width, game.screen_height)

game.errors_checking()
game.surf()

while True:
    snake.change_to = game.event_loop(snake.change_to)

    snake.moving()
    snake.change_head_position()
    game.score, food.food_pos = snake.snake_snake(game.score, food.food_pos, game.screen_width, game.screen_height)
    snake.draw_snake(game.play_surface, pygame.Color(255, 255, 255))
    food.draw_food(game.play_surface)

    snake.check_obstacles(game.game_over, game.screen_width, game.screen_height)

    game.show_score()
    game.new_screen()