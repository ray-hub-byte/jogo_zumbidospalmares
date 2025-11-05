import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, dados):
        super().__init__()
        self.frames = dados.get("frames", [])
        self.img_unica = dados.get("img", None)

        # Inicializa a imagem corretamente
        if self.frames:
            self.image = self.frames[0]
        elif self.img_unica:
            self.image = self.img_unica
        else:
            self.image = pygame.Surface((40,50))
            self.image.fill((255,0,255))  # fallback rosa se nada existir

        self.rect = self.image.get_rect(topleft=(x, y))

        # Movimento
        self.vel_x = 0
        self.vel_y = 0
        self.speed = 5
        self.jump = False
        self.direita = True
        self.frame_index = 0
        self.anim_counter = 0

        # Ataque corpo a corpo
        self.atacando = False
        self.attack_cooldown = 0
        self.attack_range = 40

        # Escada
        self.em_escada = False

        # Controle de chão para pulo
        self.no_chao = False

    def update(self, plataformas, escadas=None):
        keys = pygame.key.get_pressed()
        moving = False

        # Movimento horizontal
        self.vel_x = 0
        if keys[pygame.K_LEFT]:
            self.vel_x = -self.speed
            moving = True
            self.direita = False
        if keys[pygame.K_RIGHT]:
            self.vel_x = self.speed
            moving = True
            self.direita = True

        # Subir/descer escada
        self.em_escada = False
        if escadas:
            col_escada = pygame.sprite.spritecollide(self, escadas, False)
            if col_escada:
                self.em_escada = True
                self.vel_y = 0
                if keys[pygame.K_UP]:
                    self.rect.y -= self.speed
                if keys[pygame.K_DOWN]:
                    self.rect.y += self.speed

        # Pulo
        if keys[pygame.K_SPACE] and self.no_chao and not self.em_escada:
            self.vel_y = -15  # pulo mais alto
            self.jump = True

        # Gravidade
        if not self.em_escada:
            self.vel_y += 0.6
            if self.vel_y > 12:
                self.vel_y = 12

        # Movimenta horizontal e aplica colisão
        self.mover_horizontal(plataformas)

        # Movimenta vertical e aplica colisão
        self.mover_vertical(plataformas)

        # Limites da tela
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 800:
            self.rect.right = 800
        if self.rect.bottom > 600:
            self.rect.bottom = 600
            self.vel_y = 0
            self.jump = False
            self.no_chao = True

        # Ataque corpo a corpo
        self.atacando = False
        if keys[pygame.K_x] and self.attack_cooldown == 0:
            self.atacando = True
            self.attack_cooldown = 20
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        # Animação
        if self.frames:
            self.anim_counter += 1
            if self.atacando and len(self.frames) > 2:
                self.frame_index = 2  # ataque
            elif moving:
                self.frame_index = 1 if len(self.frames) > 1 else 0  # correndo
            else:
                self.frame_index = 0  # idle
            frame = self.frames[self.frame_index]
            self.image = frame if self.direita else pygame.transform.flip(frame, True, False)

    # --------------------------
    # Movimento Horizontal
    # --------------------------
    def mover_horizontal(self, plataformas):
        self.rect.x += self.vel_x
        for plat in plataformas:
            if self.rect.colliderect(plat.rect):
                # Colisão lateral: só ajusta se houver sobreposição vertical
                if self.rect.bottom > plat.rect.top + 5 and self.rect.top < plat.rect.bottom - 5:
                    if self.vel_x > 0:
                        self.rect.right = plat.rect.left
                    elif self.vel_x < 0:
                        self.rect.left = plat.rect.right
                    self.vel_x = 0

    # --------------------------
    # Movimento Vertical
    # --------------------------
    def mover_vertical(self, plataformas):
        prev_rect = self.rect.copy()
        self.rect.y += self.vel_y
        self.no_chao = False

        for plat in plataformas:
            if self.rect.colliderect(plat.rect):
                # Colisão caindo (player vinha de cima)
                if prev_rect.bottom <= plat.rect.top and self.vel_y > 0:
                    self.rect.bottom = plat.rect.top
                    self.vel_y = 0
                    self.jump = False
                    self.no_chao = True
                # Colisão subindo (player vinha de baixo)
                elif prev_rect.top >= plat.rect.bottom and self.vel_y < 0:
                    self.rect.top = plat.rect.bottom
                    self.vel_y = 0
