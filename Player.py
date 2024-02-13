import numpy as np
import time
import pygame
class Player:
    def __init__(self,fname,lname,hasBall,currentZone,Team):
        self.fname = fname
        self.lname = lname
        self.hasBall = hasBall
        self.Index = currentZone
        self.Team = Team

    def move(self, FutureZone):
        self.currentZone = FutureZone
    def __hash__(self):
        return hash((self.fname, self.lname,self.hasBall,self.Index,self.Team))




    def get_pass_success(self, passing, target_zone):
        
        zones_away = self.get_zones_away(target_zone)
        dfp_arnd = self.check_dfp_arnd_target()
        dfp_in = self.check_dfp_in_target()

        if dfp_arnd == False:
                
            denominator = 1 + np.exp((-0.25 * passing) + (0.25 * zones_away) + (0.6 * dfp_in))
        else:
            ant_attr = "1." + str()
            
            denominator = 1 + np.exp(((-0.25 * passing) + (0.25 * zones_away) + (0.6 * dfp_in))/float(ant_attr))
        return 1/(denominator)

    def get_zones_away(self,target_zone):
        pass

    def check_dfp_arnd_target(self):
        pass



class PlayerData:
    def __init__(self,playersInfo):
        self.game_players = [] #rects of players
        self.playersInfo = playersInfo #List of Player Objects
        self.playerRects = {}

    """Draws player onto the self.win aka the main window"""

    def draw_players(self,win):
        blue_tm, red_tm = create_players_sprites()
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
                if self.playersInfo[i] not in zone_info.attached_players['Blue Team']:

                    zone_info.attached_players['Blue Team'].append(self.playersInfo[i])
                player_rect = pygame.Rect(center_zonexY[0],center_zonexY[1],blue_tm.get_width(),blue_tm.get_height())
                self.playerRects[self.playersInfo[i]] = player_rect
            if self.playersInfo[i].Team == "Manchester United":
                zone_rect,zone_info = zoneData.get_zone(self.playersInfo[i].Index)
                center_zonexY = (zone_rect.left + zone_rect.width / 2, zone_rect.top + zone_rect.height / 2)


                if self.playersInfo[i] not in zone_info.attached_players['Red Team']:

                    zone_info.attached_players['Red Team'].append(self.playersInfo[i])
                player_rect = pygame.Rect(center_zonexY[0], center_zonexY[1], blue_tm.get_width(), blue_tm.get_height())
                self.playerRects[self.playersInfo[i]] = player_rect








"""Creating the Player Sprites"""
def create_players_sprites():
    blue_img = pygame.image.load("Images/blueTeam.png")
    blue_surf = pygame.transform.scale(blue_img, (40, 25))
    blue_surf.set_colorkey("White")
    red_img = pygame.image.load("Images/redTeam.png")
    red_surf = pygame.transform.scale(red_img, (40, 25))
    red_surf.set_colorkey("White")
    return blue_surf, red_surf





