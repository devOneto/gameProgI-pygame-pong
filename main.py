import random
import pygame
import sys

# colors
blue = (0,0,120)
white = (200,200,200)

# Inicialização
pygame.init()
clock = pygame.time.Clock()

# Configurando a janela
screenWidth = 1280
screenHeight = 960
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('Pong')

# Objetos
ball = pygame.Rect(screenWidth / 2 - 15, screenHeight / 2 - 15, 30, 30)
player = pygame.Rect(screenWidth - 20, screenHeight / 2 - 70, 10, 140)
opponent = pygame.Rect(10, screenHeight / 2 - 70, 10, 140)

# variaveis
ballSpeedX = 0.5  # 500 pixels por segundo
ballSpeedY = 0.5
opponentSpeed = 10

# scores
playerScore = 0
opponentScore = 0

#load font
font = pygame.font.SysFont('arial', 50)

def inputs():
    # Processando as entradas (eventos)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    (x, y) = pygame.mouse.get_pos()
    player.y = y - 70


def draw():

    global opponentScore, playerScore

    # Desenho
    screen.fill((0, 0, 0))
    pygame.draw.ellipse(screen, (200, 200, 200), ball)
    pygame.draw.rect(screen, (200, 200, 200), player)
    pygame.draw.rect(screen, (200, 200, 200), opponent)
    pygame.draw.line(screen, white, (screenWidth/2, 0), (screenWidth/2, screenHeight), 5)

    # Atualizando a janela 60fps
    pygame.display.flip()

    # Render Text
    # Opponent Score
    opponentScoreText = font.render( str(opponentScore) , True, white)
    screen.blit(opponentScoreText, (screenWidth/2 - 65, 50))
    # Player Score
    playerScoreText = font.render( str(playerScore) , True, white)
    screen.blit(playerScoreText, (screenWidth/2 + 40, 50))

    pygame.display.update()

def resetBall():
    global ballSpeedX, ballSpeedY
    ball.center = (screenWidth / 2, screenHeight / 2)
    ballSpeedX = random.choice((-0.5, 0.5))


def update(dt):
    global ballSpeedX, ballSpeedY, opponentScore, playerScore
    # Atualizacao
    #dt = clock.tick(120)
    ball.x += ballSpeedX * dt
    ball.y += ballSpeedY * dt

    if opponent.bottom < ball.y:
        opponent.bottom += opponentSpeed
    if opponent.top > ball.y:
        opponent.top -= opponentSpeed

    if ball.top <= 0 or ball.bottom >= screenHeight:
        ballSpeedY *= -1

    if ball.left >= screenWidth:
        opponentScore += 1
        resetBall()
    if ball.right <= 0:
        playerScore += 1
        resetBall()

    if ball.bottom >= opponent.top and ball.top <= opponent.bottom and ball.left <= opponent.right:
        delta = ball.centery - opponent.centery
        ballSpeedY = delta * 0.01
        ballSpeedX *= -1
    if ball.bottom >= player.top and ball.top <= player.bottom and ball.right >= player.left:
        delta = ball.centery - player.centery
        ballSpeedY = delta * 0.01
        ballSpeedX *= -1


previous = pygame.time.get_ticks()
lag = 0
FPS = 500
MS_PER_UPDATE = 1000/FPS

while True:
    current = pygame.time.get_ticks()
    elapsed = current - previous
    previous = current
    lag += elapsed

    #Entradas
    inputs()
    while lag >= MS_PER_UPDATE:
        # Atualização
        update(MS_PER_UPDATE)
        lag -= MS_PER_UPDATE
    #Desenho
    draw()