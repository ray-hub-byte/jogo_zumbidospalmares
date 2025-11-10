import pygame
import pygame_gui
import time
from player import Player
from plataforma import Plataforma
from inimigo import Inimigo
from tesouro import Tesouro
import math
import random
from sons import tocar_musica_fundo, efeito_botao, parar_musica
import finalizacao


pygame.init()
# Pegando a resolução do monitor
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h

# Inicializando em tela cheia
TELA = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
fullscreen = True  # flag para controle

pygame.display.set_caption("Jogo dos Palmares")
clock = pygame.time.Clock()
FONT_MSG = pygame.font.SysFont("arial", 26)  # Fonte ajustada para tesouros

# Inicia música de fundo contínua
tocar_musica_fundo()

# -----------------------------
# pygame_gui manager (menu)
# -----------------------------
manager = pygame_gui.UIManager((WIDTH, HEIGHT))
botao_jogar = pygame_gui.elements.UIButton(pygame.Rect((350, 250), (100, 50)), "Jogar", manager)
botao_sair = pygame_gui.elements.UIButton(pygame.Rect((350, 320), (100, 50)), "Sair", manager)

# -----------------------------
# helper: carregar imagem com fallback
# -----------------------------
def carregar_imagem(nome, largura=None, altura=None):
    try:
        img = pygame.image.load(nome).convert_alpha()
        if largura and altura:
            img = pygame.transform.scale(img, (largura, altura))
        return img
    except Exception as e:
        print(f"[WARNING] Erro ao carregar imagem '{nome}': {e}")
        surf = pygame.Surface((largura or 50, altura or 50), pygame.SRCALPHA)
        surf.fill((255, 0, 255))
        return surf

# -----------------------------
# Sprites / frames
# -----------------------------
dandara_idle = carregar_imagem("image (4).png", 50, 80)
dandara_run = carregar_imagem("image (5).png", 50, 80)
frames_dandara = [dandara_idle, dandara_run]

zumbi_idle = carregar_imagem("zumbiparado.png", 50, 80)
zumbi_run = carregar_imagem("zumbi correndo.png", 50, 80)
frames_zumbi = [zumbi_idle, zumbi_run]

inimigo_img = carregar_imagem("inimigo atirando.png", 50, 80)

tile_chao = carregar_imagem("chao.png", 50, 50)
tile_bloco = carregar_imagem("bloco.png", 50, 50)
tesouro_img = carregar_imagem("tesouro.png", 30, 30)

# -----------------------------
# Fundos
# -----------------------------
fundo_menu = carregar_imagem("inicio.png", WIDTH, HEIGHT)
fundo_deserto = carregar_imagem("deserto.png", WIDTH, HEIGHT)
fundo_navio = carregar_imagem("cenarionavio.png", WIDTH, HEIGHT)
fundo_plantacao = carregar_imagem("plantacao.png", WIDTH, HEIGHT)

# -----------------------------
# Funções para desenhar fundos
# -----------------------------
def desenhar_fundo_deserto(surface):
    surface.blit(fundo_deserto, (0, 0))
    for i in range(0, WIDTH, 50):
        surface.blit(tile_chao, (i, 550))

def desenhar_fundo_navio(surface):
    surface.blit(fundo_navio, (0, 0))
    for i in range(0, WIDTH, 50):
        surface.blit(tile_chao, (i, 550))

def desenhar_fundo_plantacao(surface):
    surface.blit(fundo_plantacao, (0, 0))
    for i in range(0, WIDTH, 50):
        surface.blit(tile_chao, (i, 550))

# -----------------------------
# Menu inicial
# -----------------------------
def menu_inicial():
    running = True
    while running:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                global fullscreen, WIDTH, HEIGHT, TELA
                if fullscreen:
                    WIDTH, HEIGHT = 800, 600  # tamanho da janela normal
                    TELA = pygame.display.set_mode((WIDTH, HEIGHT))
                    fullscreen = False
                else:
                    running = False  # fecha o loop da fase ou sai do jogo

            manager.process_events(event)

        manager.update(time_delta)
        TELA.blit(fundo_menu, (0,0))
        manager.draw_ui(TELA)
        pygame.display.update()

        if botao_jogar.check_pressed():
            efeito_botao()
            return "Jogar"
        if botao_sair.check_pressed():
            efeito_botao()
            return "Sair"

# -----------------------------
# Tela de seleção de personagem
# -----------------------------
def selecionar_personagem():
    global WIDTH, HEIGHT, TELA, fullscreen  # ⬅️ declare no início da função

    opcoes = {"Dandara": frames_dandara, "Zumbi": frames_zumbi}
    nomes = list(opcoes.keys())
    selected = 0
    FONT_TITULO = pygame.font.SysFont("arialblack", 42)
    FONT_NOME = pygame.font.SysFont("georgia", 28, bold=True)
    FONT_INSTRU = pygame.font.SysFont("verdana", 22)

    brilho = 0
    direcao = 1
    tempo = 0

    while True:
        clock.tick(60)
        tempo += 1
        TELA.fill((180, 140, 90))
        for y in range(0, HEIGHT, 2):
            r = 210 - int(40 * math.sin(tempo / 120 + y / 200))
            g = 180 - int(30 * math.sin(tempo / 160 + y / 300))
            b = 90 - int(20 * math.cos(tempo / 200))
            r = max(0, min(255, r))
            g = max(0, min(255, g))
            b = max(0, min(255, b))
            pygame.draw.line(TELA, (r, g, b), (0, y), (WIDTH, y))

        brilho += direcao * 3
        if brilho > 100:
            direcao = -1
        elif brilho < 0:
            direcao = 1
        cor_titulo = (255, 215 - brilho // 3, 100)
        titulo = FONT_TITULO.render("Escolha seu personagem", True, cor_titulo)
        TELA.blit(titulo, titulo.get_rect(center=(WIDTH // 2, HEIGHT // 6)))

        spacing = 320
        total_width = (len(opcoes) - 1) * spacing
        start_x = (WIDTH - total_width) // 2
        y_base = HEIGHT // 2 - 60

        for i, nome in enumerate(nomes):
            frames = opcoes[nome]
            imagem = frames[0]
            x = start_x + i * spacing
            deslocamento = int(6 * math.sin(tempo / 20 + i * math.pi / 2))
            y = y_base + deslocamento

            if i == selected:
                sombra = pygame.Surface((imagem.get_width()+14, imagem.get_height()+14), pygame.SRCALPHA)
                sombra.fill((90, 50, 10, 150))
                TELA.blit(sombra, (x-7, y-7))

                img_ampliada = pygame.transform.scale(
                    imagem,
                    (int(imagem.get_width() * 1.25), int(imagem.get_height() * 1.25))
                )
                TELA.blit(img_ampliada, (x, y-8))
                pygame.draw.rect(
                    TELA, (255, 215, 0),
                    (x-10, y-10, img_ampliada.get_width()+20, img_ampliada.get_height()+25),
                    4, border_radius=10
                )
                nome_render = FONT_NOME.render(nome, True, (90, 50, 10))
                TELA.blit(
                    nome_render,
                    nome_render.get_rect(center=(x + img_ampliada.get_width()//2, y + img_ampliada.get_height() + 40))
                )
            else:
                sombra = pygame.Surface((imagem.get_width(), imagem.get_height()), pygame.SRCALPHA)
                sombra.fill((60, 40, 10, 90))
                TELA.blit(sombra, (x, y))
                TELA.blit(imagem, (x + 6, y + 6))
                nome_render = FONT_NOME.render(nome, True, (230, 210, 180))
                TELA.blit(
                    nome_render,
                    nome_render.get_rect(center=(x + imagem.get_width()//2, y + imagem.get_height() + 35))
                )

        barra = pygame.Surface((WIDTH, 60))
        barra.fill((80, 50, 20))
        TELA.blit(barra, (0, HEIGHT - 70))
        instr = FONT_INSTRU.render("Use ← → para escolher e ENTER para confirmar", True, (255, 235, 190))
        TELA.blit(instr, instr.get_rect(center=(WIDTH // 2, HEIGHT - 40)))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None

            elif event.type == pygame.KEYDOWN:
                # ESC para sair da tela cheia ou voltar
                if event.key == pygame.K_ESCAPE:
                    if fullscreen:
                        # Sai da tela cheia, volta para janela
                        WIDTH, HEIGHT = 800, 600
                        TELA = pygame.display.set_mode((WIDTH, HEIGHT))
                        fullscreen = False
                    else:
                        # Se já não estiver fullscreen, volta para menu
                        return None

                # Teclas de navegação
                elif event.key == pygame.K_LEFT:
                    selected = (selected - 1) % len(opcoes)
                elif event.key == pygame.K_RIGHT:
                    selected = (selected + 1) % len(opcoes)
                elif event.key == pygame.K_RETURN:
                    efeito_botao()
                    return nomes[selected]


# -----------------------------
# Legendas
# -----------------------------
def mostrar_legenda(texto):
    FONT = pygame.font.SysFont(None, 30)
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return True

        TELA.fill((0,0,0))
        linhas = texto.split("\n")
        for i, linha in enumerate(linhas):
            r = FONT.render(linha, True, (255,255,255))
            TELA.blit(r, r.get_rect(center=(WIDTH//2, HEIGHT//2 - 20 + i*34)))
        instr = FONT_MSG.render("Pressione ESPAÇO para continuar", True, (200,200,200))
        TELA.blit(instr, instr.get_rect(center=(WIDTH//2, HEIGHT - 80)))
        pygame.display.update()

# -----------------------------
# Gerar plataformas aleatórias
# -----------------------------
def gerar_plataformas_aleatorias(num_blocos, largura_bloco=50, altura_bloco=20):
    blocos = []
    ALTURA_INICIAL = 500
    ESPACO_HORIZONTAL_MIN = 80
    ESPACO_HORIZONTAL_MAX = 200
    SALTO_VERTICAL_MAX = 120
    y_prev = ALTURA_INICIAL
    x_prev = 100

    for i in range(num_blocos):
        min_y = max(100, y_prev - SALTO_VERTICAL_MAX)
        max_y = min(500, y_prev + SALTO_VERTICAL_MAX)
        y = random.randint(min_y, max_y)
        x = x_prev + random.randint(ESPACO_HORIZONTAL_MIN, ESPACO_HORIZONTAL_MAX)
        if x > 750:
            x = random.randint(50, 700)
        blocos.append((x, y, largura_bloco, altura_bloco))
        x_prev, y_prev = x, y
    return blocos

# -----------------------------
# Função jogar
# -----------------------------
def jogar():
    personagem = selecionar_personagem()
    if not personagem:
        return

    frames_personagem = frames_dandara if personagem == "Dandara" else frames_zumbi

    # Legendas de introdução
    legendas_intro = [
        "Bem-vindo ao Jogo dos Palmares.",
        "Você irá explorar lugares de resistência e memória.",
        "A busca pela liberdade começa agora."
    ]
    for texto in legendas_intro:
        ok = mostrar_legenda(texto)
        if not ok:
            return

    fases = [
        {"fundo_draw": desenhar_fundo_deserto, "num_blocos": 7, 
         "inimigos":[{"x":200,"y":480,"img":inimigo_img,"caminho":[250,650]}], 
         "tesouros":[{"x":430,"y":80,"frase":"Antes da escravidão, povos africanos viviam em comunidades livres, com suas culturas, línguas e tradições."}]},
        {"fundo_draw": desenhar_fundo_navio, "num_blocos": 6, 
         "inimigos":[{"x":150,"y":480,"img":inimigo_img,"caminho":[150,400]},{"x":550,"y":480,"img":inimigo_img,"caminho":[550,750]}], 
         "tesouros":[{"x":720,"y":250,"frase":"Milhares foram capturados à força e arrancados de suas casas e famílias. Sendo levados por navios negreiros que cruzaram o Atlântico, trazendo sofrimento, doenças e morte."}]},
        {"fundo_draw": desenhar_fundo_plantacao, "num_blocos": 6, 
         "inimigos":[{"x":150,"y":480,"img":inimigo_img,"caminho":[150,360]},{"x":500,"y":480,"img":inimigo_img,"caminho":[500,720]}], 
         "tesouros":[{"x":720,"y":230,"frase":"A Lei Áurea de 1888 libertou legalmente os escravizados no Brasil. Mas a liberdade sem terras ou trabalho ainda limitava suas oportunidades."}]}
    ]

    for fase_idx, fase in enumerate(fases):
        def reiniciar_fase():
            plataformas = pygame.sprite.Group()
            escadas = pygame.sprite.Group()
            inimigos = pygame.sprite.Group()
            tesouros = pygame.sprite.Group()
            todas_sprites = pygame.sprite.Group()
            player = Player(100, 470, {"frames": frames_personagem})
            player.morreu = False
            todas_sprites.add(player)

            plat_chao = Plataforma(0, 550, WIDTH, 50)
            plat_chao.image = tile_chao
            plataformas.add(plat_chao)
            todas_sprites.add(plat_chao)

            blocos = gerar_plataformas_aleatorias(fase["num_blocos"])
            for b in blocos:
                plat = Plataforma(*b)
                plat.image = tile_bloco
                plataformas.add(plat)
                todas_sprites.add(plat)

            for t in fase["tesouros"]:
                tes = Tesouro(t["x"], t["y"], t["frase"])
                tesouros.add(tes)
                todas_sprites.add(tes)

            for inim_info in fase["inimigos"]:
                inim = Inimigo(inim_info["x"], inim_info["y"], 50, 50, img=inim_info["img"], caminho=inim_info["caminho"])
                inimigos.add(inim)
                todas_sprites.add(inim)
            return player, plataformas, escadas, inimigos, tesouros, todas_sprites

        player, plataformas, escadas, inimigos, tesouros, todas_sprites = reiniciar_fase()
        mensagem = ""
        pausa = False
        running = True

        legenda_fase = f"Fase {fase_idx+1} - Boa sorte!"
        ok = mostrar_legenda(legenda_fase)
        if not ok:
            return

        while running:
            dt = clock.tick(60)

            # Captura eventos
            eventos = pygame.event.get()
            for event in eventos:
                if event.type == pygame.QUIT:
                    parar_musica()
                    return
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        global fullscreen, WIDTH, HEIGHT, TELA
                        if fullscreen:
                            # Sai do fullscreen e volta para janela normal
                            WIDTH, HEIGHT = 800, 600
                            TELA = pygame.display.set_mode((WIDTH, HEIGHT))
                            fullscreen = False
                        else:
                            # Se já estiver em janela normal, fecha o jogo
                            running = False


                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and pausa:
                    pausa = False
                    mensagem = ""

            # Coleta tesouros
            coletados = pygame.sprite.spritecollide(player, tesouros, True)
            if coletados:
                mensagem = coletados[0].frase
                pausa = True  # pausa total do jogo

            # Atualiza jogador e inimigos se não estiver em pausa
            if not pausa:
                player.update(plataformas, escadas)
                for inim in inimigos:
                    inim.update(player)

            # Checa colisões mesmo em pausa
            for inim in list(inimigos):
                if getattr(player, "vel_y", 0) > 0 and player.rect.bottom >= inim.rect.top and player.rect.bottom - getattr(player, "vel_y", 0) < inim.rect.top:
                    if player.rect.right > inim.rect.left + 5 and player.rect.left < inim.rect.right - 5:
                        inim.kill()
                        player.vel_y = -10

            for inim in inimigos:
                if player.rect.colliderect(inim.rect):
                    if not (getattr(player, "vel_y", 0) > 0 and player.rect.bottom >= inim.rect.top and player.rect.bottom - getattr(player, "vel_y", 0) < inim.rect.top and player.rect.right > inim.rect.left + 5 and player.rect.left < inim.rect.right - 5):
                        player.morreu = True
                        break

            for inim in inimigos:
                if hasattr(inim, "projeteis"):
                    if pygame.sprite.spritecollide(player, inim.projeteis, True):
                        player.morreu = True
                        break

            # Desenha fundo e sprites
            fase["fundo_draw"](TELA)
            todas_sprites.draw(TELA)
            inimigos.draw(TELA)
            for inim in inimigos:
                if hasattr(inim, "projeteis"):
                    inim.projeteis.draw(TELA)

            if pausa and mensagem:
                     
                largura_caixa = 700
                altura_caixa = 200
                x_caixa = (WIDTH - largura_caixa) // 2
                y_caixa = (HEIGHT - altura_caixa) // 2
                caixa = pygame.Surface((largura_caixa, altura_caixa), pygame.SRCALPHA)
                caixa.fill((0, 0, 0, 210))

                fonte_tesouro = pygame.font.SysFont("georgia", 20, bold=False)

                # Quebra automática de linha (sem considerar ponto final)
                palavras = mensagem.split(" ")
                linhas = []
                linha_atual = ""

                for palavra in palavras:
                    teste = linha_atual + (" " if linha_atual else "") + palavra
                    # só quebra se a linha ultrapassar a largura permitida
                    if fonte_tesouro.size(teste)[0] > largura_caixa - 80:
                        linhas.append(linha_atual)
                        linha_atual = palavra
                    else:
                        linha_atual = teste
                if linha_atual:
                    linhas.append(linha_atual)

                # Divide em páginas se o texto for muito longo
                linhas_por_pagina = 5
                paginas = [linhas[i:i + linhas_por_pagina] for i in range(0, len(linhas), linhas_por_pagina)]
                pagina_atual = 0
                mostrando = True

                while mostrando:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            exit()
                        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                            pagina_atual += 1
                            if pagina_atual >= len(paginas):
                                mostrando = False
                                pausa = False
                                mensagem = None
                                break

                    fase["fundo_draw"](TELA)
                    todas_sprites.draw(TELA)
                    inimigos.draw(TELA)
                    for inim in inimigos:
                        if hasattr(inim, "projeteis"):
                            inim.projeteis.draw(TELA)

                    if pagina_atual < len(paginas):
                        # desenha a caixa
                        TELA.blit(caixa, (x_caixa, y_caixa))
                        pagina = paginas[pagina_atual]
                        espacamento_linha = 34
                        inicio_y = y_caixa + (altura_caixa - len(pagina) * espacamento_linha) // 2

                        for i, linha in enumerate(pagina):
                            render = fonte_tesouro.render(linha, True, (255, 255, 255))
                            rect = render.get_rect(center=(WIDTH // 2, inicio_y + i * espacamento_linha))
                            TELA.blit(render, rect)

                        # legenda do botão
                        fonte_instrucao = pygame.font.SysFont("arial", 18)
                        instrucao = fonte_instrucao.render("[ESPAÇO] para continuar", True, (200, 200, 200))
                        rect_instr = instrucao.get_rect(center=(WIDTH // 2, y_caixa + altura_caixa - 20))
                        TELA.blit(instrucao, rect_instr)

                    pygame.display.update()
                    clock.tick(60)





            # Reiniciar fase se morreu
            if player.morreu:
                TELA.fill((0,0,0))
                fase["fundo_draw"](TELA)
                todas_sprites.draw(TELA)
                s = pygame.Surface((780, 100), pygame.SRCALPHA)
                s.fill((0,0,0,180))
                TELA.blit(s, (10,200))
                txt = FONT_MSG.render("Você foi atingido! Reiniciando fase...", True, (255,255,255))
                TELA.blit(txt, (20,230))
                pygame.display.update()
                pygame.time.delay(1200)
                player, plataformas, escadas, inimigos, tesouros, todas_sprites = reiniciar_fase()
                continue

            pygame.display.update()

            # Avança fase apenas se todos os tesouros forem coletados e jogador chegou ao final
            if len(tesouros) == 0 and player.rect.right >= 780 and not pausa:
                running = False
    # Quando todas as fases terminarem:
    parar_musica()               # para a música do jogo
    finalizacao.tela_final()     # chama sua tela final com a história e música de vitória
    return


# -----------------------------
# Loop principal
# -----------------------------
def main():
    running = True
    while running:
        escolha = menu_inicial()

        if escolha == "Jogar":
            # Remove botões do menu atual
            for element in manager.get_root_container().elements.copy():
                element.kill()

            # Executa o jogo
            jogar()

            # 🔄 Após o jogo terminar, recria os botões e volta ao menu
            global botao_jogar, botao_sair
            botao_jogar = pygame_gui.elements.UIButton(pygame.Rect((350, 250), (100, 50)), "Jogar", manager)
            botao_sair = pygame_gui.elements.UIButton(pygame.Rect((350, 320), (100, 50)), "Sair", manager)

        elif escolha == "Sair":
            running = False

    parar_musica()
    pygame.quit()


if __name__ == "__main__":
    main()
