import pygame

class Tesouro(pygame.sprite.Sprite):
    def __init__(self, x, y, frase, imagem_path="tesouro.png"):
        super().__init__()
        try:
            self.image = pygame.image.load(imagem_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (30, 30))  # tamanho ajustável
        except:
            # Caso a imagem não carregue, cria um quadrado colorido
            self.image = pygame.Surface((30, 30))
            self.image.fill((255, 215, 0))  # amarelo dourado

        self.rect = self.image.get_rect(topleft=(x, y))
        self.frase = frase
 
