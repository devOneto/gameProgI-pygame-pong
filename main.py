import random
import pygame
import sys

# colors
blue = (0,0,120)
white = (200,200,200)
pureWhite = (255,255,255)

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
opponentSpeed = 1

# scores
playerScore = 0
opponentScore = 0

#load font
font = pygame.font.SysFont('arial', 50)
bigFont = pygame.font.SysFont('arial', 200)

# Start and Finish Screen Flag
onStartScreen = True
onGameOverScreen = False

def inputs():
    global onStartScreen
    # Processando as entradas (eventos)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONUP and onStartScreen:
            onStartScreen = False

    (x, y) = pygame.mouse.get_pos()
    player.y = y - 70


def draw():

    global opponentScore, playerScore, onGameOverScreen

    screen.fill((0, 0, 0))

    if onStartScreen:
        welcomeText = bigFont.render(str("P0NG"), True, pureWhite)
        pressAnyKeyText = font.render(str("Click to Start..."), True, pureWhite)
        screen.blit(welcomeText, (screenWidth / 2 - 270, screenHeight/2 - 150))
        screen.blit(pressAnyKeyText, (screenWidth / 2 - 200, screenHeight/2 +50) )
        pygame.display.flip()
    elif onGameOverScreen:
        endText = bigFont.render(str("GameOver"), True, pureWhite)
        screen.blit(endText, (140, 330))
        pygame.display.flip()
    else:
        # Desenho
        pygame.draw.ellipse(screen, (200, 200, 200), ball)
        pygame.draw.rect(screen, (200, 200, 200), player)
        pygame.draw.rect(screen, (200, 200, 200), opponent)
        pygame.draw.line(screen, white, (screenWidth / 2, 0), (screenWidth / 2, screenHeight), 5)

        # Atualizando a janela 60fps
        pygame.display.flip()

        # Render Text
        # Opponent Score
        opponentScoreText = font.render(str(opponentScore), True, white)
        screen.blit(opponentScoreText, (screenWidth / 2 - 65, 50))
        # Player Score
        playerScoreText = font.render(str(playerScore), True, white)
        screen.blit(playerScoreText, (screenWidth / 2 + 40, 50))

    pygame.display.update()

def resetBall():
    global ballSpeedX, ballSpeedY
    ball.center = (screenWidth / 2, screenHeight / 2)
    ballSpeedX = random.choice((-0.5, 0.5))


def update(dt):
    global ballSpeedX, ballSpeedY, opponentScore, playerScore, onGameOverScreen, opponentSpeed

    ball.x += ballSpeedX * dt
    ball.y += ballSpeedY * dt

    # Opponent AI
    if opponent.bottom < ball.y and ball.x < screenWidth/2:
        opponent.y += opponentSpeed
    if opponent.top > ball.y and ball.x < screenWidth/2:
        opponent.y -= opponentSpeed

    # Bound
    if ball.top <= 0 or ball.bottom >= screenHeight:
        ballSpeedY *= -1

    # Score Marks
    if ball.left >= screenWidth:
        opponentScore += 1
        resetBall()
    if ball.right <= 0:
        playerScore += 1
        resetBall()

    # Game Over
    if playerScore == 3 or opponentScore == 3:
        onGameOverScreen = True

    # Colision opponent and ball
    if ball.colliderect(opponent):
        ballSpeedX *= -1.05
    # Colision player and ball
    if ball.colliderect(player):
        ballSpeedX *= -1.05
    # Max Ball Speed
    if(ballSpeedX>1.5):
        ballSpeedX = 1.5


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
