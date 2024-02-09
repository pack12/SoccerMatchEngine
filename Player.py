import numpy as np
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

    """Creating the Player Sprites"""

def create_players_sprites():
    blue_img = pygame.image.load("Images/blueTeam.png")
    blue_surf = pygame.transform.scale(blue_img, (40, 25))
    blue_surf.set_colorkey("White")
    red_img = pygame.image.load("Images/redTeam.png")
    red_surf = pygame.transform.scale(red_img, (40, 25))
    red_surf.set_colorkey("White")
    return blue_surf, red_surf



"""Draws player onto the self.win aka the main window"""
def draw_players(game_players,win,zoneData):
    blue_tm,red_tm = create_players_sprites()
    for i in range(len(game_players)):
        if game_players[i].Team == "Manchester City":

            zone_rect = zoneData.get_zone(game_players[i].Index)
            center_zone_rect = (zone_rect.left + zone_rect.width/2,zone_rect.top + zone_rect.height/2)

            win.blit(blue_tm,center_zone_rect)
        if game_players[i].Team == "Manchester United":
            zone_rect = zoneData.get_zone(game_players[i].Index)
            center_zone_rect = (zone_rect.left + zone_rect.width/2, zone_rect.top + zone_rect.height/2)
            win.blit(red_tm, center_zone_rect)

