import pygame
"""插入 image,gif,button等类"""


class Button:
    def __init__(self, text, position, color, font, scale, event, mid_width=0, mid_height=0,
                 bk_color=(150, 150, 150, 150), effect=True):
        image = get_text_surface(text, color, font)
        width, height = image.get_size()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        x_pos = mid_width - int(width * scale / 2) if mid_width else position[0]
        y_pos = mid_height - int(height * scale / 2) if mid_height else position[1]

        self.rect.topleft = (x_pos, y_pos)
        self.clicked = False
        self.event = event
        self.bk_color = bk_color
        self.effect = effect

    def draw(self, surface, surface_position):
        action = False
        bk = pygame.draw.rect(surface, self.bk_color, self.rect)

        # 获取鼠标位置：
        pos = pygame.mouse.get_pos()
        pos = (list(pos)[0] - surface_position[0], list(pos)[1] - surface_position[1])

        if self.effect:
            pygame.draw.rect(surface, (255, 255, 255), self.rect, 3)
        # 鼠标划过按钮并点击
        if bk.collidepoint(pos):
            if self.effect:
                pygame.draw.rect(surface, (255, 0, 0), self.rect, 3)
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                config.audio_dict['button'].play()
                self.clicked = True
                action = True

        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False

        surface.blit(self.image, self.rect.topleft)

        return action