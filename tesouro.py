import pygame

class Tesouro(pygame.sprite.Sprite):
    def __init__(self, x, y, frase):
        super().__init__()
        self.image = pygame.Surface((30,30))
        self.image.fill((255,215,0))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.frase = frase
