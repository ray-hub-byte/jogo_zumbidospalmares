import pygame
import sys
import menu  # Certifique-se de que há um arquivo menu.py com a função tela_menu()

pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 800, 600
TELA = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Final do Jogo - A Busca por Liberdade")

# Fontes e cores
fonte_texto = pygame.font.Font(None, 34)
fonte_titulo = pygame.font.Font(None, 60)
fonte_botao = pygame.font.Font(None, 36)

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
CINZA = (50, 50, 50)
VERDE = (20, 180, 20)

# Caminho dos arquivos (ajuste se necessário)
MUSICA_VITORIA = "musica_vitoria.mp3"
IMAGEM_VITORIA = "vitoria.png"


def mostrar_texto_interativo(linhas):
    """Mostra o texto linha por linha, centralizado, avançando com espaço."""
    clock = pygame.time.Clock()
    indice = 0
    esperando = False

    while indice < len(linhas):
        TELA.fill(PRETO)
        linha = linhas[indice]

        # Centraliza o texto na tela
        texto_render = fonte_texto.render(linha, True, BRANCO)
        x = WIDTH // 2 - texto_render.get_width() // 2
        y = HEIGHT // 2 - texto_render.get_height() // 2
        TELA.blit(texto_render, (x, y))

        instrucao = fonte_texto.render("Pressione [ESPAÇO] para continuar", True, (150, 150, 150))
        TELA.blit(instrucao, (WIDTH // 2 - instrucao.get_width() // 2, HEIGHT - 100))

        pygame.display.flip()

        esperando = True
        while esperando:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        esperando = False
            clock.tick(30)
        indice += 1


def desenhar_botao(texto, x, y, largura, altura, cor_normal, cor_hover, pos_mouse):
    """Desenha o botão e muda de cor se o mouse passar por cima."""
    if x < pos_mouse[0] < x + largura and y < pos_mouse[1] < y + altura:
        pygame.draw.rect(TELA, cor_hover, (x, y, largura, altura), border_radius=10)
    else:
        pygame.draw.rect(TELA, cor_normal, (x, y, largura, altura), border_radius=10)

    texto_render = fonte_botao.render(texto, True, BRANCO)
    TELA.blit(texto_render, (x + (largura - texto_render.get_width()) // 2,
                             y + (altura - texto_render.get_height()) // 2))


def tela_final():
    """Tela de encerramento com história interativa e tela de vitória."""

    historia = [
        "Os escravos foram libertados...",
        "Mas a liberdade não trouxe o descanso que esperavam.",
        "Sem terras, sem direitos e sem acolhimento,",
        "foram deixados à própria sorte, em um país que ainda os negava.",
        "Mesmo assim, resistiram. Criaram quilombos, comunidades e cultura.",
        "A força de Zumbi e Dandara vive em cada gesto de resistência,",
        "em cada pessoa que luta por igualdade e dignidade.",
        "A liberdade foi apenas o começo..."
    ]

    # Parte 1: Tela preta com texto centralizado e avanço por espaço
    mostrar_texto_interativo(historia)

    # Parte 2: Tela de vitória
    try:
        fundo = pygame.image.load(IMAGEM_VITORIA)
        fundo = pygame.transform.scale(fundo, (WIDTH, HEIGHT))
    except:
        fundo = None

    pygame.mixer.music.load(MUSICA_VITORIA)
    pygame.mixer.music.play(-1)

    clock = pygame.time.Clock()
    rodando = True

    # Botão "Voltar ao menu"
    botao_largura = 220
    botao_altura = 60
    botao_x = WIDTH // 2 - botao_largura // 2
    botao_y = HEIGHT - 120

    while rodando:
        pos_mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if botao_x < pos_mouse[0] < botao_x + botao_largura and botao_y < pos_mouse[1] < botao_y + botao_altura:
                    # Voltar ao menu principal
                    pygame.mixer.music.stop()
                    import main
                    main.main()
                    return


        # Fundo
        if fundo:
            TELA.blit(fundo, (0, 0))
        else:
            TELA.fill(PRETO)


        # Botão
        desenhar_botao("Voltar ao menu", botao_x, botao_y, botao_largura, botao_altura,
                       CINZA, VERDE, pos_mouse)

        pygame.display.flip()
        clock.tick(60)

    pygame.mixer.music.stop()
    pygame.quit()


# Para testar isoladamente
if __name__ == "__main__":
    tela_final()
