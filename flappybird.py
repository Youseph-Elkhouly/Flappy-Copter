# --------------------------------------- import
import pygame
import random
import os
from pygame import*
from pygame import mixer
import sys
# --------------------------------------- screen
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" %(20, 20)
pygame.init()
SIZE = width, height = 540, 960
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Flappy Bird")

running = True

#clock and fps
clock = pygame.time.Clock()
fps = 60

#colours
white = (255, 255, 255)
blue = (0, 0, 255)

#scroll variables
ground_scroll = 0
scroll_speed = 3

#score variables
score = 0
score_up = False

#game state variables
STATE_MENU = 0
STATE_GAME = 1
state = STATE_MENU

#-----------------------------------------------------functions
#gets the rect of the generated pillars
def create_pillar():
    pillar_position = random.choice(pillar_height_list)
    new_pillar = bottompillar_pic.get_rect(midtop = (620, pillar_position))
    new_pillar1 = toppillar_pic.get_rect(midbottom = (620, pillar_position - 150))
    return new_pillar, new_pillar1
#function which moves the created pillars
def move_pillar(pillar):
    for i in pillar:
        i.centerx -= scroll_speed
    return pillar
#function that draws the pillars on the screen
def draw_pillar(pillar):
    for i in pillar:
        if i.bottom >= 800:
            screen.blit(bottompillar_pic, i)
        else:
            flip_pillar = pygame.transform.flip(toppillar_pic, False, True)
            screen.blit(toppillar_pic, i)
#function that checks for pipe collisions
def collision(pillar):
    for i in pillar:
        if helicopter.colliderect(i):
            return True

        

#gets the rect for the generated garbage bags
def create_garbage_bag():
    new_garbage_bag = garbage_bag_pic.get_rect(center = (900, 660))
    return new_garbage_bag
#moves garbage bags
def move_garbage_bag(bag):
    for i in bag:
        i.centerx -= scroll_speed
    return bag
#draws garbage bags
def draw_garbage_bag(bag):
    global score_up
    for i in bag:
        if i.centerx >=100:
            screen.blit(garbage_bag_pic, i)
        if i.centerx == 102:
            point_sound.play()
            score_up = True
        
#text function        
def text(s, z, c, x, y):
    freesansbold = pygame.font.Font('freesansbold.ttf', s)
    surface = freesansbold.render(z, True, (c))
    screen.blit(surface, (x, y))        
            

#--------------------------------------------------- loading and scaling images
floor_pic = pygame.image.load('floor.jpeg').convert()
floor = pygame.transform.scale(floor_pic, (540, 540))
floor_pic2 = pygame.image.load('floor.jpeg').convert()
floor2 = pygame.transform.scale(floor_pic2, (540, 540))

helicopter_pic = pygame.image.load('helicopter.png')
helicopter_pic = pygame.transform.scale(helicopter_pic, (51, 36))
helicopter = helicopter_pic.get_rect(center = (100, 400))
crash_helicopter_pic = pygame.image.load('crashedhelicopter.png')
crash_helicopter_pic = pygame.transform.scale(crash_helicopter_pic, (100, 100))

bg_pic = pygame.image.load('background.jpeg').convert()
bg = pygame.transform.scale(bg_pic, (540, 960))

start_button_pic = pygame.image.load('instructions.png')
start_button_pic = pygame.transform.scale(start_button_pic, (300, 300))
start_button = start_button_pic.get_rect(center = (270, 550))
logo = pygame.image.load('press.png')
logo = pygame.transform.scale(logo, (300, 300))

toppillar_pic = pygame.image.load('toppillargame.png')
toppillar_pic = pygame.transform.scale(toppillar_pic, (69, 750))
bottompillar_pic = pygame.image.load('bottompillargame.png')
bottompillar_pic = pygame.transform.scale(bottompillar_pic, (69, 750))


garbage_bag_pic = pygame.image.load('garbagebag.png')
garbage_bag_pic = pygame.transform.scale(garbage_bag_pic, (100, 100))
#lists
garbage_bag_list = []
pillar_list = []

#userevents that are used to generate objects after a specific time
LOADPILLAR = pygame.USEREVENT
pygame.time.set_timer(LOADPILLAR, 2000)

LOADGARBAGE = pygame.USEREVENT
pygame.time.set_timer(LOADGARBAGE, 3000)


#different heights that the pillars can be generated into which are randomly chosen by the function above
pillar_height_list = [250, 300, 350, 400, 450, 500, 550, 600, 650]

#sounds
jump_sound = mixer.Sound('wing.mp3')
death_sound = mixer.Sound('crashsound.wav')
point_sound = mixer.Sound('point.mp3')


#bird movement variable; changes the height of the bird when altered
bird_movement = 0

#------------------------------------------------------- game loop
while running:
    #fps stabalizer
    clock.tick(fps)     
    #event checker
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
            pygame.quit()
            sys.exit()
        #initiates functions everytime the timed uservent is activated
        if event.type == LOADPILLAR:
            pillar_list.extend(create_pillar())
        if event.type == LOADGARBAGE:
            garbage_bag_list.append(create_garbage_bag())
        if event.type == KEYDOWN:
            #quits game when escape is pressed
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            #when space is pressed the game starts, it also increases the birds height and plays a sound
            if event.key == K_SPACE:
                if state == STATE_MENU:
                    state = STATE_GAME
                if state == STATE_GAME:
                    jump_sound.play()
                    bird_movement = 0
                    bird_movement -= 8
    #---------------------------------- menu state
    if state == STATE_MENU:
        #resets variables when player dies
        helicopter.centery = 400
        pillar_list.clear()
        garbage_bag_list.clear()
        score = 0
        #rendering images on screen
        screen.blit(bg, (0, -200))
        screen.blit(floor, (ground_scroll, 700))
        screen.blit(floor2, (ground_scroll + 540, 700))
        screen.blit(helicopter_pic, (50, 360))
        screen.blit(start_button_pic, start_button)
        screen.blit(logo, (120, 80))
        
            
    #------------------------------------------ game state
    if state == STATE_GAME:
        #background rendering
        screen.blit(bg, (0, -200))
        #creating and moving pillars
        pillar_list = move_pillar(pillar_list)
        draw_pillar(pillar_list)
        #creating and moving garbage bags
        garbage_bag_list = move_garbage_bag(garbage_bag_list)
        draw_garbage_bag(garbage_bag_list)
        collide_check = collision(pillar_list)
        #game ends and death sound is played if player hits a pipe
        if collide_check == True:
            death_sound.play()
            state = STATE_MENU
        #rendering the moving floor
        screen.blit(floor, (ground_scroll, 700))
        screen.blit(floor2, (ground_scroll + 540, 700))
        ground_scroll -= scroll_speed
        #scroll effect for the floor
        if ground_scroll < -540:
            ground_scroll = 0
        #gravity effect for bird
        bird_movement += 0.5
        helicopter.centery += bird_movement
        #game ends if player hits the floor or goes too high, plays death sound
        if helicopter.centery >= 685 or helicopter.centery <= -50: 
            death_sound.play()
            state = STATE_MENU
        if helicopter.centery < 685:
            screen.blit(helicopter_pic, helicopter)
        #score system and score display
        if score_up == True:
            score += 1
            score_up = False
        score1 = str(score)
        text(20, score1, white, 20, 20)
    pygame.display.update()


