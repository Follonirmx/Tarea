import pygame
import random
import sys

# Inicialización
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Juego de Disparos")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 28)

# Colores
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Jugador
player_size = 50
player_x = 400
player_y = 500
player_speed = 5

# Balas
bullets = []
bullet_speed = 7

# Enemigos
enemies = []
enemy_size = 40
enemy_speed = 2
spawn_rate = 30  

# Puntuación
score = 0

# ====== Menú de dificultad ======
def select_difficulty():
    global enemy_speed, spawn_rate
    selecting = True
    while selecting:
        screen.fill(WHITE)
        title = font.render("Selecciona dificultad:", True, BLACK)
        easy = font.render("1. Fácil", True, BLACK)
        medium = font.render("2. Medio", True, BLACK)
        hard = font.render("3. Difícil", True, BLACK)
        exit_game = font.render("ESC. Salir", True, (200, 0, 0))

        screen.blit(title, (250, 150))
        screen.blit(easy, (300, 250))
        screen.blit(medium, (300, 300))
        screen.blit(hard, (300, 350))
        screen.blit(exit_game, (300, 400))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:  # Fácil
                    enemy_speed = 2
                    spawn_rate = 35
                    selecting = False
                elif event.key == pygame.K_2:  # Medio
                    enemy_speed = 4
                    spawn_rate = 25
                    selecting = False
                elif event.key == pygame.K_3:  # Difícil
                    enemy_speed = 6
                    spawn_rate = 15
                    selecting = False
                elif event.key == pygame.K_ESCAPE:  # Salir
                    pygame.quit()
                    sys.exit()

# Funciones de dibujo
def draw_player(x, y):
    pygame.draw.rect(screen, BLUE, (x, y, player_size, player_size))

def draw_enemy(x, y):
    pygame.draw.circle(screen, RED, (x + enemy_size//2, y + enemy_size//2), enemy_size//2)

def draw_bullet(x, y):
    pygame.draw.rect(screen, BLACK, (x, y, 5, 10))

# ====== Lógica del juego ======
def game_loop():
    global player_x, player_y, bullets, enemies, score
    running = True
    bullets = []
    enemies = []
    score = 0
    player_x, player_y = 400, 500

    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullets.append([player_x + player_size//2 - 2, player_y])
                if event.key == pygame.K_ESCAPE:  
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

        # Mover enemigos y comprobar colisión con el jugador
        for enemy in enemies[:]:
            enemy[1] += enemy_speed
            if enemy[1] > 600:
                enemies.remove(enemy)
            else:
                draw_enemy(enemy[0], enemy[1])

            # Colisión enemigo 
            if (player_x < enemy[0] + enemy_size and
                player_x + player_size > enemy[0] and
                player_y < enemy[1] + enemy_size and
                player_y + player_size > enemy[1]):
                running = False  

        # Mover balas
        for bullet in bullets[:]:
            bullet[1] -= bullet_speed
            if bullet[1] < 0:
                bullets.remove(bullet)
            else:
                draw_bullet(bullet[0], bullet[1])

        # Detectar colisiones bala-enemigo
        for bullet in bullets[:]:
            for enemy in enemies[:]:
                if (bullet[0] < enemy[0] + enemy_size and
                    bullet[0] + 5 > enemy[0] and
                    bullet[1] < enemy[1] + enemy_size and
                    bullet[1] + 10 > enemy[1]):
                    if bullet in bullets:
                        bullets.remove(bullet)
                    if enemy in enemies:
                        enemies.remove(enemy)
                        score += 1  

        # Dibujar jugador
        draw_player(player_x, player_y)

        # Mostrar puntuación
        score_text = font.render(f"Puntos: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        pygame.display.update()
        clock.tick(60)

# ====== Main ======
while True:
    select_difficulty()
    game_loop()

