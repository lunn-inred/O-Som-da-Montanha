import pygame
from config import *
from entidades import Entidades
from suporte import *
from menu_inicial import *
import config
class Inimigo(Entidades):
    def __init__(self,nome_mob,pos,groups,obstaculos,personagem_levoudano,animacao_morte,xp):
        super().__init__(groups)
        self.tipodeSprite = "inimigo"

        # sprites dos inimigos
        self.importar_sprites(nome_mob)
        self.status = "idle"
        self.image = self.animacao[self.status][self.indice_frame]
        self.qntd_inimigos = 0
        # movimentação
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0,-10)
        self.obstaculos = obstaculos

        # stats
        self.nome_mob = nome_mob
        mob_info = mob_data[self.nome_mob]
        self.vida = mob_info["vida"]
        self.quantidade_xp = mob_info["xp"]
        self.vel = mob_info["vel"]
        self.dano = mob_info["forca"]
        self.resistencia = mob_info["resistance"]
        self.tipo_atk = mob_info["tipo_atk"]
        self.visao_range = mob_info["visao_range"]
        self.atk_range = mob_info["atk_range"]

        # interações
        self.pode_atk = True
        self.tempo_atk = None
        self.atk_cd = 400
        self.personagem_levoudano = personagem_levoudano
        self.animacao_morte = animacao_morte
        self.xp = xp

        # tempo de invulnerabilidade
        self.vulneravel = True
        self.tempo_hit = None
        self.duracao = 300

        # importar audios
        self.audio_morte = pygame.mixer.Sound("./audio/death.wav")
        self.audio_morte.set_volume(config.volume["efeitos"])
        self.audio_atk = pygame.mixer.Sound(mob_info["attack_sound"])
        self.audio_atk.set_volume(config.volume["efeitos"])
        self.audio_hit = pygame.mixer.Sound("./audio/hit.wav")
        self.audio_hit.set_volume(config.volume["efeitos"])
    def importar_sprites(self,nome):
        self.animacao = {"idle":[],"move":[],"attack":[]}
        main_path = f"./graficos/monsters/{nome}/"
        for animacao in self.animacao.keys():
            self.animacao[animacao] = importar_pastas(main_path + animacao)

    def distancia_personagem(self,personagem):
        inimigo_vet = pygame.math.Vector2(self.rect.center)
        personagem_vet = pygame.math.Vector2(personagem.rect.center)
        distancia = (personagem_vet-inimigo_vet).magnitude()
        if distancia > 0:
            direcao = (personagem_vet-inimigo_vet).normalize()
        else:
            direcao = pygame.math.Vector2()
        return (distancia,direcao)

    def define_status(self,personagem):
        distancia = self.distancia_personagem(personagem)[0]
        if distancia <= self.atk_range and self.pode_atk:
            if self.status != "attack":
                self.indice_frame = 0
            self.status = "attack"
        elif distancia <= self.visao_range:
            self.status = "move"
        else:
            self.status = "idle"

    def acoes(self,personagem):
        if self.status == "attack":
            self.tempo_atk = pygame.time.get_ticks()
            self.personagem_levoudano(self.dano,self.tipo_atk)
            self.audio_atk.play()
        elif self.status == "move":
            self.direcao = self.distancia_personagem(personagem)[1]
        else:
            self.direcao = pygame.math.Vector2()

    def cooldowns(self):
        tempo_atual = pygame.time.get_ticks()
        if not self.pode_atk:
            if tempo_atual - self.tempo_atk >= self.atk_cd:
                self.pode_atk = True
        if not self.vulneravel:
            if tempo_atual - self.tempo_hit >= self.duracao:
                self.vulneravel = True

    def animar(self):
        animacao = self.animacao[self.status]

        # faz a animação de movimento do inimigo
        self.indice_frame += self.vel_animaaco
        if self.indice_frame >= len(animacao):
            if self.status == "attack":
                self.pode_atk = False
            self.indice_frame = 0

        # colocando os sprites dos inimigos
        self.image = animacao[int(self.indice_frame)]
        self.rect = self.image.get_rect(center = self.hitbox.center)
        if not self.vulneravel:
            alpha = self.valor_flutuante()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)



    def levou_dano(self,personagem,tipodeatk):
        if self.vulneravel:
            self.direcao = self.distancia_personagem(personagem)[1]
            if tipodeatk == "arma":
                self.vida -= personagem.dano_verdadeiro()
            else:
                self.vida -= personagem.dano_magico()
            self.tempo_hit = pygame.time.get_ticks()
            self.audio_hit.play()
            self.vulneravel = False

    def morreu(self):

        if self.vida <= 0:
            config.quantidade_inimigos -= 1
            self.morte = True
            self.kill()
            self.animacao_morte(self.rect.center,self.nome_mob)
            self.xp(self.quantidade_xp)
            self.audio_morte.play()





    def reacao(self):
        if not self.vulneravel:
            self.direcao *= -self.resistencia

    def update(self):
        self.reacao()
        self.movimento(self.vel)
        self.animar()
        self.cooldowns()
        self.morreu()
        self.image = pygame.transform.scale_by(self.image,0.5)
        self.audio_morte.set_volume(config.volume["efeitos"])
        self.audio_atk.set_volume(config.volume["efeitos"])
        self.audio_hit.set_volume(config.volume["efeitos"])

    def update_inimigo(self,personagem):
        self.define_status(personagem)
        self.acoes(personagem)