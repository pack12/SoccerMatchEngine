import numpy as np
import time
import random
import pygame
class Player:
    def __init__(self,fname,lname,hasBall,currentZone,Team,**kwargs):
        self.fname = fname
        self.lname = lname
        self.fullName = str(f'{self.fname} {self.lname}')
        self.hasBall = hasBall
        self.Index = currentZone
        self.Team = Team
        self.placedOnLocation = False # Used when adjusting the player rect
        self.passing = kwargs.get('passing', 10)
        self.decision = kwargs.get('decision',10)
        self.finishing = kwargs.get('finishing',10)
        self.dribble = kwargs.get('dribbling',10)
        self.speed = kwargs.get('speed',10)
        self.workRate = kwargs.get('workRate',10)
        self.kickOff = kwargs.get('kickOff',False)
        self.position = kwargs.get('position',None)
    def move(self, FutureZoneIndex):
        self.Index = FutureZoneIndex
    def __hash__(self):
        return hash((self.fname, self.lname,self.hasBall,self.Index,self.Team))




class PlayerData:
    def __init__(self,playersInfo):
        self.game_players = [] #rects of players
        self.playersInfo = playersInfo #List of Player Objects
        self.playerRects = {}

    """Draws player onto the self.win aka the main window"""

    def draw_players(self,win,zoneData):
        blue_tm, red_tm = create_players_sprites()
        self.adjust_player_rects(zoneData)
        for i in self.playerRects:
            # print(f'{str(i.fname + " "+ i.lname)}: {self.playerRects[i]}')
            # #OUTPUT = Erling Haaland:Rect(849,534,40,25)

            if i.Team == "Manchester City":
                win.blit(blue_tm,self.playerRects[i])

            if i.Team == "Manchester United":
                win.blit(red_tm,self.playerRects[i])




    def create_initial_player_rects(self,zoneData):
        blue_tm, red_tm = create_players_sprites()
        for i in range(len(self.playersInfo)):
            if self.playersInfo[i].Team == "Manchester City":
                #Get the zone rect and the zone object
                zone_rect,zone_info = zoneData.get_zone(self.playersInfo[i].Index)

                #Use the zone rect to get the center of the zone!
                center_zonexY = (zone_rect.left + zone_rect.width / 2, zone_rect.top + zone_rect.height / 2)



                #Add player on the zone object, only if it's not already there!
                if self.playersInfo[i] not in zone_info.attached_players['Manchester City']:

                    zone_info.attached_players['Manchester City'].append(self.playersInfo[i])
                player_rect = pygame.Rect(center_zonexY[0],center_zonexY[1],blue_tm.get_width(),blue_tm.get_height())
                self.playerRects[self.playersInfo[i]] = player_rect
            if self.playersInfo[i].Team == "Manchester United":
                zone_rect,zone_info = zoneData.get_zone(self.playersInfo[i].Index)
                center_zonexY = (zone_rect.left + zone_rect.width / 2, zone_rect.top + zone_rect.height / 2)


                if self.playersInfo[i] not in zone_info.attached_players['Manchester United']:

                    zone_info.attached_players['Manchester United'].append(self.playersInfo[i])
                player_rect = pygame.Rect(center_zonexY[0], center_zonexY[1], blue_tm.get_width(), blue_tm.get_height())
                self.playerRects[self.playersInfo[i]] = player_rect

    def adjust_player_rects(self,zoneData):

        for i in range(len(zoneData.zoneInfo)):




            indexOfZone = zoneData.zoneInfo[i].index

            playersInZone = []

            for k in (self.playerRects):

                # Get players who are in the zone index

                if k.Index == indexOfZone:


                    playersInZone.append(k)

            for j in range(len(playersInZone)):

                # Get the Zone Rect
                zone_rect, zone_info = zoneData.get_zone(playersInZone[j].Index)
                player = playersInZone[j]

                if player.Team == "Manchester City":

                    #Find available location for player on blue team
                    for k in ['loc_4','loc_5','loc_6']:

                        if zone_info.Locations[k][1] == None and player.placedOnLocation == False:
                            del zone_info.Locations[k][1]
                            zone_info.Locations[k].append(playersInZone[j])
                            player.placedOnLocation = True

                            #I need to pull out the tuple coordinates
                            newX = zone_info.Locations[k][0][0]
                            newY = zone_info.Locations[k][0][1]
                            playerRect = self.playerRects[player]
                            playerRectList = list(playerRect)
                            playerRectList[0] = newX
                            playerRectList[1] = newY
                            playerRectTuple = tuple(playerRectList)
                            self.playerRects[player] = pygame.Rect(playerRectTuple)
                if player.Team == "Manchester United":
                    # Find available location for player on red team
                    for k in ['loc_1','loc_2','loc_3']:
                        if zone_info.Locations[k][1] == None and player.placedOnLocation == False:
                            del zone_info.Locations[k][1]
                            zone_info.Locations[k].append(playersInZone[j])
                            player.placedOnLocation = True
                            # I need to pull out the tuple coordinates
                            newX = zone_info.Locations[k][0][0]
                            newY = zone_info.Locations[k][0][1]

                            playerRect = self.playerRects[player]
                            playerRectList = list(playerRect)
                            playerRectList[0] = newX
                            playerRectList[1] = newY
                            playerRectTuple = tuple(playerRectList)
                            self.playerRects[player] = pygame.Rect(playerRectTuple)

    def get_player_with_ball(self):
        for i in self.playerRects:
            if i.hasBall:
                return i
    def get_opposite_team(self):
        if self.get_player_with_ball().Team == "Manchester City":
            return "Manchester United"
        elif self.get_player_with_ball().Team == "Manchester United":
            return "Manchester City"
    def move_player_right(self, zoneData):
        #Get the player with the ball b/c he will be the player deciding the first move and then everybody reacts
        player = self.get_player_with_ball()

        # Get the zone object the player is on
        zone = zoneData.zoneInfo[player.Index - 1]
        futureZoneIndex = zone.index + 1
        if futureZoneIndex <= 66:

            futureZone = zoneData.zoneInfo[futureZoneIndex-1]
            print(f'Future Index: {futureZone.index}')
        print(f'Current Index: {player.Index}')


        if futureZoneIndex < 67 and futureZone.leftEdge == False:

            if len(futureZone.attached_players[player.Team]) < 3:


                #Remove the player from the zone locations
                for i in zone.Locations:
                    if zone.Locations[i][1] == player:

                        zone.Locations[i].remove(player)
                        zone.Locations[i].append(None)
                        zone.attached_players[player.Team].remove(player)

                                                                    # This is all in effort to delete and replace the player object
                                                                    #For WHATEVER reason, you cannot simply keep the player object and modify it
                                                                    #OTHERWISE I GET a KEYERROR in the dict, so to keep things simple, I just delete
                                                                    #And replace the player object with a replicate
                player_rect_from_dict = self.playerRects[player]
                del self.playerRects[player]
                player.Index += 1
                self.playerRects[player] = player_rect_from_dict
                player.placedOnLocation = False

                futureZone.attached_players[player.Team].append(player)

    def move_player_left(self, zoneData):
        player = self.get_player_with_ball()
        zone = zoneData.zoneInfo[player.Index - 1]
        futureZone = zoneData.zoneInfo[player.Index-2]
        futureZoneIndex = zone.index - 1
        print(futureZoneIndex)
        if futureZoneIndex > 0 and futureZone.rightEdge == False:

            if len(futureZone.attached_players[player.Team]) < 3:

                for i in zone.Locations:
                    if zone.Locations[i][1] == player:

                        zone.Locations[i].remove(player)
                        zone.Locations[i].append(None)
                        zone.attached_players[player.Team].remove(player)

                player_rect_from_dict = self.playerRects[player]
                del self.playerRects[player]
                player.Index -= 1
                self.playerRects[player] = player_rect_from_dict
                player.placedOnLocation = False

                futureZone.attached_players[player.Team].append(player)

    def move_player_up(self, zoneData):
        player = self.get_player_with_ball()
        zone = zoneData.zoneInfo[player.Index - 1]

        futureZoneIndex = zone.index - 11

        if futureZoneIndex > 0:

            futureZone = zoneData.zoneInfo[futureZoneIndex - 1]


            if len(futureZone.attached_players[player.Team]) < 3:

                for i in zone.Locations:
                    if zone.Locations[i][1] == player:

                        zone.Locations[i].remove(player)
                        zone.Locations[i].append(None)
                        zone.attached_players[player.Team].remove(player)

                player_rect_from_dict = self.playerRects[player]
                del self.playerRects[player]
                player.Index -= 11
                self.playerRects[player] = player_rect_from_dict
                player.placedOnLocation = False

                futureZone.attached_players[player.Team].append(player)
    def move_player_down(self, zoneData):
        player = self.get_player_with_ball()
        zone = zoneData.zoneInfo[player.Index - 1]

        futureZoneIndex = zone.index + 11

        if futureZoneIndex < 67:

            futureZone = zoneData.zoneInfo[futureZoneIndex - 1]


            if len(futureZone.attached_players[player.Team]) < 3:

                for i in zone.Locations:
                    if zone.Locations[i][1] == player:

                        zone.Locations[i].remove(player)
                        zone.Locations[i].append(None)
                        zone.attached_players[player.Team].remove(player)

                player_rect_from_dict = self.playerRects[player]
                del self.playerRects[player]
                player.Index += 11
                self.playerRects[player] = player_rect_from_dict
                player.placedOnLocation = False

                futureZone.attached_players[player.Team].append(player)
    def move_player_upLeft(self,zoneData):
        player = self.get_player_with_ball()


        zone = zoneData.zoneInfo[player.Index - 1]
        futureZoneIndex = zone.index - 12
        futureZone = zoneData.zoneInfo[futureZoneIndex-1]

        if futureZoneIndex > 0 and zone.leftEdge == False:
            if len(futureZone.attached_players[player.Team]) < 3:


                #Remove the player from the zone locations
                for i in zone.Locations:
                    if zone.Locations[i][1] == player:

                        zone.Locations[i].remove(player)
                        zone.Locations[i].append(None)
                        zone.attached_players[player.Team].remove(player)

                player_rect_from_dict = self.playerRects[player]
                del self.playerRects[player]
                player.Index -= 12
                self.playerRects[player] = player_rect_from_dict
                player.placedOnLocation = False

                futureZone.attached_players[player.Team].append(player)

    def move_player_downLeft(self,zoneData):
        player = self.get_player_with_ball()


        zone = zoneData.zoneInfo[player.Index - 1]
        futureZoneIndex = zone.index + 10
        if futureZoneIndex < 66:

            futureZone = zoneData.zoneInfo[futureZoneIndex-1]
            # print(f'Current: {zone.index}')
            # print(f'Future: {futureZoneIndex}')
        if futureZoneIndex < 67 and zone.leftEdge == False and zone.bottomEdge == False:
            if len(futureZone.attached_players[player.Team]) < 3:


                #Remove the player from the zone locations
                for i in zone.Locations:
                    if zone.Locations[i][1] == player:

                        zone.Locations[i].remove(player)
                        zone.Locations[i].append(None)
                        zone.attached_players[player.Team].remove(player)

                player_rect_from_dict = self.playerRects[player]
                del self.playerRects[player]
                player.Index += 10
                self.playerRects[player] = player_rect_from_dict
                player.placedOnLocation = False

                futureZone.attached_players[player.Team].append(player)
    def move_player_upRight(self,zoneData):
        player = self.get_player_with_ball()


        zone = zoneData.zoneInfo[player.Index - 1]
        futureZoneIndex = zone.index - 10

        if futureZoneIndex < 66 and futureZoneIndex > 0:

            futureZone = zoneData.zoneInfo[futureZoneIndex-1]
            # print(f'Current: {zone.index}')
            # print(f'Future: {futureZoneIndex}')

        #print(f'Future Zone: {futureZone.index}')
        if (futureZoneIndex < 67 and futureZoneIndex > 0) and zone.rightEdge == False:
            if len(futureZone.attached_players[player.Team]) < 3:


                #Remove the player from the zone locations
                for i in zone.Locations:
                    if zone.Locations[i][1] == player:

                        zone.Locations[i].remove(player)
                        zone.Locations[i].append(None)
                        zone.attached_players[player.Team].remove(player)

                player_rect_from_dict = self.playerRects[player]
                del self.playerRects[player]
                player.Index -= 10
                self.playerRects[player] = player_rect_from_dict
                player.placedOnLocation = False

                futureZone.attached_players[player.Team].append(player)

    def move_player_downRight(self,zoneData):
        player = self.get_player_with_ball()


        zone = zoneData.zoneInfo[player.Index - 1]
        futureZoneIndex = zone.index + 12

        if futureZoneIndex < 66 and futureZoneIndex > 0:

            futureZone = zoneData.zoneInfo[futureZoneIndex-1]
            # print(f'Current: {zone.index}')
            # print(f'Future: {futureZoneIndex}')

        #print(f'Future Zone: {futureZone.index}')
        if (futureZoneIndex < 67 and futureZoneIndex > 0) and zone.rightEdge == False:
            if len(futureZone.attached_players[player.Team]) < 3:


                #Remove the player from the zone locations
                for i in zone.Locations:
                    if zone.Locations[i][1] == player:

                        zone.Locations[i].remove(player)
                        zone.Locations[i].append(None)
                        zone.attached_players[player.Team].remove(player)

                player_rect_from_dict = self.playerRects[player]
                del self.playerRects[player]
                player.Index += 12
                self.playerRects[player] = player_rect_from_dict
                player.placedOnLocation = False

                futureZone.attached_players[player.Team].append(player)

    def player_pass_randomly(self,zoneData):
        #Initialize variable
        player_has_ball = None

        #See what player has the ball
        for i in self.playersInfo:
            if i.hasBall:
                player_has_ball = i

        #For time being, we pick a random number for a random player
        random_n = random.randint(0, len(self.playerRects) - 1)

        #Get Random player from player object list
        player_recieve_ball = self.playersInfo[random_n]

        #Iterate until we get a reciever who is on the same team and isn't the player
        while player_recieve_ball.Team != player_has_ball.Team or player_recieve_ball.hasBall == True:
            random_n = random.randint(0, len(self.playerRects) - 1)
            player_recieve_ball = self.playersInfo[random_n]

        print(f'{player_has_ball.fname} passes to {player_recieve_ball.fname}')
        self.findDistanceToTargetPlayer(zoneData, player_recieve_ball)
        # Standard delete player and reinsert it into self.playerRect
        #I think the reason why this happens (and this is just for future reference is becasue
        #When we update the player_rect object in this method, the object in the player_Rect list is different than
        #The object here! Basically you can't have the same object have 2 different attribute properties?

        player_rect_from_dict = self.playerRects[player_has_ball]
        del self.playerRects[player_has_ball]
        player_has_ball.hasBall = False
        self.playerRects[player_has_ball] = player_rect_from_dict

        player_rect_from_dict = self.playerRects[player_recieve_ball]
        del self.playerRects[player_recieve_ball]
        player_recieve_ball.hasBall = True
        self.playerRects[player_recieve_ball] = player_rect_from_dict

    def pass_to_target(self,targetPlayer):

        player_has_ball = self.get_player_with_ball()


        player_recieve_ball = targetPlayer


        # Standard delete player and reinsert it into self.playerRect
        # I think the reason why this happens (and this is just for future reference is becasue
        # When we update the player_rect object in this method, the object in the player_Rect list is different than
        # The object here! Basically you can't have the same object have 2 different attribute properties?

        player_rect_from_dict = self.playerRects[player_has_ball]
        del self.playerRects[player_has_ball]
        player_has_ball.hasBall = False
        self.playerRects[player_has_ball] = player_rect_from_dict

        player_rect_from_dict = self.playerRects[player_recieve_ball]
        del self.playerRects[player_recieve_ball]
        player_recieve_ball.hasBall = True
        self.playerRects[player_recieve_ball] = player_rect_from_dict
    def fail_pass(self,zoneData,targetPlayer,ball):
        targetPlayerZone = zoneData.zoneInfo[targetPlayer.Index - 1]
        zoneIndexes = []
        surroundingTargetZones = []

        if targetPlayerZone.index != 67 and targetPlayerZone.index != 68:

            nZoneIndex = targetPlayerZone.index - 11
            zoneIndexes.append(nZoneIndex)
            neZoneIndex = targetPlayerZone.index - 10
            zoneIndexes.append(neZoneIndex)
            nwZoneIndex = targetPlayerZone.index - 12
            zoneIndexes.append(nwZoneIndex)
            wZoneIndex = targetPlayerZone.index - 1
            zoneIndexes.append(wZoneIndex)
            eZoneIndex = targetPlayerZone.index + 1
            zoneIndexes.append(eZoneIndex)
            sZoneIndex = targetPlayerZone.index + 11
            zoneIndexes.append(sZoneIndex)
            swZoneIndex = targetPlayerZone.index + 10
            zoneIndexes.append(swZoneIndex)
            seZoneIndex = targetPlayerZone.index + 12
            zoneIndexes.append(seZoneIndex)

            for i in zoneIndexes:
                # Get the Zone
                if i > 0 and i < 67:

                    zone = zoneData.zoneInfo[i - 1]
                    surroundingTargetZones.append(zone)
                    if targetPlayerZone.rightEdge == True and zone.leftEdge == True:
                        # Don't add this zone as an available zone
                        surroundingTargetZones.remove(zone)
                    elif targetPlayerZone.leftEdge == True and zone.rightEdge == True:
                        surroundingTargetZones.remove(zone)
                    elif len(zone.attached_players[self.get_player_with_ball().Team]) > 0:
                        surroundingTargetZones.remove(zone)
                        # print(f'This zone has a player on it{zone.index}')
        elif targetPlayerZone.index == 67:
            surroundingTargetZones.append(zoneData.zoneInfo[22])
            surroundingTargetZones.append(zoneData.zoneInfo[33])
        elif targetPlayerZone.index == 68:
            surroundingTargetZones.append(zoneData.zoneInfo[32])
            surroundingTargetZones.append(zoneData.zoneInfo[43])
        print(f'PASS FAILED! Ball will go to one of these zones: {surroundingTargetZones}')
        for i in surroundingTargetZones:
            print(i.index)
        rand_num = random.randint(0,len(surroundingTargetZones)-1)
        chosenZone = surroundingTargetZones[rand_num]
        print(f'Ball will go to {chosenZone.index}')

        player_has_ball = self.get_player_with_ball()
        player_rect_from_dict = self.playerRects[player_has_ball]
        del self.playerRects[player_has_ball]
        player_has_ball.hasBall = False
        self.playerRects[player_has_ball] = player_rect_from_dict

        ball.playerAttached = None
        ball.currentIndex = chosenZone.index



    def calculatePlayerActions(self,zoneData):
        """So in order to calculate the potential player actions, the player needs to fin"""
        pass
    def findDistanceToTargetPlayer(self,zoneData,targetPlayer):
        """In order to find the distance to target player, I need to get the player with the ball and their
        current zone And I need to get the targetPlayer and the zone they're on"""
        playerWithBall = self.get_player_with_ball()
        playerWithBallZone = zoneData.zoneInfo[playerWithBall.Index - 1]
        playerWithBallX = None
        playerWithBallY = None

        targetPlayerZone = zoneData.zoneInfo[targetPlayer.Index - 1]
        targetPlayerX = None
        targetPlayerY = None

        # print(f'Target Player: {targetPlayer.fullName}')
        #Get the playerWithBall x and y location
        playerCounter = 0
        for i in zoneData.zoneInfo:

            # print(i.Locations)
            for j in i.Locations:
                # print(f'{i.index}: {i.Locations[j]}')

                if i.Locations[j][1] != None:
                    # print(f'{i.Locations[j][1].fullName}')
                    playerCounter += 1

                if i.Locations[j][1] == playerWithBall:
                    playerWithBallX = i.Locations[j][0][0]
                    playerWithBallY = i.Locations[j][0][1]
                elif i.Locations[j][1] == targetPlayer:
                    targetPlayerX = i.Locations[j][0][0]
                    targetPlayerY = i.Locations[j][0][1]
        # print(f'Player Counter: {playerCounter}')     #Had to write this print stmt in b/c player was being deleted!
        # Define the coordinates of two points
        playerWithBallPoint = np.array([playerWithBallX, playerWithBallY])
        targetPlayerPoint = np.array([targetPlayerX, targetPlayerY])

        # Calculate the distance between the two points
        distance = np.linalg.norm(targetPlayerPoint - playerWithBallPoint)

        # print("Distance between the points:", distance/147)
        return distance/147

    def findDistanceToEmptyZone(self,zoneData,targetZone):
        """In order to find the distance to target player, I need to get the player with the ball and their
                current zone And I need to get the targetPlayer and the zone they're on"""
        playerWithBall = self.get_player_with_ball()
        playerWithBallZone = zoneData.zoneInfo[playerWithBall.Index - 1]
        playerWithBallX = None
        playerWithBallY = None

        targetZoneX = None
        targetZoneY = None

        # Get the playerWithBall x and y location
        for i in zoneData.zoneInfo:
            # print(i.Locations)
            for j in i.Locations:
                # print(i.Locations[j])
                if i.Locations[j][1] == playerWithBall:
                    playerWithBallX = i.Locations[j][0][0]
                    playerWithBallY = i.Locations[j][0][1]

            if i.index == targetZone.index:
                targetZoneX = i.Locations['loc_1'][0][0]
                targetZoneY = i.Locations['loc_1'][0][1]

        # Define the coordinates of two points
        playerWithBallPoint = np.array([playerWithBallX, playerWithBallY])
        targetZonePoint = np.array([targetZoneX, targetZoneY])

        # Calculate the distance between the two points
        distance = np.linalg.norm(targetZonePoint - playerWithBallPoint)

        # print("Distance between the points:", distance / 147)
        return distance / 147

    def findDistanceToBall(self,zoneData,player,ball):
        """In order to find the distance to target player, I need to get the player with the ball and their
                current zone And I need to get the targetPlayer and the zone they're on"""

        playerWithBallZone = zoneData.zoneInfo[player.Index - 1]
        playerX = None
        playerY = None

        ballZone = zoneData.zoneInfo[player.Index - 1]
        ballX = ball.x
        ballY = ball.y

        # print(f'Target Player: {targetPlayer.fullName}')
        # Get the playerWithBall x and y location
        playerCounter = 0
        for i in zoneData.zoneInfo:

            # print(i.Locations)
            for j in i.Locations:
                # print(f'{i.index}: {i.Locations[j]}')

                if i.Locations[j][1] != None:
                    # print(f'{i.Locations[j][1].fullName}')
                    playerCounter += 1

                if i.Locations[j][1] == player:
                    playerX = i.Locations[j][0][0]
                    playerY = i.Locations[j][0][1]

        # print(f'Player Counter: {playerCounter}')     #Had to write this print stmt in b/c player was being deleted!
        # Define the coordinates of two points
        playerPoint = np.array([playerX, playerY])
        ballPoint = np.array([ballX, ballY])

        # Calculate the distance between the two points
        distance = np.linalg.norm(ballPoint - playerPoint)

        # print("Distance between the points:", distance/147)
        return distance / 147

    def findPlayerPassRates(self,zoneData):
        passRates = {}
        oppositeTeam = self.get_opposite_team()

        for i in self.playersInfo:
            if i != self.get_player_with_ball() and i.Team == self.get_player_with_ball().Team:

                distance = self.findDistanceToTargetPlayer(zoneData,i)

                #Calculate the pass rates right here and now and store them in passRates, along with potential target player
                passing = self.get_player_with_ball().passing
                targetPlayerZone = zoneData.zoneInfo[i.Index - 1]

                denominator = 1 + np.exp((-0.25 * passing) + (0.25 * distance)) + \
                              (0.6 * len(targetPlayerZone.attached_players[oppositeTeam]))
                # denominator = 1 + np.exp((-0.25 * 10) + (0.25 * 2.23))
                # print(denominator)
                rate = 1/denominator
                passRates[i.fullName] = rate



        # print(passRates)
        return passRates

    """This is for offensive players without ball"""
    def findEmptyZonePassRates(self,zoneData):
        zoneRates = {}
        for i in zoneData.zoneInfo:
            if len(i.attached_players["Manchester United"]) == 0 and len(i.attached_players["Manchester City"]) == 0:
                # print(f'Zone {i.index} has no players')
                zoneDistance = self.findDistanceToEmptyZone(zoneData, i)

                passing = self.get_player_with_ball().passing

                denominator = 1 + np.exp((-0.25 * passing) + (0.35 * zoneDistance))

                # print(denominator)
                rate = 1 / denominator
                zoneRates[i] = rate
        # print(zoneRates)
        return zoneRates
    def findDribbleRates(self,zoneData):
        dribbleRates = {}
        player = self.get_player_with_ball()
        #In order to find the Dribble Rates, I need to get all the surrounding zones
        currentZone = zoneData.zoneInfo[player.Index - 1]

        zoneIndexes = []
        availableZonesToDribble = []

        if currentZone.index != 67 and currentZone.index != 68:

            nZoneIndex = player.Index - 11
            zoneIndexes.append(nZoneIndex)
            neZoneIndex = player.Index - 10
            zoneIndexes.append(neZoneIndex)
            nwZoneIndex = player.Index - 12
            zoneIndexes.append(nwZoneIndex)
            wZoneIndex = player.Index - 1
            zoneIndexes.append(wZoneIndex)
            eZoneIndex = player.Index + 1
            zoneIndexes.append(eZoneIndex)
            sZoneIndex = player.Index + 11
            zoneIndexes.append(sZoneIndex)
            swZoneIndex = player.Index + 10
            zoneIndexes.append(swZoneIndex)
            seZoneIndex = player.Index + 12
            zoneIndexes.append(seZoneIndex)

            for i in zoneIndexes:
                # Get the Zone
                if i > 0 and i < 67:

                    zone = zoneData.zoneInfo[i - 1]
                    availableZonesToDribble.append(zone)
                    if currentZone.rightEdge == True and zone.leftEdge == True:
                        #Don't add this zone as an available zone
                        availableZonesToDribble.remove(zone)
                    elif currentZone.leftEdge == True and zone.rightEdge == True:
                        availableZonesToDribble.remove(zone)
                    elif len(zone.attached_players[self.get_player_with_ball().Team]) == 3:
                        availableZonesToDribble.remove(zone)


        elif currentZone.index == 67:
            availableZonesToDribble.append(zoneData.zoneInfo[22])
            availableZonesToDribble.append(zoneData.zoneInfo[33])
        elif currentZone.index == 68:
            availableZonesToDribble.append(zoneData.zoneInfo[32])
            availableZonesToDribble.append(zoneData.zoneInfo[43])

        if currentZone.index == 23 or currentZone.index == 34:
            availableZonesToDribble.append(zoneData.zoneInfo[66])
        elif currentZone.index == 33 or currentZone.index == 44:
            availableZonesToDribble.append(zoneData.zoneInfo[67])
        print('Available Zones to Dribble: ')
        dribbling = self.get_player_with_ball().dribble
        for i in availableZonesToDribble:
            print(i.index)
            if len(currentZone.attached_players[self.get_opposite_team()]) > 0:
                denominator = 1 + np.exp((-0.075 * dribbling))
                dribbleRates[i] = 1/denominator
            elif len(i.attached_players[self.get_opposite_team()]) > 0:
                denominator = 1 + np.exp((-0.1 * dribbling))
                dribbleRates[i] = 1/denominator
            elif len(i.attached_players[self.get_opposite_team()]) == 0:
                denominator = 1 + np.exp((-0.20 * dribbling))
                dribbleRates[i] = 1 / denominator

        # print(f'Dribbling Rates: ')
        # for i in dribbleRates:
        #     print(f'Zone: {i.index} Rate: {dribbleRates[i]}')
        return dribbleRates
    def findShotRate(self,zoneData):
        """In order to find the shot rate, I need finishing attribute and length to goal"""

        playerWithBall = self.get_player_with_ball()
        playerWithBallZone = zoneData.zoneInfo[playerWithBall.Index - 1]
        playerWithBallX = None
        playerWithBallY = None
        goalX = None
        goalY = None
        goalPoint = None
        if playerWithBall.Team == "Manchester United":
            goalX = 1656
            goalY = 455
            goalPoint = np.array([goalX,goalY])

            for i in zoneData.zoneInfo:
                # print(i.Locations)
                for j in i.Locations:
                    # print(i.Locations[j])
                    if i.Locations[j][1] == playerWithBall:
                        playerWithBallX = i.Locations[j][0][0]
                        playerWithBallY = i.Locations[j][0][1]
        elif playerWithBall.Team == "Manchester City":
            goalX = 34
            goalY = 459
            goalPoint = np.array([goalX, goalY])

            for i in zoneData.zoneInfo:
                # print(i.Locations)
                for j in i.Locations:
                    # print(i.Locations[j])
                    if i.Locations[j][1] == playerWithBall:
                        playerWithBallX = i.Locations[j][0][0]
                        playerWithBallY = i.Locations[j][0][1]
        playerWithBallPoint = np.array([playerWithBallX,playerWithBallY])
        distance = np.linalg.norm(goalPoint-playerWithBallPoint)
        distance = distance/147

        shot = 1/(1 + np.exp(-(-1 + (0.2 * playerWithBall.finishing) + (-0.35 * distance))))
        print(f'Shot Success Rate: {shot}')
        return shot

    def make_decision(self,probabilities):
        """
        Make a decision based on probabilities.

        Parameters:
        - probabilities: A list of probabilities for each action.

        Returns:
        - The index of the chosen action.
        """
        rand_num = np.random.rand()
        cumulative_prob = 0.0
        player_has_ball = self.get_player_with_ball()

        # print(f'random number for make decisioNN: {rand_num}')
        # print(f'probbbabilietes{probabilities}')
        for i, prob in enumerate(probabilities):
            cumulative_prob += prob
            # print(f'Cumulative: {cumulative_prob}')
            if rand_num < cumulative_prob:
                return i

        # Fallback: Return the last index if no decision is made
        return len(probabilities) - 1

    def does_action_succeed(self,probability):
        low = 0.0
        high = 1.0
        rand_num = np.random.uniform(low, high, 1)
        # print(f'rand: {rand_num}')
        if probability > rand_num[0]:
            print("Action succeeds!")
            return True
        else:
            print("Action does not succeed")
            return False

    def softmax(self,z):
        """
        Compute softmax values for each element of the input array.

        Parameters:
        z : numpy.ndarray
            Input array of shape (n,) where n is the number of elements.

        Returns:
        numpy.ndarray
            Array of softmax probabilities of the same shape as input array.
        """
        exp_z = np.exp(z)
        return exp_z / np.sum(exp_z)


"""Creating the Player Sprites"""
def create_players_sprites():
    blue_img = pygame.image.load("Images/blueTeam.png")
    blue_surf = pygame.transform.scale(blue_img, (40, 25))
    blue_surf.set_colorkey("White")
    red_img = pygame.image.load("Images/redTeam.png")
    red_surf = pygame.transform.scale(red_img, (40, 25))
    red_surf.set_colorkey("White")
    return blue_surf, red_surf

