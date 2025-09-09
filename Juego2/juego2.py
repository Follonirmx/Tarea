import pygame
import random
import sys

# Inicialización
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Juego de Recolección")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 28)

# Colores
WHITE = (255, 255, 255)
BLACK = (0 ,0 ,0)

# Jugador
player_size = 50
player_x = 400
player_y = 300
player_speed = 5
player_img = pygame.image.load("Homer.png")
player_img = pygame.transform.scale(player_img, (player_size, player_size))

# Objetos para recolectar
items = []
item_size = 30
spawn_rate = 20
item_img = pygame.image.load("Dona.png")
item_img = pygame.transform.scale(item_img, (item_size, item_size))
# Puntuación
score = 0
font = pygame.font.SysFont(None, 36)

# ====== Selección de dificultad ======
def select_difficulty():
    global spawn_rate
    selecting = True
    while selecting:
        screen.fill(WHITE)
        title = font.render("Seleccione dificultad:", True, BLACK)
        easy = font.render("1. Fácil", True, BLACK)
        medium = font.render("2. Medio", True, BLACK)
        hard = font.render("3. Difícil", True, BLACK)
        
        screen.blit(title,(250,150))
        screen.blit(easy,(300,250))
        screen.blit(medium,(300,300))
        screen.blit(hard,(300,350))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1: # Fácil
                    spawn_rate = 15
                    selecting = False
                elif event.key == pygame.K_2:  # Medio
                    spawn_rate = 25
                    selecting = False
                elif event.key == pygame.K_3:  # Difícil
                    spawn_rate = 35
                    selecting = False

# ====== Dibujar jugador y objetos ======
def draw_player(x, y):
    screen.blit(player_img, (x, y))

def draw_item(x, y):
    screen.blit(item_img, (x, y))

# ====== Lógica del juego ======
def game_loop():
    global player_x, player_y, items, score
    running = True
    items = []
    score = 0
    player_x, player_y = 400, 300
    
    while running:
        screen.fill(WHITE)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # salir con ESC
                    running = False
                
        # Movimiento del jugador
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < 800 - player_size:
            player_x += player_speed
        if keys[pygame.K_UP] and player_y > 0:
            player_y -= player_speed
        if keys[pygame.K_DOWN] and player_y < 600 - player_size:
            player_y += player_speed
            
        # Generar objetos
        if random.randint(1, spawn_rate) == 1:
            items.append([random.randint(0, 800 - item_size), random.randint(0, 600 - item_size)])
            
        # Recolectar objetos
        for item in items[:]:
            if (player_x < item[0] + item_size and
                player_x + player_size > item[0] and
                player_y < item[1] + item_size and
                player_y + player_size > item[1]):
                items.remove(item)
                score += 1
                
        # Dibujar objetos
        for item in items:
            draw_item(item[0], item[1])
            
        draw_player(player_x, player_y)
        
        # Mostrar puntuación
        score_text = font.render(f"Puntos: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))
        exit_text = font.render("Presiona ESC para salir", True, (200, 0, 0))
        screen.blit(exit_text, (500, 10))
        
        pygame.display.update()
        clock.tick(60)

# ====== Main ======
select_difficulty()
game_loop()
pygame.quit()
sys.exit()

