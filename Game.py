import pygame
import random
from Ball import Ball
from Zone import ZoneData
from playerActionWithBall import playerActionWithBall
from playerActionOffBall import playerActionOffBall
import time
import threading
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
        def thread_function(self,playerData,zoneData,ball):
            playerActionCount = 0
            while ball.playerAttached != None:
                playerActionWithBall(playerData,zoneData,ball)
                playerActionCount += 1
                print(f'{playerActionCount} on-ball actions performed')
                time.sleep(0.5)


        def check_events(self,zoneData,playerData,ball):
                
            for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.running = False
                        elif event.key == pygame.K_d:
                            self.debug = not self.debug
                        elif event.key == pygame.K_SPACE:

                            playerData.move_player_right(zoneData)

                        elif event.key == pygame.K_LEFT:
                            playerData.move_player_left(zoneData)
                        elif event.key == pygame.K_p:
                            playerData.player_pass_randomly(zoneData)
                        elif event.key == pygame.K_UP:
                            playerData.move_player_up(zoneData)
                        elif event.key == pygame.K_DOWN:
                            playerData.move_player_down(zoneData)
                        elif event.key == pygame.K_q:
                            playerData.move_player_upLeft(zoneData)
                        elif event.key == pygame.K_z:
                            playerData.move_player_downLeft(zoneData)
                        elif event.key == pygame.K_o:
                            """This will now be offball action button"""
                            playerActionOffBall(playerData,zoneData,ball)
                            # playerData.move_player_upRight(zoneData)
                        elif event.key == pygame.K_m:
                            playerData.move_player_downRight(zoneData)
                        elif event.key == pygame.K_a:
                            # playerActionWithBall(playerData,zoneData,ball)
                            x = threading.Thread(target=self.thread_function, args=(playerData,zoneData,ball))
                            x.start()







                            """Then we need to see whether the chosen action is actually successful"""
                            
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
                
                self.check_events(zoneData,playerData,ball)

                # RENDER YOUR GAME HERE
                self.win.blit(soccer_field,(0,0))
                if self.debug:
                    zoneData.draw_zones(self.win)
                playerData.draw_players(self.win,zoneData)
                ball.draw_ball(self.win,playerData,zoneData)
                pygame.display.flip() #Update Display

                self.clock.tick(60)  # limits FPS to 60
                """Not implemented but zoneData.update will go here"""
            pygame.quit()

