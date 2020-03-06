import sys, pygame
from array import *

#sprites from https://opengameart.org/content/battleships

pygame.init()

clock = pygame.time.Clock()

size = width, height = 1020, 600
speed = [2, 2]
black = 0, 0, 0
white = 255, 255, 255
red = 255, 0, 0
pale_blue = 118, 142, 181
blue = 81, 120, 181
dark_blue = 53, 88, 143
transparent = (0, 0, 0, 0)

screen = pygame.display.set_mode(size)
pygame.display.set_caption('Battleship')

gridImg = pygame.image.load('assets/grid.png')
fiveBoat = pygame.image.load('assets/fiveBoat.png')
fourBoat = pygame.image.load('assets/fourBoat.png')
threeBoat1 = pygame.image.load('assets/threeBoat1.png')
threeBoat2 = pygame.image.load('assets/threeBoat2.png')
twoBoat = pygame.image.load('assets/twoBoat.png')

boatArray = [fiveBoat, fourBoat, threeBoat1, threeBoat2, twoBoat]


#functions
def button(msg,x,y,width,height,iColor,aColor, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if (x+width > mouse[0] > x) and (y+height > mouse[1] > y):
        pygame.draw.rect(screen, aColor,(x,y,width,height))
        if click[0] == 1 and action != None:
            if action == "game_loop":
                game_loop()
            elif action == "quit":
                pygame.quit()
                quit()
    else:
        pygame.draw.rect(screen, iColor,(x,y,width,height))

    smallFont = pygame.font.Font("freesansbold.ttf",28)
    bText = smallFont.render(msg, True, white)
    bTextRect = bText.get_rect()
    bTextRect.center = ( (x+(width/2)), (y+(height/2)) )
    screen.blit(bText, bTextRect)


def game_intro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.fill(pale_blue)

        largeFont = pygame.font.Font('freesansbold.ttf', 48)
        font = pygame.font.Font('freesansbold.ttf', 28)

        titleText = largeFont.render('Battleship', True, white)
        titleTextRect = titleText.get_rect()
        titleTextRect.center = (width // 2, height // 6)

        screen.blit(titleText, titleTextRect)
        button('Say "Start" to begin game', 300, 300, 400 ,50, blue, dark_blue, "game_loop")

        pygame.display.update()
        clock.tick(60)


def game_loop():
    screen.fill(blue)

    titleFont = pygame.font.Font('freesansbold.ttf', 20)

    ybText = titleFont.render('Your Board', True, white)
    ybTextRect = ybText.get_rect()
    ybTextRect.center = (width // 4, 20)

    obText = titleFont.render('Opponent Board', True, white)
    obTextRect = obText.get_rect()
    obTextRect.center = (750, 20)

    screen.blit(ybText, ybTextRect)
    screen.blit(obText, obTextRect)

    #temporary placement of opponent battleships
    opponentShips = [[0,1,1,1,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0],
                    [1,0,0,0,0,0,0,0,0,0],
                    [1,0,0,0,0,0,0,0,0,0],
                    [1,0,0,0,0,0,1,1,0,0],
                    [1,0,0,0,0,0,0,0,0,0],
                    [1,0,0,0,0,0,0,0,0,1],
                    [0,0,1,1,1,1,0,0,0,1],
                    [0,0,0,0,0,0,0,0,0,1],
                    [0,0,0,0,0,0,0,0,0,0]]

    userShips = [[0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0]]

    gameExit = False
    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.blit(gridImg, (15,40))
        screen.blit(gridImg, (570, 40))

        #user places their boats

        screen.blit(boatArray[0], (width // 2 - 10, 200))

        bpText = titleFont.render('Will your 5 boat be horizontal or vertical?', True, black)
        bpTextRect = bpText.get_rect()
        bpTextRect.center = (width // 2, height // 2 + 200)
        screen.blit(bpText, bpTextRect)





        pygame.display.update()
        clock.tick(60)


game_intro()
game_loop()
pygame.quit()
quit()
