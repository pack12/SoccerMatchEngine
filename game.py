import pygame

from Zone import Zone

class Game:
        def __init__(self):
            
            self.width = 1700
            self.height = 925
            pygame.init()
            self.win = pygame.display.set_mode((self.width, self.height))
            pygame.display.set_caption("Soccer Sim")
            self.clock = pygame.time.Clock()
            self.running = True
            self.zones = []
            self.zones_surfs = []
            self.create_zone_board()
            self.game_players = []
            self.debug = True

        """Soccer surf is created here"""
        def create_field(self):
                
            self.soccer_surf = pygame.image.load("Images/Soccer_Field_Transparant.svg.png")
            self.soccer_surf = pygame.transform.scale(self.soccer_surf, (self.width-780,1700))
            self.soccer_surf = pygame.transform.rotate(self.soccer_surf, 90)


            return self.soccer_surf

        def check_events(self):
                
            for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.running = False
                        elif event.key == pygame.K_d:
                            self.debug = not self.debug
                    if event.type == pygame.MOUSEBUTTONDOWN:
                           self.check_mouse_in_zone()
                    elif event.type == pygame.QUIT:
                        self.running = False

        """This is where the rects and zones are made"""
        def create_zone_board(self):
                zone = Zone()
                for j in range(6):
                            
                        zone.x = 52
                        
                        for i in range(11):
                                
                                self.zones.append(pygame.Rect(zone.x,zone.y, zone.width, zone.height))
                                zone.x += zone.width

                                #Creating a copy Zone to reference
                                newZone = Zone()
                                newZone.x = zone.x
                                newZone.y = zone.y
                                newZone.index = (i+1) + (j*11)
                                self.zones_surfs.append(newZone)
                            
                    
                        zone.y += zone.height

        """Checks to see if mouse pos is in zone"""
        def check_mouse_in_zone(self):
                # Get the position of the mouse
                mouse_x, mouse_y = pygame.mouse.get_pos()
                print(f'Mousex: {mouse_x} and Mousey: {mouse_y}')
                for i in range(len(self.zones)):
                        if self.zones[i].collidepoint(mouse_x, mouse_y):
                                print(f'Index: {self.zones_surfs[i].index}')
                                
        """Draw zones onto self.win"""
        def draw_zones(self):
                for i in range(len(self.zones)):
                        pygame.draw.rect(self.win, 'black',self.zones[i],2)

        """Creating the Player Sprites"""
        def create_players_sprites(self):
            blue_img = pygame.image.load("Images/blueTeam.png")
            blue_surf = pygame.transform.scale(blue_img,(40,25))
            blue_surf.set_colorkey("White")
            red_img = pygame.image.load("Images/redTeam.png")
            red_surf = pygame.transform.scale(red_img, (40, 25))
            red_surf.set_colorkey("White")
            return blue_surf,red_surf



        """Used to get the Zone Rect, based on the Index"""
        """Returns Rect of Zone"""
        def get_zone(self,index):
            for i in range(len(self.zones_surfs)):
                if self.zones_surfs[i].index == index:

                    for j in range(len(self.zones)):
                        if j == i:


                            return self.zones[j]

        """Draws player onto the self.win aka the main window"""
        def draw_players(self):
            blue_tm,red_tm = self.create_players_sprites()
            for i in range(len(self.game_players)):
                if self.game_players[i].Team == "Manchester City":

                    zone_rect = self.get_zone(self.game_players[i].Index)
                    center_zone_rect = (zone_rect.left + zone_rect.width/2,zone_rect.top + zone_rect.height/2)

                    self.win.blit(blue_tm,center_zone_rect)
                if self.game_players[i].Team == "Manchester United":
                    zone_rect = self.get_zone(self.game_players[i].Index)
                    center_zone_rect = (zone_rect.left + zone_rect.width/2, zone_rect.top + zone_rect.height/2)
                    self.win.blit(red_tm, center_zone_rect)

        
        def run(self):
            soccer_field = self.create_field()

            while self.running:
                
                self.check_events()

                # RENDER YOUR GAME HERE
                self.win.blit(soccer_field,(0,0))
                if self.debug:
                    self.draw_zones()
                self.draw_players()
                pygame.display.flip() #Update Display

                self.clock.tick(60)  # limits FPS to 60
            pygame.quit()
