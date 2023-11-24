import pygame as pg
import random
import neat

class Player:

    def __init__(self, snail_rect) -> None:
        
        self.sprite = pg.image.load('graphics/Player/player_stand.png').convert_alpha()

        self.sprite_rect = self.sprite.get_rect(midbottom = (50, 300))

        self.alive = True

        self.snail_rect = snail_rect

        self.player_grav = 1

        self.time_alive = 0
        
    def get_time_alive(self):
        self.time_alive = int(pg.time.get_ticks() / 1000)
    
    def inc_grav(self):
        self.player_grav += 1


    def is_alive(self):
        return self.alive

    def get_distance(self):

        """ gets the dist from snail to player """
        dist = pg.math.Vector2(self.sprite_rect.center).distance_to((self.snail_rect.center))
        p_pos_x, p_pos_y = self.sprite_rect.center
        s_pos_x, s_pos_y= self.snail_rect.center
        # player_from_ground = 300 - self.sprite_rect.bottom
        return [p_pos_x, p_pos_y,s_pos_x, s_pos_y, dist]

    def draw_player(self):
        # screen.blit(self.sprite, self.sprite_rect)
        return self.sprite, self.sprite_rect

    def apply_grav(self):
        self.sprite_rect.bottom += self.player_grav

    def set_grav(self, grav):
        self.player_grav = grav

    def stay_on_floor(self):
        self.sprite_rect.bottom = 300

    def get_bot(self):
        return self.sprite_rect.bottom
    
    def collison_check(self):
        if self.sprite_rect.colliderect(self.snail_rect):
            self.alive = False

    def get_reward(self):
        return self.time_alive 

def run_game(genomes, config):  # genomes, config

    pg.init()
    
    # FONT 
    font = pg.font.Font(None, 50)

    # SNAIL SPEED 
    speed = 5

    screen = pg.display.set_mode((800,400))   
    pg.display.set_caption('Running Game')
    clock = pg.time.Clock()

    # BACKGROUND 
    sky_surface = pg.image.load('graphics/Sky.png').convert()
    ground_surface = pg.image.load('graphics/ground.png').convert()

    # SNAIL 
    snail_surface = pg.image.load('graphics/snail/snail1.png').convert_alpha()
    snail_rect = snail_surface.get_rect(midbottom = (850,300))
        
    #live counter  
    
    live_num = 0
    counter = 0

    # COLLECTION OF CARS AND NETS 

    nets = []
    list_players = []

    for i, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        g.fitness = 0  # reset all fitness back to 0
        list_players.append(Player(snail_rect))


    Done = False
    while not Done:
        clock.tick(60)

        for event in pg.event.get():
            # get method retrieves all the events 
            if event.type == pg.QUIT:  # checks when player presses the x button 
                pg.quit()  # quits the game, but still keeps the while loop running 
                Done = True
        
        for player in list_players:
            player.inc_grav()
            player.apply_grav()
            if player.get_bot() > 300:
                player.stay_on_floor()

        for i, player in enumerate(list_players):
            # loop through players and each palyer will make a choice 
            output = nets[i].activate(player.get_distance())
            choice = output.index(max(output))
            # if i ==0:
            #     print(choice)
            if choice == 0:
                if player.get_bot() == 300:
                    player.set_grav(-20)
                    
            else:
                player.stay_on_floor()
            
        
        # print(genomes[0][1].fitness)
        # COUNT NUM PLAYERS ALIVE 
        live_num = 0
        for i, player in enumerate(list_players):
            player.collison_check()
            player.get_time_alive()
            if player.is_alive():
                live_num += 1
                genomes[i][1].fitness += player.get_reward()
                pla, pla_re = player.draw_player()
                screen.blit(pla, pla_re)
                # print(genomes[i][1].fitness)
        
            

        if live_num == 0:
            print("break!")
            Done = True
            
        counter += 1
        if counter == 30 * 40: # Stop After About 20 Seconds
            Done = True



        str_num_alive1 = font.render(f' {live_num}', False, 'black')
        screen.blit(sky_surface, (0,0))
        screen.blit(ground_surface, (0,300))
        screen.blit(str_num_alive1, (0,0))
        
        # DRAW PLAYER 
        for player in list_players: 
            if player.is_alive():
                pla, pla_re = player.draw_player()
                screen.blit(pla, pla_re)

        # SNAIL 
        snail_rect.left -= speed

        if snail_rect.left < -100:
            snail_rect.left = 850
        screen.blit(snail_surface, snail_rect)

        

        pg.display.update()

if __name__  == "__main__":
    config_path = "./config.txt"
    config = neat.config.Config(neat.DefaultGenome,
                                neat.DefaultReproduction,
                                neat.DefaultSpeciesSet,
                                neat.DefaultStagnation,
                                config_path)

    # Create Population And Add Reporters
    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)
    
    # Run Simulation For A Maximum of 1000 Generations
    population.run(run_game, 1000)
