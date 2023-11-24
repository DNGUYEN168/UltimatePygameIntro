import pygame as pg
# from sys import exit
import random  # use this to decide a rand speed for snail / fly  
import neat

def run_game(genomes, config):
    pg.init()

    screen = pg.display.set_mode((800,400))   
    pg.display.set_caption('Running Game')
    # game_active = True

    #TEXT 

    font = pg.font.Font('font/Pixeltype.ttf', 50)

    # CREATE A FLOOR / CEILING FOR FPS 
    clock = pg.time.Clock()

    # CENTER 


    # BACKGROUND 
    sky_surface = pg.image.load('graphics/Sky.png').convert()
    ground_surface = pg.image.load('graphics/ground.png').convert()


    # ENTITIES 
    snail_surface = pg.image.load('graphics/snail/snail1.png').convert_alpha()
    snail_rect = snail_surface.get_rect(midbottom = (850,300))

    # PLAYER ANIMATION 
    player_ani_frame = 0
    player_alive = True
    player_surface = pg.image.load('graphics/Player/player_stand.png').convert_alpha()
    player_walk1_surface =  pg.image.load('graphics/Player/player_walk_1.png').convert_alpha()
    player_walk2_surface =  pg.image.load('graphics/Player/player_walk_2.png').convert_alpha()
    player_rect = player_surface.get_rect(midbottom = (50,300))


    # END SCREEN

    player_surface_dead = pg.image.load('graphics/Player/jump.png').convert_alpha()
    player_surface_dead_rect = player_surface_dead.get_rect(center = (400,150))
    text_game_surface = font.render('Game Over', False, 'black')
    text_game_surface_rect = text_game_surface.get_rect(center = (400,50))
    text_game_surface_restart = font.render('Press Space to Start Again', False, 'black')
    text_game_surface_rect_restart = text_game_surface_restart.get_rect(center = (400,300))

    # GRAVITY 

    player_gravity = 1

    # SCORE / TEXT 
    start_time = 0

    def display_score():
        current_time = int(pg.time.get_ticks() / 1000) - start_time   # LOOK INTO THIS FOR TRAINING 
        score_surface = font.render(f'Score: {current_time}', False, 'black')
        score_rect = score_surface.get_rect(center = (400,50))
        screen.blit(score_surface, score_rect)

        
    # PREPING NEAT 
    nets = []
    for i, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        g.fitness = 0


    Done = False
    while not Done:
        clock.tick(60)

        for event in pg.event.get():
            # get method retrieves all the events 
            if event.type == pg.QUIT:  # checks when player presses the x button 
                pg.quit()  # quits the game, but still keeps the while loop running 
                Done = True

            # NEAT

            # Keybord Input
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    if player_rect.bottom == 300:
                        player_gravity = -20



        

            # else:
            #     if event.type == pg.KEYDOWN:
            #         if event.key == pg.K_SPACE:
            #                 # game_active = True
            #             snail_rect.left = 850
            #             start_time = int(pg.time.get_ticks() / 1000)


        screen.blit(sky_surface, (0,0))
        screen.blit(ground_surface, (0,300))
        


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

        dist =pg.math.Vector2(player_rect.center).distance_to((snail_rect.center)) # dist from snail to player 
        text_game_surface_restart = font.render(f'{dist}', False, 'black')
        screen.blit(text_game_surface_restart, (0,0))

        if player_rect.colliderect(snail_rect):  # this has to be somehwere in the reward 
            #     game_active = False 
            start_time = int(pg.time.get_ticks() / 1000)   
            snail_rect.left = 850
            player_alive = False
        display_score()

        # NEAT 

        for i in (nets):
            output = i.activate([dist])
            choice = output.index(max(output))
            if choice == 1:
                if player_rect.bottom == 300:
                    player_gravity = -20
            if choice == 0:
                player_rect.bottom == 300

        if not player_alive:
            break
        else:
            genomes[0][1].fitness += start_time / 60

        


        

        pg.draw.line(screen,'black', player_rect.center, snail_rect.center,1)


        
        




        # GAME OVER STATE 

        # else:  # what will happen when we die 
        #     screen.fill('#99E793')
        #     screen.blit(player_surface_dead, player_surface_dead_rect)
        #     screen.blit(text_game_surface, text_game_surface_rect)
        #     screen.blit(text_game_surface_restart, text_game_surface_rect_restart)


        pg.display.update()




# if __name__ == "__main__":

#     config_path = "./config.txt"
#     config = neat.config.Config(neat.DefaultGenome,
#                                 neat.DefaultReproduction,
#                                 neat.DefaultSpeciesSet,
#                                 neat.DefaultStagnation,
#                                 config_path)
    
#     population = neat.Population(config)
#     population.add_reporter(neat.StdOutReporter(True))
#     stats = neat.StatisticsReporter()
#     population.add_reporter(stats)

#     population.run(run_game, 100)

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
