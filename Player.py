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

    """Draws player onto the self.win aka the main window"""

    def draw_players(self,win, zoneData):
        blue_tm, red_tm = create_players_sprites()
        #Go through ALL player objects
        for i in range(len(self.playersInfo)):
            if self.playersInfo[i].Team == "Manchester City":
                #Get the zone rect and the zone object
                zone_rect,zone_info = zoneData.get_zone(self.playersInfo[i].Index)

                #Use the zone rect to get the center of the zone!
                center_zonexY = (zone_rect.left + zone_rect.width / 2, zone_rect.top + zone_rect.height / 2)

                #Add player on the zone object, only if it's not already there!
                if self.playersInfo[i] not in zone_info.attached_players['Blue Team']:

                    zone_info.attached_players['Blue Team'].append(self.playersInfo[i])
                if len(zone_info.attached_players['Blue Team']) > 1:
                    pass

                #Create the Rect and depending on condition, add it to list of rectangles
                blue_rect = win.blit(blue_tm, center_zonexY)

                if len(self.game_players) < 20:
                    self.game_players.append(blue_rect)
            if self.playersInfo[i].Team == "Manchester United":
                zone_rect,zone_info = zoneData.get_zone(self.playersInfo[i].Index)
                center_zonexY = (zone_rect.left + zone_rect.width / 2, zone_rect.top + zone_rect.height / 2)


                if self.playersInfo[i] not in zone_info.attached_players['Red Team']:

                    zone_info.attached_players['Red Team'].append(self.playersInfo[i])
                if len(zone_info.attached_players['Red Team']) > 1:
                    #Find the player rect containing both of these
                    for i in range(len(self.game_players)):
                        pass
                    pass


                red_rect = win.blit(red_tm, center_zonexY)
                if len(self.game_players) < 20:

                    self.game_players.append(red_rect)






"""Creating the Player Sprites"""
def create_players_sprites():
    blue_img = pygame.image.load("Images/blueTeam.png")
    blue_surf = pygame.transform.scale(blue_img, (40, 25))
    blue_surf.set_colorkey("White")
    red_img = pygame.image.load("Images/redTeam.png")
    red_surf = pygame.transform.scale(red_img, (40, 25))
    red_surf.set_colorkey("White")
    return blue_surf, red_surf





