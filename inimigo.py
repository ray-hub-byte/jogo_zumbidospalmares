import pygame
import math

class Inimigo(pygame.sprite.Sprite):
    def __init__(self, x, y, largura, altura, img=None, caminho=None):
        super().__init__()
        # Imagem do inimigo
        if img:
            self.image = pygame.transform.scale(img,(largura,altura))
        else:
            self.image = pygame.Surface((largura,altura))
            self.image.fill((255,0,0))
        self.rect = self.image.get_rect(topleft=(x,y))
        
        # Caminho horizontal opcional
        self.caminho = caminho if caminho else [x]
        self.indice_caminho = 0
        self.vel = 2
        
        # Projetéis
        self.projeteis = pygame.sprite.Group()
        self.tempo_tiro = 0  # contador de frames

        # Direção para flip
        self.direita = True

    def update(self, player=None):
        # -----------------------------
        # Movimento seguindo o caminho
        # -----------------------------
        if len(self.caminho) > 1:
            destino = self.caminho[self.indice_caminho]
            if self.rect.x < destino:
                self.rect.x += self.vel
                self.direita = True
            elif self.rect.x > destino:
                self.rect.x -= self.vel
                self.direita = False
            if abs(self.rect.x - destino) < self.vel:
                self.indice_caminho = (self.indice_caminho + 1) % len(self.caminho)

        # -----------------------------
        # Disparo em direção ao player
        # -----------------------------
        if player:
            self.tempo_tiro += 1
            if self.tempo_tiro >= 120:  # a cada 1,5 segundos
                proj = Projetil(self.rect.centerx, self.rect.centery, player.rect.centerx, player.rect.centery)
                self.projeteis.add(proj)
                self.tempo_tiro = 0

        # Atualizar projéteis
        self.projeteis.update()

class Projetil(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y):
        super().__init__()
        self.image = pygame.Surface((10,10))
        self.image.fill((0,0,0))
        self.rect = self.image.get_rect(center=(x,y))

        # Calcular vetor de direção
        dx = target_x - x
        dy = target_y - y
        dist = math.hypot(dx, dy)
        if dist == 0:
            dist = 1
        self.vel_x = dx/dist * 1
        self.vel_y = dy/dist * 1

    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        if self.rect.top > 600 or self.rect.bottom < 0 or self.rect.left>800 or self.rect.right<0:
            self.kill()
