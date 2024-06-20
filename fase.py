import pygame

import config
from config import *
from tileset import Tileset
from personagem import Personagem
from suporte import *
from random import *
from interface import Interface
from inimigos import Inimigo
from particulas import AnimacaoPersonagem
from feiticos import Magia
from upgrades import Upgrade
from menu import Menu
from menu_inicial import main_menu
class Fase:
    def __init__(self):

        self.jogando = False
        self.pausa = False
        self.ganhou = False
        # identificar a superficie da tela
        self.superficieTela = pygame.display.get_surface()

        # definir os grupos de sprite
        self.sprites_visiveis = CameraGrupo()
        self.obstaculos = pygame.sprite.Group()

        # sprite dos ataques
        self.atk_atual = None
        self.atk_sprites = pygame.sprite.Group()
        self.sprites_atacaveis = pygame.sprite.Group()
        # configuração dos sprite
        self.fazeMapa()
        # interface do usuario
        self.interface = Interface()
        self.upgrade = Upgrade(self.personagem)
        self.menu = Menu(self.personagem)
        self.main_menu = main_menu(self.personagem)
        self.opcoes = False
        self.creditos = False
        self.controles = False
        # particulas
        self.animacao_personagem = AnimacaoPersonagem()
        self.magia = Magia(self.animacao_personagem)

    def fazeMapa(self):
        # configuração dos sprites do mapa e das coisas que nele aparecem
        layouts = {
            "limitedomapa": importar_layout("./mapa/borda.csv"),
            "grama":importar_layout("./mapa/grama.csv"),
            "objetos":importar_layout("./mapa/objetos.csv"),
            "entidades": importar_layout("./mapa/entidades.csv")
        }
        # definição dos graficos das coisas que possam ser colididadas no mapa e sao cenario
        graficos = {
            "grama": importar_pastas("./graficos/Grass"),
            "objetos": importar_pastas("./graficos/objects")
        }
        # desenhando na tela os graficos, o mapa e o personagem
        for estilo,layout in layouts.items():
            for linha_index, lin in enumerate(layout):
                for col_index, col in enumerate(lin):
                    if col != "-1":
                        x = col_index * tamanhosprite
                        y = linha_index * tamanhosprite
                        if estilo == "limitedomapa": # bordas do mapa onde nao da pro personagem passar
                            Tileset((x,y),[self.obstaculos],"invisivel")
                        if estilo == "grama": # florzinhas que se destacam do fundo e sao obstaculos
                            escolheGrama = choice(graficos["grama"])
                            Tileset((x,y),[self.sprites_visiveis,self.obstaculos,self.sprites_atacaveis], "grama", escolheGrama)
                        if estilo == "objetos": # coisas como colunas, arvores, estatuas
                            superf = graficos["objetos"][int(col)]
                            Tileset((x,y),[self.sprites_visiveis,self.obstaculos],"objetos",superf)
                        if estilo == "entidades":

                            if col == "1":
                                self.personagem = Personagem((x, y), [self.sprites_visiveis], self.obstaculos,
                                                            self.del_atk, self.fazePoder)
                            else:
                                if col == "17": mob_nome = "bamboo"
                                elif col == "104": mob_nome = "spirit"

                                else: mob_nome = "raccoon"
                                self.inimigo = Inimigo(mob_nome,(x,y),[self.sprites_visiveis,self.sprites_atacaveis],self.obstaculos,self.personagem_levoudano,self.animacao_morte,self.xp)



    def fazePoder(self,tipo,forca,custo):
        if tipo == "heal":
            self.magia.curar(self.personagem,forca,custo,[self.sprites_visiveis])

        if tipo == "flame":
            self.magia.flame(self.personagem,custo,[self.sprites_visiveis,self.atk_sprites])

    def del_atk(self):
        if self.atk_atual:
            self.atk_atual.kill()
        self.atk_atual = None

    def logica_atk(self):
        if self.atk_sprites:
            for atk_sprites in self.atk_sprites:
                colisoes = pygame.sprite.spritecollide(atk_sprites,self.sprites_atacaveis,False)
                if colisoes:
                    for alvo in colisoes:
                        if alvo.tipodeSprite == "grama":
                            pos = alvo.rect.center
                            deslocamento = pygame.math.Vector2(0,80)
                            for folhas in range(randint(3,6)):
                                self.animacao_personagem.criar_particulas_grama(pos - deslocamento,[self.sprites_visiveis])
                            alvo.kill()
                        else:
                            alvo.levou_dano(self.personagem,atk_sprites.tipodeSprite)

    def personagem_levoudano(self, quantidade, tipodeatk):
        if self.personagem.vulneravel:
            self.personagem.vida -= quantidade
            self.personagem.vulneravel = False
            self.personagem.foi_hitado = pygame.time.get_ticks()
            self.animacao_personagem.criar_particulas(tipodeatk,self.personagem.rect.center,[self.sprites_visiveis])
        if self.personagem.vida <= 0:
            self.personagem.vida = 0
            self.personagem.morreu = True

    def animacao_morte(self,pos,tipodeparticula):
        self.animacao_personagem.criar_particulas(tipodeparticula,pos,self.sprites_visiveis)


    def xp(self,quantidade):
        self.personagem.xp += quantidade

    def ganhar(self):
        if config.quantidade_inimigos == 0:
            self.personagem.ganhou = True
    def rodar(self):

        # atualizações e mostrar as coisas do cenario e o personagem na tela
        self.ganhar()
        if self.personagem.jogando:




            self.personagem.menu()
            self.sprites_visiveis.desenhos(self.personagem)
            self.interface.tela(self.personagem)
            if self.personagem.upando:
                self.upgrade.tela()
            elif self.personagem.pausa:
                self.menu.tela()
            elif self.personagem.morreu:
                self.menu.tela()
            elif self.personagem.ganhou:
                self.menu.tela()

            else:
                self.personagem.entradas()
                self.sprites_visiveis.update()
                self.sprites_visiveis.update_inimigo(self.personagem)
                self.logica_atk()









class CameraGrupo(pygame.sprite.Group):
    # a camera do jogo pra fazer com que as coisas sejam desenhadas conforme sua posição no eixo y
    def __init__(self):
        # configuração geral
        super().__init__()
        self.superficieTela = pygame.display.get_surface()
        self.larguramedia = self.superficieTela.get_size()[0] // 2
        self.alturamedia = self.superficieTela.get_size()[1] // 2
        self.deslocamentoCamera = pygame.math.Vector2()
        # desenho do cenario
        self.superficieFundo = pygame.image.load("./graficos/tilemap/ground.png")

        self.fundo_rect = self.superficieFundo.get_rect(topleft = (0,0))
    def desenhos(self, personagem):
        # pegar o deslocamento necessário da camera
        self.deslocamentoCamera.x = personagem.rect.centerx - self.larguramedia
        self.deslocamentoCamera.y = personagem.rect.centery - self.alturamedia
        # alocar o cenário nas coordenadas certas
        deslocamentoFundo = self.fundo_rect.topleft - self.deslocamentoCamera
        self.superficieTela.blit(self.superficieFundo,deslocamentoFundo)

        # for sprite in self.sprites():
        # desenha os objetos baseado na cordenada y, deixa o jogo mais bonito
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            deslocamento_pos = sprite.rect.topleft - self.deslocamentoCamera
            self.superficieTela.blit(sprite.image, deslocamento_pos)

    def update_inimigo(self,personagem):
        sprites_inimigos = [sprite for sprite in self.sprites()if hasattr(sprite,"tipodeSprite") and sprite.tipodeSprite == "inimigo"]
        for inimigo in sprites_inimigos:
            inimigo.update_inimigo(personagem)
