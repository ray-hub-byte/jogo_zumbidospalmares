import pygame
from player import Player
from plataforma import Plataforma
from inimigo import Inimigo
from tesouro import Tesouro

pygame.init()
TELA = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Jogo dos Palmares")
clock = pygame.time.Clock()
FONT = pygame.font.SysFont(None, 36)

# -----------------------------
# Função para carregar imagens
# -----------------------------
def carregar_imagem(nome_arquivo):
    """Tenta carregar a imagem e retorna None se não existir"""
    try:
        return pygame.image.load(nome_arquivo).convert_alpha()
    except FileNotFoundError:
        print(f"Arquivo não encontrado: {nome_arquivo}")
        return None

# -----------------------------
# Carregar imagens dos personagens
# -----------------------------
# Zumbi (imagem única)
zumbi_img = carregar_imagem("zumbiDP.png")

# Dandara (3 imagens: parada, andando, correndo)
frames_dandara = []
for i in range(4, 7):  # image(4).png = parada, image(5).png = andando, image(6).png = correndo
    img = carregar_imagem(f"dandara/image({i}).png")
    if img:
        frames_dandara.append(img)

# -----------------------------
# Definir personagens
# -----------------------------
personagens = {
    "Zumbi dos Palmares": {"img": zumbi_img},
    "Dandara dos Palmares": {"frames": frames_dandara}
}

personagem_escolhido = None

# -----------------------------
# Menu de seleção de personagem
# -----------------------------
def menu_personagem():
    global personagem_escolhido
    selected = 0
    opcoes = list(personagens.keys())
    selecionando = True

    while selecionando:
        TELA.fill((30, 30, 30))

        # Título
        titulo = FONT.render("Selecione seu personagem", True, (255, 255, 255))
        TELA.blit(titulo, (220, 50))

        # Mostrar personagens
        for i, nome in enumerate(opcoes):
            dados = personagens[nome]
            rect = pygame.Rect(150 + i*300, 200, 200, 250)

            # Mostrar imagem parada ou primeiro frame da animação
            if dados.get("img"):
                TELA.blit(pygame.transform.scale(dados["img"], (150, 200)), (rect.x + 25, rect.y))
            elif dados.get("frames") and len(dados["frames"]) > 0:
                TELA.blit(pygame.transform.scale(dados["frames"][0], (150, 200)), (rect.x + 25, rect.y))
            else:
                pygame.draw.rect(TELA, (255, 0, 0), rect)
                txt = pygame.font.SysFont(None, 28).render("Sem imagem", True, (255, 255, 255))
                TELA.blit(txt, (rect.x + 35, rect.y + 100))

            # Nome do personagem
            nome_texto = FONT.render(nome, True, (255, 255, 255))
            TELA.blit(nome_texto, (rect.x, rect.y + 210))

            # Destaque do selecionado
            if i == selected:
                pygame.draw.rect(TELA, (255, 255, 0), rect, 5)

        # Instruções
        instr = pygame.font.SysFont(None, 24).render("Use ← → e ENTER para escolher", True, (255, 255, 255))
        TELA.blit(instr, (180, 520))

        pygame.display.update()

        # Eventos do teclado
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    selected = (selected - 1) % len(opcoes)
                elif event.key == pygame.K_RIGHT:
                    selected = (selected + 1) % len(opcoes)
                elif event.key == pygame.K_RETURN:
                    personagem_escolhido = opcoes[selected]
                    return personagem_escolhido
                elif event.key == pygame.K_ESCAPE:
                    return None

# -----------------------------
# Função principal do jogo
# -----------------------------
def jogar_palmares():
    global personagem_escolhido
    if not personagem_escolhido:
        print("Escolha primeiro um personagem!")
        return

    # Grupos de sprites
    todas_sprites = pygame.sprite.Group()
    plataformas = pygame.sprite.Group()
    inimigos = pygame.sprite.Group()
    tesouros = pygame.sprite.Group()

    # Criar jogador com imagens corretas
    dados = personagens[personagem_escolhido]
    player = Player(100, 500, dados)
    todas_sprites.add(player)

    # Criar plataformas
    plat1 = Plataforma(0, 580, 800, 20)
    plat2 = Plataforma(200, 450, 200, 20)
    plat3 = Plataforma(500, 350, 200, 20)
    plataformas.add(plat1, plat2, plat3)
    todas_sprites.add(plataformas)

    # Criar inimigos
    inimigo1 = Inimigo(300, 420, 50, 30)
    inimigos.add(inimigo1)
    todas_sprites.add(inimigos)

    # Criar tesouros (curiosidades históricas)
    curiosidades = [
        "Os quilombos eram comunidades formadas por escravizados que fugiam.",
        "A capoeira era uma forma de resistência cultural.",
        "Muitos escravizados mantinham suas tradições e religiões africanas.",
        "O trabalho nos engenhos era extremamente exaustivo e perigoso.",
        "A música e a dança eram formas de preservar identidade e cultura."
    ]
    for i, frase in enumerate(curiosidades):
        x = 150 + i*120
        y = 300 - i*30
        tesouro = Tesouro(x, y, frase)
        tesouros.add(tesouro)
        todas_sprites.add(tesouro)

    mensagem = ""
    running = True
    while running:
        clock.tick(60)

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Atualizar todos os sprites
        todas_sprites.update(plataformas)

        # Colisão com inimigos
        if pygame.sprite.spritecollideany(player, inimigos):
            print("Você perdeu!")
            running = False

        # Coleta de tesouros
        coletados = pygame.sprite.spritecollide(player, tesouros, True)
        if coletados:
            mensagem = coletados[0].frase
            print("Tesouro coletado:", mensagem)

        # Desenhar tudo
        TELA.fill((135, 206, 235))  # fundo azul
        todas_sprites.draw(TELA)

        # Mostrar mensagem do tesouro
        if mensagem:
            FONT_MSG = pygame.font.SysFont(None, 28)
            txt = FONT_MSG.render(mensagem, True, (255, 255, 255))
            TELA.blit(txt, (10, 550))

        pygame.display.update()

# -----------------------------
# Menu principal
# -----------------------------
running = True
while running:
    TELA.fill((50, 50, 50))
    options = ["1 - Escolher Personagem", "2 - Jogar", "0 - Sair"]
    for i, opt in enumerate(options):
        txt = FONT.render(opt, True, (255, 255, 255))
        TELA.blit(txt, (200, 150 + i*60))
    pygame.display.update()

    # Eventos do menu
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                menu_personagem()
            elif event.key == pygame.K_2:
                jogar_palmares()
            elif event.key == pygame.K_0:
                running = False

pygame.quit()
