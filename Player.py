import numpy as np
import time
import random
import pygame
class Player:
    def __init__(self,fname,lname,hasBall,currentZone,Team):
        self.fname = fname
        self.lname = lname
        self.fullName = str(f'{self.fname} {self.lname}')
        self.hasBall = hasBall
        self.Index = currentZone
        self.Team = Team
        self.placedOnLocation = False # Used when adjusting the player rect

    def move(self, FutureZone):
        self.currentZone = FutureZone
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
    def dribble_player_right(self,zoneData):
        #Get the player with the ball b/c he will be the player deciding the first move and then everybody reacts
        player = self.get_player_with_ball()

        # Get the zone object the player is on
        zone = zoneData.zoneInfo[player.Index - 1]
        futureZone = zoneData.zoneInfo[player.Index]

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

    def dribble_player_left(self,zoneData):
        player = self.get_player_with_ball()
        zone = zoneData.zoneInfo[player.Index - 1]
        futureZone = zoneData.zoneInfo[player.Index-2]

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

    def dribble_player_up(self,zoneData):
        player = self.get_player_with_ball()
        zone = zoneData.zoneInfo[player.Index - 1]

        futureZoneIndex = zone.index - 11

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
    def dribble_player_down(self,zoneData):
        player = self.get_player_with_ball()
        zone = zoneData.zoneInfo[player.Index - 1]

        futureZoneIndex = zone.index + 11

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

    def player_pass_randomly(self):
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

        # Standard delete player and reinsert it into self.playerRect
        player_rect_from_dict = self.playerRects[player_has_ball]
        del self.playerRects[player_has_ball]
        player_has_ball.hasBall = False
        self.playerRects[player_has_ball] = player_rect_from_dict

        player_rect_from_dict = self.playerRects[player_recieve_ball]
        del self.playerRects[player_recieve_ball]
        player_recieve_ball.hasBall = True
        self.playerRects[player_recieve_ball] = player_rect_from_dict



"""Creating the Player Sprites"""
def create_players_sprites():
    blue_img = pygame.image.load("Images/blueTeam.png")
    blue_surf = pygame.transform.scale(blue_img, (40, 25))
    blue_surf.set_colorkey("White")
    red_img = pygame.image.load("Images/redTeam.png")
    red_surf = pygame.transform.scale(red_img, (40, 25))
    red_surf.set_colorkey("White")
    return blue_surf, red_surf

