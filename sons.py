import pygame

pygame.mixer.init()

musica = None

def tocar_musica_fundo():
    global musica
    if musica is None:
        musica = pygame.mixer.Sound("music.wav")  # coloque aqui seu arquivo de música
        musica.set_volume(0.3)  # volume ajustável
        musica.play(loops=-1)    # loops=-1 para tocar continuamente
    return musica

def parar_musica():
    global musica
    if musica:
        musica.stop()
        musica = None

def efeito_botao():
    try:
        som = pygame.mixer.Sound("botao.wav")  # coloque aqui seu arquivo de efeito de botão
        som.set_volume(2.0)  # volume baixo para não ser muito forte
        som.play()
    except Exception as e:
        print(f"[ERRO] Não foi possível tocar o efeito: {e}") 
