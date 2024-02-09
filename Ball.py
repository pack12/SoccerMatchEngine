import pygame
class Ball:
    def __init__(self):
        self.currentIndex = 0
        self.playerAttached = ""
    def create_ball(self):
        ball_surf = pygame.image.load("Images/soccerBall.png")
        ball_surf = pygame.transform.scale(ball_surf,(20,12))
        ball_surf.set_colorkey("Black")
        return ball_surf

    def update_index(self,futureIndex):
        self.currentIndex = futureIndex

