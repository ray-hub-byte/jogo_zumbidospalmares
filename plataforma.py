import pygame

class Plataforma(pygame.sprite.Sprite):
    def __init__(self, x, y, largura, altura):
        super().__init__()
        self.image = pygame.Surface((largura, altura))
        self.image.fill((160,82,45))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
