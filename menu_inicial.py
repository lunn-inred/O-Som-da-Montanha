import sys

import pygame

import config
from config import *

class main_menu:
    def __init__(self,fases):
        # definicoes gerais
        self.superficie_tela = pygame.display.get_surface()
        self.background = pygame.image.load("./graficos/main_menu/background.png").convert_alpha()
        self.creditos = pygame.image.load("./graficos/main_menu/Créditos.png").convert_alpha()
        self.controles = pygame.image.load(("./graficos/main_menu/Controles.png")).convert_alpha()
        self.background1 = pygame.transform.scale(self.background,(largura,altura))
        self.rect = self.superficie_tela.get_rect()
        self.fases = fases
        self.valor_max = list(config.volume_max.values())



        self.numero_atributos = 5
        self.numero_opcoes = 2
        self.nome_atibutos = ["Iniciar","Opções","Controles","Créditos","Sair"]
        self.nome_opcoes = ["Músicas","Efeitos"]
        self.gameover = ["Continuar"]

        self.fonte = pygame.font.Font(fonte_inter,tamanho_fonte)

        # dimenções dos itens
        self.altura = self.superficie_tela.get_size()[1]//10
        self.largura = self.superficie_tela.get_size()[0]*0.6 -500
        self.largura_op = self.superficie_tela.get_size()[0] * 0.6
        self.altura_op = self.superficie_tela.get_size()[1] // 10 +15
        self.criar()

        # sistema de selecao
        self.indice_select = 0
        self.indice_select_op = 0
        self.tempo_select = None
        self.pode_mexer = True

    def entradas(self):
        teclas = pygame.key.get_pressed()
        lmb = pygame.mouse.get_pressed()[0]
        if self.pode_mexer:
            if not self.fases.opcoes:
                if teclas[pygame.K_s] or teclas[pygame.K_DOWN]:
                    if self.indice_select < self.numero_atributos - 1:
                        self.indice_select += 1
                        self.pode_mexer = False
                        self.tempo_select = pygame.time.get_ticks()
                elif teclas[pygame.K_w] or teclas[pygame.K_UP]:
                    if self.indice_select >= 1:
                        self.indice_select -= 1
                        self.pode_mexer = False
                        self.tempo_select = pygame.time.get_ticks()

                if teclas[pygame.K_SPACE] or teclas[pygame.K_KP_ENTER] or lmb or teclas[pygame.K_RETURN]:
                    self.pode_mexer = False
                    self.tempo_select = pygame.time.get_ticks()
                    self.lista[self.indice_select].acao(self.fases,self.nome_atibutos[self.indice_select])

            else:
                if teclas[pygame.K_s] or teclas[pygame.K_DOWN]:
                    if self.indice_select_op < self.numero_opcoes - 1:
                        self.indice_select_op += 1
                        self.pode_mexer = False
                        self.tempo_select = pygame.time.get_ticks()
                elif teclas[pygame.K_w] or teclas[pygame.K_UP]:
                    if self.indice_select_op >= 1:
                        self.indice_select_op -= 1
                        self.pode_mexer = False
                        self.tempo_select = pygame.time.get_ticks()
                if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
                    self.lista_op[self.indice_select_op].acao(self.fases,self.nome_opcoes[self.indice_select_op])
                if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
                    self.lista_op[self.indice_select_op].acao(self.fases,self.nome_opcoes[self.indice_select_op]+"1")
        for evento in pygame.event.get():
            mousex, mousey = pygame.mouse.get_pos()

            if evento.type == pygame.MOUSEMOTION:
                if mousex >= 551 and mousex <= 775:
                    if mousey >= 159 and mousey <= 226:
                        self.indice_select = 0
                    if mousey >= 251 and mousey <= 319:
                        self.indice_select = 1
                    if mousey >= 339 and mousey <= 406:
                        self.indice_select = 2
                    if mousey >= 429 and mousey <= 498:
                        self.indice_select = 3
                    if mousey >= 519 and mousey <= 588:
                        self.indice_select = 4
    def pegarValor_indice(self, indice):
        return list(config.volume.values())[indice]

    def cooldown(self):
        if not self.pode_mexer:
            momento_atual = pygame.time.get_ticks()
            if momento_atual - self.tempo_select >= 300:
                self.pode_mexer = True


    def criar(self):
        self.lista = []
        for item, indice in enumerate(range(self.numero_atributos)):
            # posicao horizontal
            altura_total = self.superficie_tela.get_size()[1]//2
            incremento = altura_total//4
            # esq = self.superficie_tela.get_size()[1]*0.1
            esq = self.superficie_tela.get_size()[0]//2 - 130

            # posicao vertical
            topo = (item * incremento) + (incremento - self.altura)//2 + 150

            item = Items(esq,topo,self.largura,self.altura,indice,self.fonte)
            self.lista.append(item)
        self.lista_op = []
        for item, indice in enumerate(range(self.numero_opcoes)):
            # posicao horizontal
            altura_total = self.superficie_tela.get_size()[1]//2 + 100
            incremento = altura_total//self.numero_atributos
            # esq = self.superficie_tela.get_size()[1]*0.1
            esq = self.superficie_tela.get_size()[0]//2 - 380

            # posicao vertical
            topo = (item * incremento) + (incremento - self.altura_op)//2 + 200

            item = Items(esq,topo,self.largura_op,self.altura_op,indice,self.fonte)
            self.lista_op.append(item)

    def tela(self):

        self.superficie_tela.blit(self.background1,self.rect)

        self.entradas()
        self.cooldown()

        if self.fases.opcoes:

            teclas = pygame.key.get_pressed()
            if teclas[pygame.K_ESCAPE]:
                self.fases.opcoes = False
            for indice, item in enumerate(self.lista_op):
                nome = self.nome_opcoes[indice]
                valor_max = self.valor_max[indice]
                valor = self.pegarValor_indice(indice)
                item.tela(self.superficie_tela, self.indice_select_op, nome)
                item.barra(self.superficie_tela,valor,valor_max,self.indice_select_op)
        elif self.fases.creditos:
            self.superficie_tela.blit(self.creditos, self.rect)
            teclas = pygame.key.get_pressed()
            if teclas[pygame.K_ESCAPE]:
                self.fases.creditos = False

        elif self.fases.controles:
            self.superficie_tela.blit(self.controles, self.rect)
            teclas = pygame.key.get_pressed()
            if teclas[pygame.K_ESCAPE]:
                self.fases.controles = False

        else:
            for indice, item in enumerate(self.lista):
                nome = self.nome_atibutos[indice]
                item.tela(self.superficie_tela,self.indice_select,nome)


class Items:
    def __init__(self,esq,topo,l,a,indice,fonte):
        self.rect = pygame.Rect(esq,topo,l,a)
        self.indice = indice
        self.fonte = fonte


    def nomes(self,superficie,nome,selecionado):

        # cores
        cor = texto_selecionado if selecionado else cor_texto

        # titulo
        surf_titulo = self.fonte.render(nome,False,cor)
        rect_titulo = surf_titulo.get_rect(midtop = self.rect.midtop + pygame.math.Vector2(0,20))

        # desenhar na tela
        superficie.blit(surf_titulo, rect_titulo)



    def acao(self,fases,nome):
        if nome == "Iniciar":
            fases.personagem.rodando = False
            fases.personagem.jogando = True
        if nome == "Sair":
            pygame.quit()
            sys.exit()
        if nome == "Opções":
            fases.opcoes = True
        if nome == "Créditos":
            fases.creditos = True
        if nome == "Controles":
            fases.controles = True
        if nome == "Músicas":
            config.volume["musica"] += 0.01
            if config.volume["musica"] >=config.volume_max["musica"]:
                config.volume["musica"] = config.volume_max["musica"]
        if nome == "Efeitos":
            config.volume["efeitos"] += 0.01
            if config.volume["efeitos"] >=config.volume_max["efeitos"]:
                config.volume["efeitos"] = config.volume_max["efeitos"]
        if nome == "Músicas1":
            config.volume["musica"] -= 0.01
            if config.volume["musica"] <= 0:
                config.volume["musica"] = 0
        if nome == "Efeitos1":
            config.volume["efeitos"] -= 0.01
            if config.volume["efeitos"] <=0:
                config.volume["efeitos"] = 0


    def barra(self, superficie, valor, valor_max, selecionado):
        # posições
        esq = self.rect.midleft + pygame.math.Vector2(60, 10)
        direita = self.rect.midright - pygame.math.Vector2(60, -10)
        cor = cor_barra_selecionado

        altura_total = direita[0] - esq[0]
        valor_relativo = (valor / valor_max) * altura_total
        rect_valor = pygame.Rect(esq[0] + valor_relativo, esq[1] - 15, 10, 30)

        pygame.draw.line(superficie, cor, esq, direita, 5)
        pygame.draw.rect(superficie, cor, rect_valor)
        valor_atual = self.fonte.render(f"{int(valor*100)}%", False, cor)
        rect_atual = pygame.Rect(esq[0] + valor_relativo, esq[1]+10, 30, 10)
        superficie.blit(valor_atual, rect_atual)


    def tela(self,superficie,num_selecao,nome):

        if self.indice == num_selecao:
            pygame.draw.rect(superficie, cor_fundo_upgrade, self.rect)
            pygame.draw.rect(superficie, cor_borda_inter, self.rect, 4)
        else:
            pygame.draw.rect(superficie,cor_fundo_inter,self.rect)
            pygame.draw.rect(superficie,cor_borda_inter,self.rect,4)

        self.nomes(superficie,nome,self.indice == num_selecao)
