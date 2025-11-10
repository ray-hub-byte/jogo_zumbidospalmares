import pygame

class Plataforma(pygame.sprite.Sprite):
    def __init__(self, x, y, largura, altura, imagem=None):
        super().__init__()
        if imagem:
            self.image = pygame.transform.scale(imagem, (largura, altura))
        else:
            self.image = pygame.Surface((largura, altura))
            self.image.fill((160,82,45))
        self.rect = self.image.get_rect(topleft=(x, y))
 
