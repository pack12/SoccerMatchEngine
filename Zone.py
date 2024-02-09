import pygame
class Zone:
    def __init__(self):
        self.width = 145
        self.height = 147
        self.x = 0
        self.y = 20
        self.attached_players = {"Red Team":[], "Blue Team":[]}
        self.location_name = ""
        self.index = 0
class ZoneData:
    def __init__(self):
        self.zoneInfo = [] #List of Zone objects
        self.zones = [] #actual rects

    """This is where the rects and zones are made"""

    def create_zone_board(self):
        zone = Zone()
        for j in range(6):

            zone.x = 52

            for i in range(11):
                self.zones.append(pygame.Rect(zone.x, zone.y, zone.width, zone.height))
                zone.x += zone.width

                # Creating a copy Zone to reference
                newZone = Zone()
                newZone.x = zone.x
                newZone.y = zone.y
                newZone.index = (i + 1) + (j * 11)
                self.zoneInfo.append(newZone)

            zone.y += zone.height


    """Used to get the Zone Rect, based on the Index"""
    """Returns Rect of Zone"""

    def get_zone(self,index):

        for i in range(len(self.zoneInfo)):
            if self.zoneInfo[i].index == index:

                for j in range(len(self.zones)):
                    if j == i:
                        return self.zones[j]

    """Draw zones onto self.win"""

    def draw_zones(self,win):
        for i in range(len(self.zones)):
            pygame.draw.rect(win, 'black', self.zones[i], 2)

    """Checks to see if mouse pos is in zone"""

    def check_mouse_in_zone(self):
        # Get the position of the mouse
        mouse_x, mouse_y = pygame.mouse.get_pos()
        print(f'Mousex: {mouse_x} and Mousey: {mouse_y}')
        for i in range(len(self.zones)):
            if self.zones[i].collidepoint(mouse_x, mouse_y):
                print(f'Index: {self.zoneInfo[i].index}')

    # def update(self,game_players):
    #     for i in range(len(self.zoneInfo)):
