import sys
import pygame
import config
from config import *
from suporte import *

class Menu:
    def __init__(self,personagem):
        # definicoes gerais
        self.superficie_tela = pygame.display.get_surface()
        self.image = pygame.image.load('./graficos/teste/player.png').convert_alpha()
        self.deslocamentoCamera = pygame.math.Vector2()
        self.personagem = personagem
        self.ganhou = False
        self.numero_atributos = 3
        self.numero_opcoes = 2
        self.nome_atibutos = ["Continuar","Opções","Sair do Jogo"]
        self.nome_opcoes = ["Músicas", "Efeitos"]
        self.valor_max = list(config.volume_max.values())
        self.fonte = pygame.font.Font(fonte_inter,tamanho_fonte)
        self.indice_frame = 0
        self.vel_animacao = 0.07
        self.rect = self.superficie_tela.get_rect()
        self.animacoes = dict(left=[], right=[], right_idle=[], left_idle=[], right_attack=[], left_attack=[],
                              right_charging=[], left_charging=[], left_death=[], right_death=[])
        self.fundinho = pygame.Surface((1280,720))
        self.fundinho.set_alpha(127)
        self.fundinho.fill("black")
        self.yipee = pygame.mixer.Sound("./audio/yipeee.ogg")
        self.yipee.set_volume(config.volume["efeitos"])


        # dimenções dos itens
        self.altura = self.superficie_tela.get_size()[1]//10
        self.largura = self.superficie_tela.get_size()[0]*0.6 -500
        self.largura_op = self.superficie_tela.get_size()[0] * 0.6
        self.altura_op = self.superficie_tela.get_size()[1] // 10 + 15
        self.criar()

        # sistema de selecao
        self.indice_select_op = 0
        self.indice_select = 0
        self.tempo_select = None
        self.pode_mexer = True

    def entradas(self):
        teclas = pygame.key.get_pressed()
        lmb = pygame.mouse.get_pressed()[0]
        if self.pode_mexer:
            if not self.personagem.opcoes:
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
                    self.lista[self.indice_select].acao(self.personagem, self.nome_atibutos[self.indice_select])
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
                    self.lista_op[self.indice_select_op].acao(self.personagem, self.nome_opcoes[self.indice_select_op])
                if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
                    self.lista_op[self.indice_select_op].acao(self.personagem,self.nome_opcoes[self.indice_select_op] + "1")
        for evento in pygame.event.get():
            mousex, mousey = pygame.mouse.get_pos()

            if evento.type == pygame.MOUSEMOTION:
                if mousex >= 521 and mousex <= 786:
                    if mousey >= 165 and mousey <= 232:
                        self.indice_select = 0
                    if mousey >= 285 and mousey <= 355:
                        self.indice_select = 1
                    if mousey >= 404 and mousey <= 473:
                        self.indice_select = 2

    def pegarValor_indice(self, indice):
        return list(config.volume.values())[indice]

    def importar_assets(self):
        personagem_path = "./graficos/player/"
        self.animacoes = dict(left=[], right=[], right_idle=[], left_idle=[], right_attack=[], left_attack=[],
                              right_charging=[], left_charging=[], left_death=[], right_death=[])
        for animacao in self.animacoes.keys():
            full_path = personagem_path + animacao
            self.animacoes[animacao] = importar_pastas(full_path)

    def cooldown(self):
        if not self.pode_mexer:
            momento_atual = pygame.time.get_ticks()
            if momento_atual - self.tempo_select >= 300:
                self.pode_mexer = True

    def animarmorte(self):
        animacao = self.animacoes["left_death"]


        # faz a animação de movimento
        self.indice_frame += self.vel_animacao
        if self.indice_frame >= len(animacao):
            self.vel_animacao = 0
            self.indice_frame = -1
        # definir as imagems da animacao
        self.image = animacao[int(self.indice_frame)]
        self.rect = self.image.get_rect(center=self.personagem.hitbox.center)
    def animar(self):
        animacao = self.animacoes["left_charging"]
        self.vel_animacao = 0.15

        # faz a animação de movimento
        self.indice_frame += self.vel_animacao
        if self.indice_frame >= len(animacao):

            self.indice_frame = 0
        # definir as imagems da animacao
        self.image = animacao[int(self.indice_frame)]
        self.rect = self.image.get_rect(center=self.personagem.hitbox.center)

    def criar(self):
        self.lista = []
        for item, indice in enumerate(range(self.numero_atributos)):
            # posicao horizontal
            altura_total = self.superficie_tela.get_size()[1]//2
            incremento = altura_total//self.numero_atributos
            # esq = self.superficie_tela.get_size()[1]*0.1
            esq = self.superficie_tela.get_size()[0]//2 - 120

            # posicao vertical
            topo = (item * incremento) + (incremento - self.altura)//2 + 140

            item = Items(esq,topo,self.largura,self.altura,indice,self.fonte)
            self.lista.append(item)
            self.lista_op = []
            for item, indice in enumerate(range(self.numero_opcoes)):
                # posicao horizontal
                altura_total = self.superficie_tela.get_size()[1] // 2 + 100
                incremento = altura_total // self.numero_atributos
                # esq = self.superficie_tela.get_size()[1]*0.1
                esq = self.superficie_tela.get_size()[0] // 2 - 380

                # posicao vertical
                topo = (item * incremento) + (incremento - self.altura_op) // 2 + 200

                item = Items(esq, topo, self.largura_op, self.altura_op, indice, self.fonte)
                self.lista_op.append(item)



    def tela(self):
        self.importar_assets()
        self.cooldown()
        self.superficie_tela.blit(self.fundinho, self.rect)
        if self.personagem.opcoes:
            self.entradas()
            teclas = pygame.key.get_pressed()
            if teclas[pygame.K_ESCAPE]:
                self.personagem.opcoes = False
            for indice, item in enumerate(self.lista_op):
                nome = self.nome_opcoes[indice]
                valor_max = self.valor_max[indice]
                valor = self.pegarValor_indice(indice)
                item.tela(self.superficie_tela, self.indice_select_op, nome)
                item.barra(self.superficie_tela, valor, valor_max, self.indice_select_op)

        elif self.personagem.morreu:

            self.animarmorte()
            self.superficie_tela.fill("black")

            self.deslocamentoCamera.y = self.personagem.rect.centery - altura//2 + 25
            self.deslocamentoCamera.x = self.personagem.rect.centerx - largura//2 + 15

            pos = self.personagem.rect.topleft - self.deslocamentoCamera

            self.image = pygame.transform.scale_by(self.image,1.9)
            self.superficie_tela.blit(self.image,pos)
            texto = self.fonte.render("Game Over", False,cor_texto)
            largura_texto = texto.get_width()
            rect = pygame.Rect(largura//2-largura_texto//2,altura//2-100,80,80)
            self.superficie_tela.blit(texto,rect)

            if self.vel_animacao == 0:
                texto = self.fonte.render("Pressione Espaço para Reiniciar", False, cor_texto)
                largura_texto = texto.get_width()
                rect = pygame.Rect(largura // 2 - largura_texto//2, altura // 2 +100, 40, 20)
                self.superficie_tela.blit(texto, rect)



        elif self.personagem.ganhou:
            self.yipee.play()

            self.superficie_tela.fill("black")
            self.animar()
            self.deslocamentoCamera.y = self.personagem.rect.centery - altura // 2 + 25
            self.deslocamentoCamera.x = self.personagem.rect.centerx - largura // 2 + 25

            pos = self.personagem.rect.topleft - self.deslocamentoCamera

            self.image = pygame.transform.scale_by(self.image, 1.9)
            self.superficie_tela.blit(self.image, pos)
            texto = self.fonte.render("Você Ganhou!!", False, cor_texto)
            largura_texto = texto.get_width()
            rect = pygame.Rect(largura // 2 - largura_texto//2, altura // 2 - 100, 80, 80)
            self.superficie_tela.blit(texto, rect)


            texto1 = self.fonte.render("Pressione Espaço para Reiniciar", False, cor_texto)
            largura_texto1 = texto1.get_width()
            rect1 = pygame.Rect(largura // 2 - largura_texto1//2, altura // 2 + 100, 40, 20)
            self.superficie_tela.blit(texto1, rect1)


        else:

            self.entradas()
            for indice, item in enumerate(self.lista):
                nome = self.nome_atibutos[indice]
                item.tela(self.superficie_tela, self.indice_select, nome)


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



    def acao(self,personagem,nome):
        if nome == "Continuar":
            personagem.pausa = False
        if nome == "Sair do Jogo":
            pygame.quit()
            sys.exit()
        if nome == "Opções":
            personagem.opcoes = True
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
