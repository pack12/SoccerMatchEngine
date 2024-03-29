import pygame
class Ball:
    def __init__(self):
        self.currentIndex = 0
        self.playerAttached = None
        self.x = None
        self.y = None
    def create_ball(self):
        ball_surf = pygame.image.load("Images/soccerBall.png")
        ball_surf = pygame.transform.scale(ball_surf,(20,16))
        ball_surf.set_colorkey("Black")
        return ball_surf

    def update_index(self,futureIndex):
        self.currentIndex = futureIndex
    def draw_ball(self,win,playerData,zoneData):
        ball_surf = self.create_ball()

        for i in playerData.playerRects:
            if i.hasBall== True and i.Team == "Manchester City":

                # Get the player rect
                playerRect = playerData.playerRects[i]
                self.x = playerRect[0] - 10
                self.y = playerRect[1]
                self.currentIndex = i.Index
                self.playerAttached = i

            elif i.hasBall == True and i.Team == "Manchester United":
                playerRect = playerData.playerRects[i]
                self.x = playerRect[0] + 25
                self.y = playerRect[1]
                self.currentIndex = i.Index
                self.playerAttached = i
                # print(f'Ball current index: {self.currentIndex}')
        if self.playerAttached == None:
            # print(f'Ball current index: {self.currentIndex}')
            self.x = zoneData.zoneInfo[self.currentIndex-1].x - 80
            self.y = zoneData.zoneInfo[self.currentIndex-1].y + 50

        ball_rect = pygame.Rect(self.x,self.y, ball_surf.get_width(), ball_surf.get_height())
        win.blit(ball_surf, ball_rect)





