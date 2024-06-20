import pygame

import config
from config import *
from random import randint

class Magia:
    def __init__(self,animacao_personagem):
        self.animacao_personagem = animacao_personagem
        self.audios = {
        "curar": pygame.mixer.Sound("./audio/heal.wav"),
        "flame": pygame.mixer.Sound("./audio/Fire.wav")
        }
        self.audios["curar"].set_volume(config.volume["efeitos"])
        self.audios["flame"].set_volume(config.volume["efeitos"])

    def curar(self,personagem,forca,custo,groups):
        self.audios["curar"].set_volume(config.volume["efeitos"])

        if personagem.mana >= custo:
            self.audios["curar"].play()
            personagem.vida += forca
            personagem.mana -= custo
            if personagem.vida >= personagem.stats["vida"]:
                personagem.vida = personagem.stats["vida"]
            self.animacao_personagem.criar_particulas("aura",personagem.rect.center,groups)
            self.animacao_personagem.criar_particulas("heal", personagem.rect.center + pygame.math.Vector2(0,-50), groups)

    def flame(self,personagem,custo,groups):

        self.audios["flame"].set_volume(config.volume["efeitos"])
        if personagem.mana >= custo:
            personagem.mana -= custo
            self.audios["flame"].play()

            if personagem.status.split("_")[0] == "right":
                direcao = pygame.math.Vector2(1,0)
            else:
                direcao = pygame.math.Vector2(-1,0)

            for i in range(1,6):
                deslocamento = (direcao.x * i) * tamanhosprite
                x = personagem.rect.centerx + deslocamento + randint(-tamanhosprite//3,tamanhosprite//3)
                y = personagem.rect.centery + randint(-tamanhosprite//3,tamanhosprite//3)
                self.animacao_personagem.criar_particulas("flame",(x,y),groups)