import pygame as pg
# from sys import exit

pg.init()

screen = pg.display.set_mode((800,400))   
pg.display.set_caption('Running Game')

# CREATE A FLOOR / CEILING FOR FPS 
clock = pg.time.Clock()


# BACKGROUND 
sky_surface = pg.image.load('UltimatePygameIntro/graphics/Sky.png').convert()
ground_surface = pg.image.load('UltimatePygameIntro/graphics/ground.png').convert()


# ENTITIES 

snail_surface = pg.image.load('UltimatePygameIntro/graphics/snail/snail1.png').convert_alpha()
snail_rect = snail_surface.get_rect(midbottom = (850,300))

# PLAYER ANIMATION 
player_ani_frame = 0

player_surface = pg.image.load('UltimatePygameIntro/graphics/Player/player_stand.png').convert_alpha()
player_walk1_surface =  pg.image.load('UltimatePygameIntro/graphics/Player/player_walk_1.png').convert_alpha()
player_walk2_surface =  pg.image.load('UltimatePygameIntro/graphics/Player/player_walk_2.png').convert_alpha()
player_rect = player_surface.get_rect(midbottom = (50,300))

Done = False
while not Done:
    clock.tick(60)
    for event in pg.event.get():
        # get method retrieves all the events 
        if event.type == pg.QUIT:  # checks when player presses the x button 
            pg.quit()  # quits the game, but still keeps the while loop running 
            Done = True

    screen.blit(sky_surface, (0,0))
    screen.blit(ground_surface, (0,300))

    # SNAIL MOVEMENT AND RESET
    snail_rect.left -= 5

    if snail_rect.left < -100:
        snail_rect.left = 850
    screen.blit(snail_surface, snail_rect)




    # PLAYER ANIMATION 
    if player_ani_frame == 420:
        player_surface = player_walk1_surface
    if player_ani_frame == 840:
        player_surface = player_walk2_surface
        player_ani_frame = 0
    screen.blit(player_surface, player_rect)

    player_ani_frame += 15


    if player_rect.colliderect(snail_rect):
        print('collide')
        

    pg.display.update()

