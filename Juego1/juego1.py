import pygame
import random
import sys

# Inicialización
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Juego de Evasión")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 28)

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Jugador
player_size = 50
player_x = 400
player_y = 500
player_speed = 5
player_img = pygame.image.load("gato1.png")
player_img = pygame.transform.scale(player_img, (player_size, player_size))

# Enemigos
enemies = []
enemy_speed = 3
spawn_rate = 20
enemy_size = 30
enemy_img = pygame.image.load("gota.png")
enemy_img = pygame.transform.scale(enemy_img, (enemy_size, enemy_size))


# Puntuación
score = 0


# ====== Menú Principal ======
def main_menu():
    while True:
        screen.fill(WHITE)
        title = font.render("MENU PRINCIPAL", True, BLACK)
        play = font.render("1. Jugar", True, BLACK)
        quit_game = font.render("2. Salir", True, BLACK)

        screen.blit(title, (280, 150))
        screen.blit(play, (320, 250))
        screen.blit(quit_game, (320, 300))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    select_difficulty()
                    game_loop()
                elif event.key == pygame.K_2:
                    pygame.quit()
                    sys.exit()


# ====== Selección de dificultad ======
def select_difficulty():
    global enemy_speed, spawn_rate, enemy_size
    selecting = True
    while selecting:
        screen.fill(WHITE)
        title = font.render("Selecciona dificultad:", True, BLACK)
        easy = font.render("1. Fácil", True, BLACK)
        medium = font.render("2. Medio", True, BLACK)
        hard = font.render("3. Difícil", True, BLACK)

        screen.blit(title, (250, 150))
        screen.blit(easy, (300, 250))
        screen.blit(medium, (300, 300))
        screen.blit(hard, (300, 350))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    enemy_speed = 3
                    spawn_rate = 25
                    selecting = False
                elif event.key == pygame.K_2:
                    enemy_speed = 5
                    spawn_rate = 20
                    selecting = False
                elif event.key == pygame.K_3:
                    enemy_speed = 7
                    spawn_rate = 15
                    selecting = False


# ====== Dibujar jugador y enemigo ======
def draw_player(x, y):
    

def draw_enemy(x, y):
    screen.blit(enemy_img, (x, y))


# ====== Lógica del juego ======
def game_loop():
    global player_x, player_y, enemies, score
    enemies = []
    player_x, player_y = 400, 500
    score = 0
    running = True
    start_ticks = pygame.time.get_ticks()

    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Movimiento del jugador
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < 800 - player_size:
            player_x += player_speed

        # Generar enemigos
        if random.randint(1, spawn_rate) == 1:
            enemies.append([random.randint(0, 800 - enemy_size), 0])

        # Mover y dibujar enemigos
        for enemy in enemies[:]:
            enemy[1] += enemy_speed
            if enemy[1] > 600:
                enemies.remove(enemy)
            else:
                draw_enemy(enemy[0], enemy[1])

            # Detectar colisiones
            if (player_x < enemy[0] + enemy_size and
                player_x + player_size > enemy[0] and
                player_y < enemy[1] + enemy_size and
                player_y + player_size > enemy[1]):
                running = False

        draw_player(player_x, player_y)

        # Actualizar puntuación (por segundos)
        seconds = (pygame.time.get_ticks() - start_ticks) // 1000
        score = seconds
        text = font.render(f"Puntuación: {score}", True, BLACK)
        screen.blit(text, (10, 10))

        pygame.display.update()
        clock.tick(60)

    # Cuando se pierde → volver al menú principal
    main_menu()


# ====== Main ======
main_menu()

