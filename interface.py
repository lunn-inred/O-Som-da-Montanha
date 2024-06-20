import pygame
from config import *


class Interface:
    def __init__(self):
        # definições gerais
        self.superficieTela = pygame.display.get_surface()
        self.fonte = pygame.font.Font(fonte_inter,tamanho_fonte)

        # barras de vida e mana
        self.vida_rect = pygame.Rect(10,10,largura_barra_vida,altura_barra)
        self.mana_rect = pygame.Rect(10,34,largura_barra_mana,altura_barra)



        # converter o dicionario de poderes
        self.img_poder = []
        for poder in dados_poderes.values():
            poder = pygame.image.load(poder["graficos"]).convert_alpha()

            self.img_poder.append(poder)
    def mostrarBarra(self,atual,qtd_max,fundo_rect,cor):
        # faz o fundo das barras
        pygame.draw.rect(self.superficieTela,cor_fundo_inter,fundo_rect)

        # convertendo o valor do stat pra pixels
        razao = atual/qtd_max
        largura_atual = fundo_rect.width * razao
        rect_atual = fundo_rect.copy()
        rect_atual.width = largura_atual

        # desenhar a barra
        pygame.draw.rect(self.superficieTela,cor,rect_atual)
        pygame.draw.rect(self.superficieTela,cor_borda_inter,fundo_rect,3)


    def mostrarXP(self,xp):
        superficie_texto = self.fonte.render(str(f"exp: {int(xp)}"),False,cor_texto)

        x = self.superficieTela.get_size()[0] - 20
        y = self.superficieTela.get_size()[1] - 20
        rect_texto = superficie_texto.get_rect(bottomright = (x,y))


        pygame.draw.rect(self.superficieTela,cor_fundo_inter,rect_texto.inflate(20,20))
        self.superficieTela.blit(superficie_texto,rect_texto)
        pygame.draw.rect(self.superficieTela, cor_borda_inter, rect_texto.inflate(20, 20),3)




    def itematual(self,esquerda,topo, mudou,usando):
        fundo_rect = pygame.Rect(esquerda,topo,tamanho_item,tamanho_item)
        pygame.draw.rect(self.superficieTela,cor_fundo_inter,fundo_rect)
        if mudou:
            pygame.draw.rect(self.superficieTela, bordaD_ativa, fundo_rect, 3)
        else:
            pygame.draw.rect(self.superficieTela, cor_borda_inter, fundo_rect,3)
        if usando:
            pygame.draw.rect(self.superficieTela, bordaD_ativa, fundo_rect, 3)
        else:
            pygame.draw.rect(self.superficieTela, cor_borda_inter, fundo_rect, 3)
        return fundo_rect
    def inventario(self,esquerda,topo,mudou,usando):
        fundo_rect2 = pygame.Rect(esquerda, topo, tamanho_item * 0.9, tamanho_item *0.9)
        pygame.draw.rect(self.superficieTela, cor_fundo_inter, fundo_rect2)
        if mudou:
            pygame.draw.rect(self.superficieTela, bordaD_ativa, fundo_rect2, 3)
        else:
            pygame.draw.rect(self.superficieTela, cor_borda_inter, fundo_rect2, 3)
        if usando:
            pygame.draw.rect(self.superficieTela, bordaD_ativa, fundo_rect2, 3)
        else:
            pygame.draw.rect(self.superficieTela, cor_borda_inter, fundo_rect2, 3)

        return fundo_rect2
    def poderes1(self,indice_poderes,mudou,usando):
        fundo_rect = self.itematual(20, 630,mudou,usando)  # primario
        superficie_arma = self.img_poder[indice_poderes]
        rect_arma = superficie_arma.get_rect(center=fundo_rect.center)
        self.superficieTela.blit(superficie_arma,rect_arma)

    def poderes2(self,indice_poderes,mudou,usando):
        fundo_rect2 = self.inventario(80, 645,mudou,usando)  # secundario
        superficie_poder = self.img_poder[indice_poderes]
        rect_poder = superficie_poder.get_rect(center=fundo_rect2.center)
        self.superficieTela.blit(superficie_poder, rect_poder)
    def tela(self,personagem):
        self.mostrarBarra(personagem.vida, personagem.stats["vida"], self.vida_rect, vida_cor)
        self.mostrarBarra(personagem.mana, personagem.stats["mana"], self.mana_rect, mana_cor)
        self.mostrarXP(personagem.xp)
        self.poderes1(0,personagem.mudando_poder,personagem.fogo)
        self.poderes2(1,personagem.mudando_poder,personagem.cura)
