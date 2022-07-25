import pygame as pg, sys, random

def draw_floor():  # continuosly moving base
    screen.blit(floorsurface, (floor_x_pos, 900))  # sets floor image
    screen.blit(floorsurface, (floor_x_pos+576, 900))  # sets floor image

def create_pipe():  # creates pipesurface
    randpipeheigth = random.choice(pipeheight)
    bottom_pipe = pipesurface.get_rect(midtop=(700, randpipeheigth))
    top_pipe = pipesurface.get_rect(midbottom=(700, randpipeheigth-300))
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes

def drawpipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 1024:
            screen.blit(pipesurface, pipe)
        else:
            flippipe = pg.transform.flip(pipesurface, False, True)
            screen.blit(flippipe, pipe)

def collisionpipe(pipes):
    for pipe in pipes:
        if birdrect.colliderect(pipe):
            deathsound.play()  # plays death sound when collision happens
            return False      # if bird collides pipe return false

    if birdrect.top <= -100 or birdrect.bottom >= 900:
        deathsound.play()
        return False     # if bird goes out of screen return False

    return True

def rotate_bird(bird):
    newbird = pg.transform.rotozoom(bird, -bird_movement*5, 1)
    return newbird

def birdanimation():
    newbird = birdframe[birdindex]
    newbirdrect = newbird.get_rect(center=(100, birdrect.centery))
    return newbird, newbirdrect

def scoredisp(gamestate):
    if gamestate == 'maingame':
        scoresurface = gamefont.render(str(int(score)), True, (255, 255, 255))
        scorerect = scoresurface.get_rect(center=(288, 100))
        screen.blit(scoresurface, scorerect)
    if gamestate == 'gameover':
        scoresurface = gamefont.render(f'Score: {int(score)}', True, (255, 255, 255))
        scorerect = scoresurface.get_rect(center=(288, 100))
        screen.blit(scoresurface, scorerect)

        highscoresurface = gamefont.render(f'High Score: {int(highscore)}', True, (255, 255, 255))
        highscorerect = highscoresurface.get_rect(center=(288, 850))
        screen.blit(highscoresurface, highscorerect)

def updatescore(score, highscore):
    if score > highscore:
        highscore = score
    return highscore

def scorecheck():
    global score, canscore
    if pipelist:
        for pipe in pipelist:
            if 95 < pipe.centerx < 105 and canscore == True:
                score += 1
                scoresound.play()
                canscore = False
            if pipe.centerx < 0:
                canscore = True

pg.init()  # Starts pygame

screen = pg.display.set_mode((576, 1024))  # Sets screen size
pg.display.set_caption('Flappy Bird')
clock = pg.time.Clock()  # Sets time variable
gamefont = pg.font.Font('flappy bird/assets/04B_19.TTF' ,40)

# game variable

gravity = 0.25
bird_movement = 0

gameactive = True

score = 0
highscore = 0
canscore = True

bgsurface = pg.image.load('flappy bird/assets/background-day.png').convert()  # adress of bg image and .convert() to convert image into more workable form
bgsurface = pg.transform.scale2x(bgsurface)  # scale screen to 2 times

floorsurface = pg.image.load('flappy bird/assets/base.png').convert()
floorsurface = pg.transform.scale2x(floorsurface)

birddown = pg.image.load('flappy bird/assets/redbird-downflap.png').convert_alpha()
birddown = pg.transform.scale2x(birddown)
birdmid = pg.image.load('flappy bird/assets/redbird-midflap.png').convert_alpha()
birdmid = pg.transform.scale2x(birdmid)
birdup = pg.image.load('flappy bird/assets/redbird-upflap.png').convert_alpha()
birdup = pg.transform.scale2x(birdup)

birdframe = [birddown, birdmid, birdup]
birdindex = 0
birdsurface = birdframe[birdindex]

# birdsurface = pg.image.load('/users/soumik/desktop/python/flappybird/bluebird-midflap.png').convert_alpha()
# birdsurface = pg.transform.scale2x(birdsurface)

birdrect = birdsurface.get_rect(center=(100, 512))  # puts a rectangle around the bird, rectangles detect collisions, bird should detect collisions with pipes
BIRDFLAP = pg.USEREVENT + 1
pg.time.set_timer(BIRDFLAP, 200)

pipesurface = pg.image.load('flappy bird/assets/pipe-green.png').convert()
pipesurface = pg.transform.scale2x(pipesurface)
pipelist = []
SPAWNPIPE = pg.USEREVENT  # creates user event

pg.time.set_timer(SPAWNPIPE, 1200)  # sets timer to spawn pipes every 1200 ms

pipeheight = [400, 600, 800]

gameoversurf = pg.image.load('flappy bird/assets/message.png').convert_alpha()
gameoversurf = pg.transform.scale2x(gameoversurf)
gameoverrect = gameoversurf.get_rect(center=(288, 512))

flapsound = pg.mixer.Sound('flappy bird/assets/sound_sfx_wing.wav')
deathsound = pg.mixer.Sound('flappy bird/assets/sound_sfx_hit.wav')
scoresound = pg.mixer.Sound('flappy bird/assets/sound_sfx_point.wav')

floor_x_pos = 0
countdown = 100

while True:  # main game loop
    for event in pg.event.get():  # event loop for all game events like moving mouse or clicking any button
        if event.type == pg.QUIT:  # pg.QUIT is the cross button
            pg.quit()  # quits pygame
            sys.exit()  # exits the main game loop

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:  # bird movement when space bar is pressed
                bird_movement = -10
                #bird_movement -= 10
                flapsound.play()
            if event.key == pg.K_SPACE and gameactive == False:  # to end game when collision happens
                gameactive = True
                pipelist.clear()
                birdrect.center = (100, 512)
                bird_movement = 0
                score = 0

        if event.type == SPAWNPIPE:
            pipelist.extend(create_pipe())

        if event.type == BIRDFLAP:
            if birdindex < 2:
                birdindex += 1
            else:
                birdindex = 0

            birdsurface, birdrect = birdanimation()

    screen.blit(bgsurface, (0, 0))  # sets background image
    if gameactive:    # bird and pipes are shown till gameactive is true, it becomes false when collision happens
    # bird movement
        bird_movement += gravity  # bird falls down every movement
        rotatedbird = rotate_bird(birdsurface)
        birdrect.centery += bird_movement  # moves bird along center y axis
        screen.blit(rotatedbird, birdrect)  # sets bird with rectangle
        gameactive = collisionpipe(pipelist)

    # pipes
        pipelist = move_pipes(pipelist)
        drawpipes(pipelist)

    # display score
        scorecheck()
        scoredisp('maingame')


    else:
        screen.blit(gameoversurf, gameoverrect )
        highscore = updatescore(score, highscore)
        scoredisp('gameover')

# floor
    floor_x_pos -= 1  # moves the base left
    draw_floor()
    if floor_x_pos <= -576:
        floor_x_pos = 0

    pg.display.update()  # updates screen
    clock.tick(120)  # frame speed to 120 fps