import pygame
import math
from player import Player
from plataforma import Plataforma
from inimigo import Inimigo
from tesouro import Tesouro

pygame.init()
TELA = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Jogo dos Palmares")
clock = pygame.time.Clock()
FONT = pygame.font.SysFont(None, 36)
FONT_MSG = pygame.font.SysFont(None, 28)

# -----------------------------
# Função para carregar imagens
# -----------------------------
def carregar_imagem(nome_arquivo, width=None, height=None):
    try:
        img = pygame.image.load(nome_arquivo).convert_alpha()
        if width and height:
            img = pygame.transform.scale(img, (width, height))
        return img
    except:
        print(f"Não encontrado: {nome_arquivo}")
        return None

# -----------------------------
# Carregar imagens dos personagens
# -----------------------------
zumbi_parado = carregar_imagem("zumbiparado.png", 80, 100)
zumbi_correndo = carregar_imagem("zumbicorrendo.png", 80, 100)
frames_zumbi = [f for f in [zumbi_parado, zumbi_correndo] if f]

dandara_parada = carregar_imagem("image (4).png", 80, 100)
dandara_correndo = carregar_imagem("image (5).png", 80, 100)
frames_dandara = [f for f in [dandara_parada, dandara_correndo] if f]

personagens = {
    "Zumbi dos\nPalmares": {"frames": frames_zumbi},
    "Dandara dos\nPalmares": {"frames": frames_dandara}
}

# -----------------------------
# Menu inicial estilo Mario
# -----------------------------
def menu_inicial(TELA, FONT, personagens):
    options = ["Jogar", "Créditos", "Sair"]
    selected = 0
    anim_counter = 0
    running = True

    zumbi_frames = personagens["Zumbi dos\nPalmares"].get("frames", [])
    dandara_frames = personagens["Dandara dos\nPalmares"].get("frames", [])

    while running:
        clock.tick(60)
        TELA.fill((139, 69, 19))  # fundo marrom

        # Chão estilo Mario
        for i in range(0, 800, 50):
            pygame.draw.rect(TELA, (205, 133, 63), (i, 550, 48, 50))
            pygame.draw.rect(TELA, (139, 69, 19), (i + 5, 555, 38, 40))

        # Letreiro semi-transparente
        s = pygame.Surface((600, 50), pygame.SRCALPHA)
        s.fill((0, 0, 0, 120))
        TELA.blit(s, (100, 20))
        titulo = FONT.render("Jogo dos Palmares", True, (255, 223, 186))
        TELA.blit(titulo, titulo.get_rect(center=(400, 45)))

        # Personagens animados
        if zumbi_frames:
            idx = (anim_counter // 10) % len(zumbi_frames)
            TELA.blit(zumbi_frames[idx], (200, 400 + 5 * math.sin(anim_counter * 0.1)))
        if dandara_frames:
            idx = (anim_counter // 10) % len(dandara_frames)
            TELA.blit(dandara_frames[idx], (500, 400 + 5 * math.sin(anim_counter * 0.1)))

        # Menu horizontal
        for i, opt in enumerate(options):
            cor = (255, 255, 0) if i == selected else (255, 255, 255)
            txt = FONT.render(opt, True, cor)
            TELA.blit(txt, txt.get_rect(center=(400, 200 + i * 80)))

        pygame.display.update()
        anim_counter += 1

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    return options[selected]

# -----------------------------
# Menu de escolha de personagem
# -----------------------------
def menu_personagem(TELA, FONT, personagens):
    opcoes = list(personagens.keys())
    selected = 0
    running = True

    while running:
        TELA.fill((139, 69, 19))
        titulo = FONT.render("Selecione seu personagem", True, (255, 223, 186))
        TELA.blit(titulo, (200, 50))

        for i, nome in enumerate(opcoes):
            dados = personagens[nome]
            rect = pygame.Rect(150 + i * 250, 200, 150, 200)
            if dados.get("frames"):
                TELA.blit(dados["frames"][0], (rect.x, rect.y))
            else:
                pygame.draw.rect(TELA, (0, 0, 0), rect)

            nome_texto = FONT.render(nome, True, (255, 255, 255))
            TELA.blit(nome_texto, (rect.x, rect.y + 210))

            if i == selected:
                pygame.draw.rect(TELA, (255, 255, 0), rect, 4)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    selected = (selected - 1) % len(opcoes)
                elif event.key == pygame.K_RIGHT:
                    selected = (selected + 1) % len(opcoes)
                elif event.key == pygame.K_RETURN:
                    return opcoes[selected]

# -----------------------------
# Fases do jogo
# -----------------------------
fases = [
    {
        "plataformas": [(0, 580, 800, 20), (200, 450, 200, 20), (500, 350, 200, 20)],
        "inimigos": [{"x": 300, "y": 420, "img": "inimigo atirando.png", "caminho": [300, 500]}],
        "tesouros": [
            {"x": 150, "y": 300, "frase": "Os quilombos eram comunidades formadas por escravizados que fugiam."},
            {"x": 500, "y": 300, "frase": "A capoeira era uma forma de resistência cultural."}
        ]
    },
    {
        "plataformas": [(0, 580, 800, 20), (150, 450, 200, 20), (450, 350, 200, 20)],
        "inimigos": [{"x": 400, "y": 420, "img": "inimigo.png", "caminho": [400, 600]}],
        "tesouros": [
            {"x": 200, "y": 300, "frase": "Muitos escravizados mantinham suas tradições e religiões africanas."},
            {"x": 500, "y": 250, "frase": "O trabalho nos engenhos era extremamente exaustivo e perigoso."}
        ]
    }
]

# -----------------------------
# Jogar fase com mensagens pausáveis e ataque corpo a corpo
# -----------------------------
def jogar(personagem_escolhido):
    for fase in fases:
        todas_sprites = pygame.sprite.Group()
        plataformas = pygame.sprite.Group()
        inimigos = pygame.sprite.Group()
        tesouros = pygame.sprite.Group()

        dados = personagens[personagem_escolhido]
        player = Player(100, 500, dados)
        todas_sprites.add(player)

        # Plataformas
        for p in fase["plataformas"]:
            plat = Plataforma(*p)
            plataformas.add(plat)
            todas_sprites.add(plat)

        # Tesouros
        for t in fase["tesouros"]:
            tes = Tesouro(t["x"], t["y"], t["frase"])
            tesouros.add(tes)
            todas_sprites.add(tes)

        # Inimigos
        for i in fase["inimigos"]:
            img = carregar_imagem(i["img"], 50, 50)
            inim = Inimigo(i["x"], i["y"], 50, 50, img, caminho=i["caminho"])
            inimigos.add(inim)
            todas_sprites.add(inim)

        mensagem = ""
        pausa = False
        running = True
        while running:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN:
                    if pausa and event.key == pygame.K_SPACE:
                        pausa = False
                        mensagem = ""

            if not pausa:
                # Atualizar player e inimigos
                todas_sprites.update(plataformas)
                for inim in inimigos:
                    inim.update(player)

                # Colisão com inimigos
                for inim in inimigos:
                    # Pisando em cima mata o inimigo
                    if player.vel_y > 0 and player.rect.bottom <= inim.rect.top + 15 and \
                       player.rect.right > inim.rect.left and player.rect.left < inim.rect.right:
                        inim.kill()
                        player.vel_y = -10  # impulso
                    # Ataque corpo a corpo (tecla X)
                    elif player.atacando and abs(player.rect.centerx - inim.rect.centerx) < player.attack_range and \
                         abs(player.rect.centery - inim.rect.centery) < player.attack_range:
                        inim.kill()

                # Checar projéteis
                for inim in inimigos:
                    if pygame.sprite.spritecollideany(player, inim.projeteis):
                        print("Você foi atingido!")
                        return

                # Coletar tesouros e pausar
                coletados = pygame.sprite.spritecollide(player, tesouros, True)
                if coletados:
                    mensagem = coletados[0].frase
                    pausa = True

            # Desenhar
            TELA.fill((135, 206, 235))
            for i in range(0, 800, 50):
                pygame.draw.rect(TELA, (205, 133, 63), (i, 550, 48, 50))
                pygame.draw.rect(TELA, (139, 69, 19), (i + 5, 555, 38, 40))

            todas_sprites.draw(TELA)
            for inim in inimigos:
                inim.projeteis.draw(TELA)

            # Mensagem do tesouro
            if mensagem:
                s = pygame.Surface((780, 100), pygame.SRCALPHA)
                s.fill((0,0,0,180))
                TELA.blit(s, (10, 200))
                txt = FONT_MSG.render(mensagem, True, (255, 255, 255))
                TELA.blit(txt, (20, 230))

            pygame.display.update()

            # Passar de fase
            if player.rect.right >= 780 and not pausa:
                running = False

    print("Parabéns! Você completou todas as fases!")

# -----------------------------
# Loop principal
# -----------------------------
running = True
while running:
    escolha = menu_inicial(TELA, FONT, personagens)
    if escolha == "Jogar":
        personagem = menu_personagem(TELA, FONT, personagens)
        if personagem:
            jogar(personagem)
    elif escolha == "Créditos":
        print("Créditos do jogo...")
        pygame.time.wait(2000)
    else:
        running = False

pygame.quit()
