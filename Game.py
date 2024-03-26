import pygame
import random
from Ball import Ball
from Zone import ZoneData
from softMaxMkII import softmax
from makeDecision import *
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
                            playerData.move_player_upRight(zoneData)
                        elif event.key == pygame.K_m:
                            playerData.move_player_downRight(zoneData)
                        elif event.key == pygame.K_a:
                            #Calculating action
                            playerPassRates = playerData.findPlayerPassRates(zoneData) # Will be in form of {<playerObject> : 0.78}

                            emptyZonePassRates = playerData.findEmptyZonePassRates(zoneData) # Will be in form of {<zoneObject>: 0.80}
                            dribbleRates = playerData.findDribbleRates(zoneData) #Dribble Rate will be in form of {<zoneObject>: 0.677}
                            shotRate = playerData.findShotRate(zoneData)

                            playerPassRatesArray = []
                            emptyZonePassRatesArray = []
                            dribbleRatesArray = []

                            for i in playerPassRates:
                                playerPassRatesArray.append(playerPassRates[i])
                            for i in emptyZonePassRates:
                                emptyZonePassRatesArray.append(emptyZonePassRates[i])
                            for i in dribbleRates:
                                dribbleRatesArray.append(dribbleRates[i])
                            smPass = playerData.softmax(playerPassRatesArray)
                            # print(f'Probabilities of passes: {smPass}')
                            smEmptyZonePassRates = softmax(emptyZonePassRatesArray)
                            # print(f'Probabilities of Empty zone passes: {smEmptyZonePassRates}')
                            smDribble = playerData.softmax(dribbleRatesArray)
                            # print(f'Probabilities of dribble: {smDribble}')

                            chosenPass = playerData.make_decision(smPass.tolist())
                            # print(f'Index of Chosen Pass: {chosenPass}')

                            chosenDribble = playerData.make_decision(smDribble.tolist())
                            # print(f'chosendribble: {chosenDribble}')
                            """The next thing that has to happen is that we pick each action index"""
                            """Put the respective percentages against each other, so it would be: 
                            [chosenPassRate, chosenDribbleRate, shotRate]"""

                            # Convert dictionary keys to a list
                            pass_rate_keys_list = list(playerPassRates.keys())

                            f_pass_rate = playerPassRates[pass_rate_keys_list[chosenPass]]

                            dribble_rate_keys_list = list(dribbleRates.keys())

                            f_dribble_rate = dribbleRates[dribble_rate_keys_list[chosenDribble]]
                            # smShot = softmax([shotRate,1])
                            # print(f'Probabilities of shot: {smShot}')
                            finalActions = [f_pass_rate,f_dribble_rate,shotRate] #actions go [pass,dribble,shot]
                            smFinalDecision = playerData.softmax(finalActions)

                            chosenFinalAction = playerData.make_decision(smFinalDecision.tolist())
                            print(f'Chosen Action: {chosenFinalAction}')
                            playerWithBall = playerData.get_player_with_ball()
                            # print(f'Player with ball: {playerWithBall}')
                            if chosenFinalAction == 0 and playerData.get_player_with_ball().kickOff == False:
                                print(f'Chosen pass is to {pass_rate_keys_list[chosenPass]}: '
                                      f'{playerPassRates[pass_rate_keys_list[chosenPass]]}')
                                doesPassSucceed = playerData.does_action_succeed(f_pass_rate)

                                findTargetPlayer = pass_rate_keys_list[chosenPass]
                                targetPlayer = None
                                for i in playerData.playerRects:
                                    if i.fullName == findTargetPlayer:
                                        print(f'Found player! {i.fullName}')
                                        targetPlayer = i
                                print(f'Target Player: {findTargetPlayer}')

                                if doesPassSucceed != True:
                                    playerData.fail_pass(zoneData, targetPlayer,ball)
                                else:
                                    playerData.pass_to_target(targetPlayer)

                            elif chosenFinalAction == 1 and playerData.get_player_with_ball().kickOff == False:
                                print(f'Chosen Dribble is to {dribble_rate_keys_list[chosenDribble].index}')
                                futureZoneIndex = dribble_rate_keys_list[chosenDribble].index
                                # print('chose to dribble')
                                doesDribbleSucceed = playerData.does_action_succeed(f_dribble_rate)

                                if doesDribbleSucceed == True:
                                    zone = zoneData.zoneInfo[playerWithBall.Index - 1]
                                    futureZone = zoneData.zoneInfo[futureZoneIndex - 1]

                                    for i in zone.Locations:
                                        if zone.Locations[i][1] == playerWithBall:
                                            zone.Locations[i].remove(playerWithBall)
                                            zone.Locations[i].append(None)
                                            zone.attached_players[playerWithBall.Team].remove(playerWithBall)




                                    player_rect_from_dict = playerData.playerRects[playerWithBall]
                                    print(f'PlayerWtihBallIndex before Del: {playerWithBall.Index}')
                                    del playerData.playerRects[playerWithBall]
                                    playerWithBall.Index = futureZoneIndex
                                    playerData.playerRects[playerWithBall] = player_rect_from_dict
                                    playerWithBall.placedOnLocation = False

                                    futureZone.attached_players[playerWithBall.Team].append(playerWithBall)
                                    print('Index should be updated!')
                                    print(f'PlayerWithBallIndex: {playerWithBall.Index}')

                                    # for i in playerData.playerRects:
                                    #     if i == playerWithBall:
                                    #         player_rect_from_dict = playerData.playerRects[playerWithBall]
                                    #         del playerData.playerRects[playerWithBall]
                                    #         playerWithBall.Index = futureZone
                                    #         playerData.playerRects[playerWithBall] = player_rect_from_dict

                                    # playerData.playerRects[playerWithBall.Index - 1]
                                    # playerWithBall.move(futureZone)
                            elif chosenFinalAction == 2 and playerData.get_player_with_ball().kickOff == False:
                                print('chose to shoot! yolo')
                                playerData.does_action_succeed(shotRate)
                            elif playerData.get_player_with_ball().kickOff == True:
                                print(f'KICK OFF HERE AT ETHIAD STADIUM')
                                print(f'Chosen pass is to {pass_rate_keys_list[chosenPass]}: '
                                      f'{playerPassRates[pass_rate_keys_list[chosenPass]]}')
                                doesPassSucceed = playerData.does_action_succeed(f_pass_rate)
                                playerData.get_player_with_ball().kickOff = False
                                findTargetPlayer = pass_rate_keys_list[chosenPass]
                                targetPlayer = None
                                for i in playerData.playerRects:
                                    if i.fullName == findTargetPlayer:
                                        print(f'Found player! {i.fullName}')
                                        targetPlayer = i
                                print(f'Target Player: {findTargetPlayer}')

                                if doesPassSucceed != True:
                                    playerData.fail_pass(zoneData,targetPlayer,ball)
                                else:
                                    playerData.pass_to_target(targetPlayer)

                            print(f'Final Probs: {f_pass_rate,f_dribble_rate,shotRate}')





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
