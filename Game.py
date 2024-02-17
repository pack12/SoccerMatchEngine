import pygame

from Ball import Ball
from Zone import ZoneData

class Game:
        def __init__(self):
            
            self.width = 1700
            self.height = 925
            pygame.init()
            self.win = pygame.display.set_mode((self.width, self.height))
            pygame.display.set_caption("Soccer Sim")
            self.clock = pygame.time.Clock()
            self.running = True
            self.debug = True

        """Soccer surf is created here"""
        def create_field(self):
                
            self.soccer_surf = pygame.image.load("Images/Soccer_Field_Transparant.svg.png")
            self.soccer_surf = pygame.transform.scale(self.soccer_surf, (self.width-780,1700))
            self.soccer_surf = pygame.transform.rotate(self.soccer_surf, 90)


            return self.soccer_surf

        def check_events(self,zoneData):
                
            for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.running = False
                        elif event.key == pygame.K_d:
                            self.debug = not self.debug
                    if event.type == pygame.MOUSEBUTTONDOWN:
                           zoneData.check_mouse_in_zone()
                    elif event.type == pygame.QUIT:
                        self.running = False



        def run(self,playerData):
            soccer_field = self.create_field()
            zoneData = ZoneData()
            zoneData.create_zone_board()
            playerData.create_initial_player_rects(zoneData)
            ball = Ball()
            while self.running:
                
                self.check_events(zoneData)

                # RENDER YOUR GAME HERE
                self.win.blit(soccer_field,(0,0))
                if self.debug:
                    zoneData.draw_zones(self.win)
                playerData.draw_players(self.win,zoneData)
                ball.draw_ball(self.win,playerData)
                pygame.display.flip() #Update Display

                self.clock.tick(60)  # limits FPS to 60
                """Not implemented but zoneData.update will go here"""
            pygame.quit()
