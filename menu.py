import pygame

def menu_personagem(TELA, FONT, personagens):
    selected = 0
    opcoes = list(personagens.keys())
    selecionando = True
    personagem_escolhido = None

    while selecionando:
        TELA.fill((135,206,235))
        titulo = FONT.render("Selecione seu personagem", True, (255,0,0))
        TELA.blit(titulo, titulo.get_rect(center=(400,50)))

        spacing = 250
        total_width = spacing*(len(opcoes)-1)+150
        start_x = (800-total_width)//2

        for i, nome in enumerate(opcoes):
            dados = personagens[nome]
            x = start_x + i*spacing
            y = 200

            if dados.get("img"):
                TELA.blit(dados["img"], (x,y))
            elif dados.get("frames") and len(dados["frames"])>0:
                TELA.blit(dados["frames"][0], (x,y))
            else:
                pygame.draw.rect(TELA,(0,0,0),(x,y,150,200))

            if " " in nome:
                primeiro, segundo = nome.split(" ",1)
            else:
                primeiro, segundo = nome,""
            TELA.blit(FONT.render(primeiro,True,(255,255,255)),(x+25,y+210))
            TELA.blit(FONT.render(segundo,True,(255,255,255)),(x+25,y+240))

            if i == selected:
                pygame.draw.rect(TELA,(255,0,0),(x-5,y-5,160,210),5)

        instr = FONT.render("Use ← → e ENTER para escolher",True,(255,255,255))
        TELA.blit(instr,instr.get_rect(center=(400,520)))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    selected = (selected-1)%len(opcoes)
                elif event.key == pygame.K_RIGHT:
                    selected = (selected+1)%len(opcoes)
                elif event.key == pygame.K_RETURN:
                    personagem_escolhido = opcoes[selected]
                    return personagem_escolhido
                elif event.key == pygame.K_ESCAPE:
                    return None
 
