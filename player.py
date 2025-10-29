import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, dados_personagem):
        super().__init__()

        # -------------------------------
        # Carregar imagens separadas
        # Cada imagem representa uma ação do personagem
        # -------------------------------
        self.parado = None   # imagem quando parado
        self.andando = []    # imagens quando andando
        self.correndo = []   # imagens quando correndo (opcional)
        self.index = 0       # índice de animação
        self.counter = 0     # contador para controlar velocidade da animação
        self.vel_y = 0       # velocidade vertical (gravidade)
        self.jump = False    # flag para pular
        self.speed = 5       # velocidade horizontal

        # Se for imagem única (ex: Zumbi parado)
        if dados_personagem.get("img"):
            self.parado = pygame.transform.scale(dados_personagem["img"], (50, 70))
            self.andando = [self.parado]  # usa a mesma imagem para andar

        # Se for Dandara com várias imagens
        elif dados_personagem.get("frames"):
            frames = dados_personagem["frames"]
            # Supondo que você tenha 3 imagens:
            # frames[0] = parada
            # frames[1] = andando
            # frames[2] = correndo
            if len(frames) >= 3:
                self.parado = pygame.transform.scale(frames[0], (50, 70))
                self.andando = [pygame.transform.scale(frames[1], (50, 70))]
                self.correndo = [pygame.transform.scale(frames[2], (50, 70))]
            else:
                # se tiver menos imagens, usar a primeira para tudo
                self.parado = pygame.transform.scale(frames[0], (50, 70))
                self.andando = [self.parado]

        # Se não tiver imagens, usar retângulo colorido
        else:
            cor = dados_personagem.get("cor", (255, 0, 0))
            surf = pygame.Surface((40, 50))
            surf.fill(cor)
            self.parado = surf
            self.andando = [surf]

        # Imagem inicial
        self.image = self.parado
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    # -------------------------------
    # Atualização do Player
    # -------------------------------
    def update(self, plataformas):
        keys = pygame.key.get_pressed()
        andando = False

        # Movimentação horizontal
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            andando = True
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            andando = True

        # Pular
        if keys[pygame.K_SPACE]:
            if not self.jump:
                self.vel_y = -15
                self.jump = True

        # Gravidade
        self.vel_y += 0.8
        self.rect.y += self.vel_y

        # Colisão com plataformas
        col_plataformas = pygame.sprite.spritecollide(self, plataformas, False)
        for plat in col_plataformas:
            if self.vel_y > 0:  # caindo
                self.rect.bottom = plat.rect.top
                self.vel_y = 0
                self.jump = False

        # -------------------------------
        # Troca de imagens (animação)
        # -------------------------------
        if andando and len(self.andando) > 0:
            # Quando andando, alterna os frames
            self.counter += 1
            if self.counter >= 10:  # a cada 10 ticks troca o frame
                self.counter = 0
                self.index = (self.index + 1) % len(self.andando)
                self.image = self.andando[self.index]
        else:
            # Se não está andando, mostra imagem parada
            self.image = self.parado
