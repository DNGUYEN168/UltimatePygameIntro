import pygame as pg
# from sys import exit

pg.init()

screen = pg.display.set_mode((800,400))   
pg.display.set_caption('Running Game')
game_active = True

#TEXT 

font = pg.font.Font('UltimatePygameIntro/font/Pixeltype.ttf', 50)

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


# END SCREEN

player_surface_dead = pg.image.load('UltimatePygameIntro/graphics/Player/player_stand.png').convert_alpha()
player_surface_dead_rect = player_surface_dead.get_rect(center = (400,200))
text_game_surface = font.render('Game Over', False, 'black')
# GRAVITY 

player_gravity = 1

# SCORE / TEXT 
start_time = 0

def display_score():
    current_time = int(pg.time.get_ticks() / 1000) - start_time   # LOOK INTO THIS FOR TRAINING 
    score_surface = font.render(f'Score: {current_time}', False, 'black')
    score_rect = score_surface.get_rect(center = (400,50))
    screen.blit(score_surface, score_rect)

    




Done = False
while not Done:
    clock.tick(60)

    for event in pg.event.get():
        # get method retrieves all the events 
        if event.type == pg.QUIT:  # checks when player presses the x button 
            pg.quit()  # quits the game, but still keeps the while loop running 
            Done = True



        # Keybord Input
        if game_active:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    if player_rect.bottom == 300:
                        player_gravity = -20
        else:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    game_active = True
                    snail_rect.left = 850
                    start_time = int(pg.time.get_ticks() / 1000)

    if game_active:
        screen.blit(sky_surface, (0,0))
        screen.blit(ground_surface, (0,300))
        display_score()


        # SNAIL MOVEMENT AND RESET
        snail_rect.left -= 5

        if snail_rect.left < -100:
            snail_rect.left = 850
        screen.blit(snail_surface, snail_rect)


        # PLAYER ANIMATION 

        player_gravity += 1
        player_rect.bottom += player_gravity

        # COLLISION / FLOOR
        if player_rect.bottom > 300:
            player_rect.bottom = 300

        screen.blit(player_surface, player_rect)


        if player_ani_frame == 420:
            player_surface = player_walk1_surface
        if player_ani_frame == 840:
            player_surface = player_walk2_surface
            player_ani_frame = 0
        player_ani_frame += 15


        if player_rect.colliderect(snail_rect):
            game_active = False

    
    # GAME OVER STATE 

    else:  # what will happen when we die 
        screen.fill('#99E793')
        screen.blit(player_surface_dead, player_surface_dead_rect)
        screen.blit(text_game_surface, (400,50))


    pg.display.update()


    #KEY INPUT 

    # keys = (pg.key.get_pressed())  # we treat this like a dict 
    # if keys[pg.K_SPACE]:
    #     print("JUMP")
    # if keys[pg.K_w]:
    #     player_rect.top -= 5
    # if keys[pg.K_s]:
    #     player_rect.top += 5
    # if keys[pg.K_a]:
    #     player_rect.left -= 5
    # if keys[pg.K_d]:
    #     player_rect.left += 5



    # if event.type == pg.MOUSEBUTTONDOWN:
    #     if player_rect.collidepoint(event.pos):
    #         player_gravity = -20
