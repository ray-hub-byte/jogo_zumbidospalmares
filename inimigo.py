import pygame
import math

class Projetil(pygame.sprite.Sprite):
    def __init__(self, x, y, alvo_x, alvo_y):
        super().__init__()
        self.image = pygame.Surface((10,10))
        self.image.fill((255,0,0))
        self.rect = self.image.get_rect(center=(x,y))
        dx = alvo_x - x
        dy = alvo_y - y
        dist = math.hypot(dx, dy)
        if dist == 0:
            dist = 1
        self.vel_x = dx/dist * 5
        self.vel_y = dy/dist * 5

    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        if (self.rect.right < 0 or self.rect.left > 800 or
            self.rect.bottom < 0 or self.rect.top > 600):
            self.kill()

class Inimigo(pygame.sprite.Sprite):
    def __init__(self, x, y, largura, altura, img, caminho):
        super().__init__()
        self.original_img = img
        self.image = img
        self.rect = self.image.get_rect(topleft=(x, y))
        self.caminho = caminho
        self.vel = 2
        self.direcao = 1
        self.projeteis = pygame.sprite.Group()
        self.tempo_tiro = 0
        self.tempo_reload = 90

    def update(self, player):
        # Movimento horizontal
        self.rect.x += self.vel * self.direcao
        if self.rect.left < self.caminho[0]:
            self.rect.left = self.caminho[0]
            self.direcao = 1
        elif self.rect.right > self.caminho[1]:
            self.rect.right = self.caminho[1]
            self.direcao = -1

        # Virar imagem
        if self.direcao < 0:
            self.image = pygame.transform.flip(self.original_img, True, False)
        else:
            self.image = self.original_img

        # Atirar
        self.tempo_tiro += 1
        if self.tempo_tiro >= self.tempo_reload:
            self.tempo_tiro = 0
            self.atirar(player)

        self.projeteis.update()

    def atirar(self, player):
        proj = Projetil(self.rect.centerx, self.rect.centery,
                        player.rect.centerx, player.rect.centery)
        self.projeteis.add(proj)
