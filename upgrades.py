import pygame
from config import *

class Upgrade:
    def __init__(self,personagem):
        # definicoes gerais
        self.superficie_tela = pygame.display.get_surface()
        self.personagem = personagem
        self.numero_atributos = len(personagem.stats)
        self.nome_atibutos = list(personagem.stats.keys())
        self.valor_max = list(personagem.max_stats.values())
        self.fonte = pygame.font.Font(fonte_inter,tamanho_fonte)
        self.fundinho = pygame.Surface((1280, 720))
        self.fundinho.set_alpha(127)
        self.fundinho.fill("black")

        # dimenções dos itens
        self.altura = self.superficie_tela.get_size()[1]*0.8
        self.largura = self.superficie_tela.get_size()[0]//6
        self.criar()

        # sistema de selecao
        self.indice_select = 0
        self.tempo_select = None
        self.pode_mexer = True

    def entradas(self):
        teclas = pygame.key.get_pressed()
        lmb = pygame.mouse.get_pressed()[0]
        if self.pode_mexer:
            if teclas[pygame.K_d] or teclas[pygame.K_RIGHT]:
                if self.indice_select < self.numero_atributos - 1:
                    self.indice_select += 1
                    self.pode_mexer = False
                    self.tempo_select = pygame.time.get_ticks()
            elif teclas[pygame.K_a] or teclas[pygame.K_LEFT]:
                if self.indice_select >= 1:
                    self.indice_select -= 1
                    self.pode_mexer = False
                    self.tempo_select = pygame.time.get_ticks()

            if teclas[pygame.K_SPACE] or teclas[pygame.K_KP_ENTER] or lmb:
                self.pode_mexer = False
                self.tempo_select = pygame.time.get_ticks()
                self.lista[self.indice_select].upar(self.personagem)
        for evento in pygame.event.get():
            mousex, mousey = pygame.mouse.get_pos()

            if evento.type == pygame.MOUSEMOTION:
                if mousey >= 73 and mousey <= 645:
                    if mousex >= 53 and mousex <= 265:
                        self.indice_select = 0
                    if mousex >= 374 and mousex <= 584:
                        self.indice_select = 1
                    if mousex >= 695 and mousex <= 905:
                        self.indice_select = 2
                    if mousex >= 1013 and mousex <= 1225:
                        self.indice_select = 3

    def cooldown(self):
        if not self.pode_mexer:
            momento_atual = pygame.time.get_ticks()
            if momento_atual - self.tempo_select >= 300:
                self.pode_mexer = True


    def criar(self):
        self.lista = []
        for item, indice in enumerate(range(self.numero_atributos)):
            # posicao horizontal
            largura_total = self.superficie_tela.get_size()[0]
            incremento = largura_total//self.numero_atributos
            esq = (item * incremento) + (incremento-self.largura)//2

            # posicao vertical
            topo = self.superficie_tela.get_size()[1]*0.1

            item = Items(esq,topo,self.largura,self.altura,indice,self.fonte)
            self.lista.append(item)

    def tela(self):
        self.entradas()
        self.cooldown()
        self.superficie_tela.blit(self.fundinho,(0,0))
        for indice, item in enumerate(self.lista):
            nome = self.nome_atibutos[indice]
            valor = self.personagem.pegarValor_indice(indice)
            valor_max = self.valor_max[indice]
            custo = self.personagem.pegarCusto_indice(indice)
            item.tela(self.superficie_tela,self.indice_select,nome,valor,valor_max,custo)


class Items:
    def __init__(self,esq,topo,l,a,indice,fonte):
        self.rect = pygame.Rect(esq,topo,l,a)
        self.indice = indice
        self.fonte = fonte

    def nomes(self,superficie,nome,custo,selecionado):

        # cores
        cor = texto_selecionado if selecionado else cor_texto

        # titulo
        surf_titulo = self.fonte.render(nome,False,cor)
        rect_titulo = surf_titulo.get_rect(midtop = self.rect.midtop + pygame.math.Vector2(0,20))
        # custo
        surf_custo = self.fonte.render(f"{int(custo)}", False, cor)
        rect_custo = surf_custo.get_rect(midbottom=self.rect.midbottom - pygame.math.Vector2(0, 20))
        # desenhar na tela
        superficie.blit(surf_titulo, rect_titulo)
        superficie.blit(surf_custo, rect_custo)

    def barra(self,superficie,valor,valor_max,selecionado):

        topo = self.rect.midtop + pygame.math.Vector2(0,60)
        baixo = self.rect.midbottom - pygame.math.Vector2(0,60)
        cor = cor_barra_selecionado if selecionado else cor_barra

        altura_total = baixo[1] - topo[1]
        valor_relativo = (valor/valor_max) * altura_total
        rect_valor = pygame.Rect(baixo[0]-15,baixo[1]-valor_relativo,30,10)

        pygame.draw.line(superficie,cor,topo,baixo,5)
        pygame.draw.rect(superficie,cor,rect_valor)
        valor_atual = self.fonte.render(f"{int(valor)}",False,cor)
        rect_atual = pygame.Rect(baixo[0] - 48, baixo[1] - valor_relativo-7, 30, 10)
        superficie.blit(valor_atual,rect_atual)

    def upar(self,personagem):
        atributo_upado = list(personagem.stats.keys())[self.indice]
        if personagem.xp >= personagem.custo_up[atributo_upado] and personagem.stats[atributo_upado] < personagem.max_stats[atributo_upado]:
            personagem.xp -= personagem.custo_up[atributo_upado]
            personagem.stats[atributo_upado] *= 1.2
            personagem.custo_up[atributo_upado] *= 1.4
            personagem.nivel *= 1.4

        if personagem.stats[atributo_upado] > personagem.max_stats[atributo_upado]:
            personagem.stats[atributo_upado] = personagem.max_stats[atributo_upado]


    def tela(self,superficie,num_selecao,nome,valor,valor_max,custo):
        if self.indice == num_selecao:
            pygame.draw.rect(superficie, cor_fundo_upgrade, self.rect)
            pygame.draw.rect(superficie, cor_borda_inter, self.rect, 4)
        else:
            pygame.draw.rect(superficie,cor_fundo_inter,self.rect)
            pygame.draw.rect(superficie,cor_borda_inter,self.rect,4)

        self.nomes(superficie,nome,custo,self.indice == num_selecao)
        self.barra(superficie,valor,valor_max,self.indice == num_selecao)