import pygame
from pygame.locals import *
import random

# Инициализация Pygame
pygame.init()

# Размеры окна игры
screen_width = 800
screen_height = 600

# Создание окна игры
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Арканоид")

clock = pygame.time.Clock()

# Загрузка изображения фона
background_image = pygame.image.load("background.jpg")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# Загрузка изображения платформы
platform_image = pygame.image.load("platform.png")
platform_image = pygame.transform.scale(platform_image, (100, 25))

# Загрузка изображения мяча
ball_image = pygame.image.load("ball.png")
ball_radius = 10
ball_image = pygame.transform.scale(ball_image, (ball_radius * 2, ball_radius * 2))

# Загрузка изображения кирпича
brick_image = pygame.image.load("brick.png")
brick_width = 75
brick_height = 25
brick_image = pygame.transform.scale(brick_image, (brick_width, brick_height))

# Количество блоков в строке и столбце
blocks_per_row = 10
blocks_per_column = 5

# Отступы между блоками
horizontal_padding = (screen_width - brick_width * blocks_per_row) // (blocks_per_row + 1)
vertical_padding = 20

# Позиция платформы
platform_width = 100
platform_height = 10
platform_x = (screen_width - platform_width) // 2
platform_y = screen_height - platform_height - 10

# Скорость платформы
platform_speed = 5

# Позиция мяча
ball_x = screen_width // 2
ball_y = screen_height // 2
ball_dx = random.choice([-3, 3])
ball_dy = 3

# Создание блоков
block_list = []
for row in range(blocks_per_column):
    for col in range(blocks_per_row):
        block_x = horizontal_padding + col * (brick_width + horizontal_padding)
        block_y = vertical_padding + row * (brick_height + vertical_padding)
        block_rect = pygame.Rect(block_x, block_y, brick_width, brick_height)
        block_list.append(block_rect)

# Загрузка шрифта
font = pygame.font.Font(None, 36)

# Создание текста
game_title = font.render("Арканоид", True, (255, 255, 255))
title_rect = game_title.get_rect()
title_rect.centerx = screen.get_rect().centerx
title_rect.centery = screen.get_rect().centery - 50

start_text = font.render("Начать", True, (255, 255, 255))
start_rect = start_text.get_rect()
start_rect.centerx = screen.get_rect().centerx
start_rect.centery = screen.get_rect().centery

settings_text = font.render("Настройки", True, (255, 255, 255))
settings_rect = settings_text.get_rect()
settings_rect.centerx = screen.get_rect().centerx
settings_rect.centery = screen.get_rect().centery + 50

speed_text = font.render("Скорость", True, (255, 255, 255))
speed_rect = speed_text.get_rect()
speed_rect.centerx = screen.get_rect().centerx - 100
speed_rect.centery = screen.get_rect().centery + 100

platform_speed_text = font.render("Платформы", True, (255, 255, 255))
platform_speed_rect = platform_speed_text.get_rect()
platform_speed_rect.centerx = screen.get_rect().centerx
platform_speed_rect.centery = screen.get_rect().centery + 150

ball_speed_text = font.render("Мяча", True, (255, 255, 255))
ball_speed_rect = ball_speed_text.get_rect()
ball_speed_rect.centerx = screen.get_rect().centerx
ball_speed_rect.centery = screen.get_rect().centery + 200

platform_speed_value = 5
ball_speed_value = 3

# Флаги состояния игры
show_main_screen = True
show_settings = False
game_over = False
game_win = False

# Основной игровой цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if show_main_screen:
        screen.blit(background_image, (0, 0))
        screen.blit(game_title, title_rect)
        screen.blit(start_text, start_rect)
        screen.blit(settings_text, settings_rect)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            show_main_screen = False
            show_settings = False

        if keys[pygame.K_s]:
            show_main_screen = False
            show_settings = True

    elif show_settings:
        screen.blit(background_image, (0, 0))
        screen.blit(speed_text, speed_rect)
        screen.blit(platform_speed_text, platform_speed_rect)
        screen.blit(ball_speed_text, ball_speed_rect)

        platform_speed_value_text = font.render(str(platform_speed_value), True, (255, 255, 255))
        platform_speed_value_rect = platform_speed_value_text.get_rect()
        platform_speed_value_rect.centerx = screen.get_rect().centerx + 100
        platform_speed_value_rect.centery = screen.get_rect().centery + 150

        ball_speed_value_text = font.render(str(ball_speed_value), True, (255, 255, 255))
        ball_speed_value_rect = ball_speed_value_text.get_rect()
        ball_speed_value_rect.centerx = screen.get_rect().centerx + 100
        ball_speed_value_rect.centery = screen.get_rect().centery + 200

        screen.blit(platform_speed_value_text, platform_speed_value_rect)
        screen.blit(ball_speed_value_text, ball_speed_value_rect)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            show_main_screen = True
            show_settings = False

        if keys[pygame.K_UP]:
            platform_speed_value += 1
            ball_speed_value += 1

        if keys[pygame.K_DOWN]:
            platform_speed_value -= 1
            ball_speed_value -= 1

        # Ограничение значений скорости
        if platform_speed_value < 1:
            platform_speed_value = 1
            ball_speed_value = 1

        if platform_speed_value > 10:
            platform_speed_value = 10
            ball_speed_value = 10

        platform_speed = platform_speed_value
        ball_dy = ball_speed_value

    elif game_over:
        screen.blit(background_image, (0, 0))
        game_over_text = font.render("Игра окончена", True, (255, 255, 255))
        game_over_rect = game_over_text.get_rect()
        game_over_rect.centerx = screen.get_rect().centerx
        game_over_rect.centery = screen.get_rect().centery
        screen.blit(game_over_text, game_over_rect)

        restart_text = font.render("Нажмите Enter, чтобы начать заново", True, (255, 255, 255))
        restart_rect = restart_text.get_rect()
        restart_rect.centerx = screen.get_rect().centerx
        restart_rect.centery = screen.get_rect().centery + 50
        screen.blit(restart_text, restart_rect)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            game_over = False
            platform_x = (screen_width - platform_width) // 2
            platform_y = screen_height - platform_height - 10
            ball_x = screen_width // 2
            ball_y = screen_height // 2
            ball_dx = random.choice([-3, 3])
            ball_dy = ball_speed_value

            block_list = []
            for row in range(blocks_per_column):
                for col in range(blocks_per_row):
                    block_x = horizontal_padding + col * (brick_width + horizontal_padding)
                    block_y = vertical_padding + row * (brick_height + vertical_padding)
                    block_rect = pygame.Rect(block_x, block_y, brick_width, brick_height)
                    block_list.append(block_rect)

    elif game_win:
        screen.blit(background_image, (0, 0))
        game_win_text = font.render("Победа!", True, (255, 255, 255))
        game_win_rect = game_win_text.get_rect()
        game_win_rect.centerx = screen.get_rect().centerx
        game_win_rect.centery = screen.get_rect().centery
        screen.blit(game_win_text, game_win_rect)

        restart_text = font.render("Нажмите Enter, чтобы начать заново", True, (255, 255, 255))
        restart_rect = restart_text.get_rect()
        restart_rect.centerx = screen.get_rect().centerx
        restart_rect.centery = screen.get_rect().centery + 50
        screen.blit(restart_text, restart_rect)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            game_win = False
            platform_x = (screen_width - platform_width) // 2
            platform_y = screen_height - platform_height - 10
            ball_x = screen_width // 2
            ball_y = screen_height // 2
            ball_dx = random.choice([-3, 3])
            ball_dy = ball_speed_value

            block_list = []
            for row in range(blocks_per_column):
                for col in range(blocks_per_row):
                    block_x = horizontal_padding + col * (brick_width + horizontal_padding)
                    block_y = vertical_padding + row * (brick_height + vertical_padding)
                    block_rect = pygame.Rect(block_x, block_y, brick_width, brick_height)
                    block_list.append(block_rect)

    else:
        # Обработка движения платформы
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and platform_x > 0:
            platform_x -= platform_speed
        if keys[pygame.K_RIGHT] and platform_x < screen_width - platform_width:
            platform_x += platform_speed

        # Обработка движения мяча
        ball_x += ball_dx
        ball_y += ball_dy

        if ball_x < ball_radius or ball_x > screen_width - ball_radius:
            ball_dx *= -1
        if ball_y < ball_radius:
            ball_dy *= -1

        # Проверка столкновения мяча с платформой
        if ball_y + ball_radius > platform_y and ball_x + ball_radius >= platform_x and ball_x - ball_radius <= platform_x + platform_width:
            ball_dy *= -1

        # Проверка столкновения мяча с блоками
        for block_rect in block_list:
            if block_rect.collidepoint(ball_x, ball_y):
                block_list.remove(block_rect)
                ball_dy *= -1
                break

        # Проверка победы
        if len(block_list) == 0:
            game_win = True

        # Проверка поражения
        if ball_y > screen_height - ball_radius:
            game_over = True

        # Отрисовка элементов игры
        screen.blit(background_image, (0, 0))
        screen.blit(platform_image, (platform_x, platform_y))
        screen.blit(ball_image, (ball_x - ball_radius, ball_y - ball_radius))
        for block_rect in block_list:
            screen.blit(brick_image, block_rect)

    pygame.display.flip()
    clock.tick(60)

# Завершение Pygame
pygame.quit()
