import pygame

def carregar_imagem(nome_arquivo, largura=None, altura=None):
    """Carrega imagem e redimensiona se necessário"""
    try:
        img = pygame.image.load(nome_arquivo).convert_alpha()
        if largura and altura:
            img = pygame.transform.scale(img, (largura, altura))
        return img
    except:
        print(f"Erro ao carregar imagem: {nome_arquivo}")
        return None

def desenhar_fundo_mario(TELA):
    """Desenha fundo estilo Mario"""
    # Céu gradiente
    for i in range(0, 600):
        cor = (135, 206, 235 - i//5)
        pygame.draw.line(TELA, cor, (0, i), (800, i))
    # Chão
    pygame.draw.rect(TELA, (139,69,19), (0,550,800,50))
    # Blocos decorativos
    for x in range(100,800,150):
        pygame.draw.rect(TELA,(255,215,0),(x,450,50,50))
        pygame.draw.rect(TELA,(255,215,0),(x+60,350,50,50))
