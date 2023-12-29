# 敌方大本营类
import pygame
import home

class EnemyHome(home.Home):
    def __init__(self,stage):
        home.Home.__init__()
        self.homes = ["img1", " ","" ]
        self.home = pygame.image.load(self)
        self.times = 300  # 设置时间
        self.stage = stage  # 关卡，不同关卡的enemy home不同

    # 随着事件
    # def situation(self):
    #     self.home = pygame.image.load(self.homes[])
    #     if self.times =













