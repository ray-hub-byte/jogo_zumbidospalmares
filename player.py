import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, dados):
        super().__init__()
        self.frames = dados.get("frames", [])
        self.img_unica = dados.get("img", None)
        self.image = self.img_unica if self.img_unica else (self.frames[0] if self.frames else pygame.Surface((40,50)))
        self.rect = self.image.get_rect(topleft=(x,y))

        # Movimento
        self.vel_y = 0
        self.jump = False
        self.speed = 5
        self.direita = True
        self.frame_index = 0
        self.anim_counter = 0

        # Ataque corpo a corpo
        self.attack_cooldown = 0
        self.attack_range = 40
        self.atacando = False

    def update(self, plataformas):
        keys = pygame.key.get_pressed()
        moving = False

        # Movimento horizontal
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            moving = True
            self.direita = False
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            moving = True
            self.direita = True

        # Pular
        if keys[pygame.K_SPACE] and not self.jump:
            self.vel_y = -15
            self.jump = True

        # Ataque corpo a corpo
        self.atacando = False
        if keys[pygame.K_x] and self.attack_cooldown == 0:
            self.atacando = True
            self.attack_cooldown = 20

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        # Gravidade
        self.vel_y += 0.8
        self.rect.y += self.vel_y

        # Colisão com plataformas
        col_plat = pygame.sprite.spritecollide(self, plataformas, False)
        for plat in col_plat:
            if self.vel_y > 0:
                self.rect.bottom = plat.rect.top
                self.vel_y = 0
                self.jump = False

        # Animação
        if self.frames:
            self.anim_counter += 1
            if self.atacando and len(self.frames) > 2:
                self.frame_index = 2
            elif moving:
                self.frame_index = 1 if len(self.frames) > 1 else 0
            else:
                self.frame_index = 0
            frame = self.frames[self.frame_index]
            if self.direita:
                self.image = frame
            else:
                self.image = pygame.transform.flip(frame, True, False)
