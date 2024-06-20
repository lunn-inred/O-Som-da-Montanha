import pygame
from suporte import importar_pastas
from random import choice

class AnimacaoPersonagem:
    def __init__(self):
        self.frames = {
            # magic
            'flame': importar_pastas('./graficos/particles/flame/frames'),
            'aura': importar_pastas('./graficos/particles/aura'),
            'heal': importar_pastas('./graficos/particles/heal/frames'),

            # attacks
            'claw': importar_pastas('./graficos/particles/claw'),
            'slash': importar_pastas('./graficos/particles/slash'),
            'sparkle': importar_pastas('./graficos/particles/sparkle'),
            'leaf_attack': importar_pastas('./graficos/particles/leaf_attack'),
            'thunder': importar_pastas('./graficos/particles/thunder'),

            # monster deaths
            'squid': importar_pastas('./graficos/particles/smoke_orange'),
            'raccoon': importar_pastas('./graficos/particles/raccoon'),
            'spirit': importar_pastas('./graficos/particles/nova'),
            'bamboo': importar_pastas('./graficos/particles/bamboo'),

            # leafs
            'leaf': (
                importar_pastas('./graficos/particles/leaf1'),
                importar_pastas('./graficos/particles/leaf2'),
                importar_pastas('./graficos/particles/leaf3'),
                importar_pastas('./graficos/particles/leaf4'),
                importar_pastas('./graficos/particles/leaf5'),
                importar_pastas('./graficos/particles/leaf6'),
                self.refletir(importar_pastas('./graficos/particles/leaf1')),
                self.refletir(importar_pastas('./graficos/particles/leaf2')),
                self.refletir(importar_pastas('./graficos/particles/leaf3')),
                self.refletir(importar_pastas('./graficos/particles/leaf4')),
                self.refletir(importar_pastas('./graficos/particles/leaf5')),
                self.refletir(importar_pastas('./graficos/particles/leaf6'))
            )
        }

    def refletir(self,frames):
        novos_frames = []

        for frame in frames:
            frame_espelhado = pygame.transform.flip(frame,True,False)
            novos_frames.append(frame_espelhado)
        return novos_frames

    def criar_particulas_grama(self,pos,groups):
        frames_animacao = choice(self.frames["leaf"])
        Particulas(pos,frames_animacao,groups)

    def criar_particulas(self,tipodeanimacao,pos,groups):
        frames_animacao = self.frames[tipodeanimacao]
        Particulas(pos,frames_animacao,groups)
class Particulas(pygame.sprite.Sprite):
    def __init__(self,pos,animacao,groups):
        super().__init__(groups)
        self.tipodeSprite = "magia"
        self.indice_frame = 0
        self.vel_animacao = 0.15
        self.frames = animacao
        self.image = self.frames[self.indice_frame]
        self.rect = self.image.get_rect(center = pos)
    def animar(self):
        self.indice_frame += self.vel_animacao
        if self.indice_frame >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.indice_frame)]

    def update(self):
        self.animar()
        self.image = pygame.transform.scale_by(self.image,0.5)