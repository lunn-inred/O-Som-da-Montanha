import pygame,sys
from config import *
from suporte import *
from entidades import Entidades
import config
class Personagem(Entidades):
	def __init__(self,pos,groups,obstaculos,del_atk,faze_poder):
		super().__init__(groups)
		self.image = pygame.image.load('./graficos/teste/player.png').convert_alpha()
		self.imagem = pygame.transform.scale_by(self.image, 1.9)
		self.pos = pos

		self.rect = self.imagem.get_rect(topleft = self.pos)
		self.hitbox = self.rect.inflate(-6,deslocamento_hitbox["personagem"])

		# condições para o jogo
		self.pausa = False
		self.upando = False
		self.jogando = False
		self.opcoes = False
		self.rodando = True
		self.morreu = False
		self.ganhou = False

		# definição dos graficos
		self.importar_assets()
		self.status = "right_idle"

		# definição da movimentação
		self.atacando = False
		self.cooldown = 400
		self.tempoD_atk = None
		self.obstaculos = obstaculos
		self.cura = False
		self.fogo = False


		# poderes
		self.faze_poder = faze_poder
		self.indice_poder = 0
		self.poder = list(dados_poderes.keys())[self.indice_poder]
		self.mudando_poder = False
		self.tempoD_mudaPoder = None
		self.num_poderes = 1
		# stats do personagem
		self.stats = {"vida": 40, "mana": 30,"poder":8,"vel":5}
		self.max_stats = {"vida": 100, "mana": 70,"poder":20,"vel":8}
		self.custo_up = {"vida": 100, "mana": 100,"poder":100,"vel":100}
		self.vida = self.stats["vida"]
		self.mana = self.stats["mana"]
		self.xp = 0
		self.nivel = 100
		self.vel = self.stats["vel"]

		# timer pro dano
		self.vulneravel = True
		self.foi_hitado = None
		self.duracao = 500

		# importar audio
		self.som_atk = pygame.mixer.Sound("./audio/sword.wav")
		self.som_atk.set_volume(config.volume["efeitos"])

	def importar_assets(self):
		personagem_path = "./graficos/player/"
		self.animacoes = dict(left=[], right=[], right_idle=[], left_idle=[], right_attack=[], left_attack=[], right_charging=[], left_charging=[], left_death=[], right_death=[])
		for animacao in self.animacoes.keys():
			full_path = personagem_path + animacao
			self.animacoes[animacao] = importar_pastas(full_path)


	def entradas(self):
		# pega as entradas de mouse e teclado e passa pro codigo
		teclas = pygame.key.get_pressed()



		# entradas para se mover
		if not self.atacando:
				# recuperar a mana
			if teclas[pygame.K_r]:
				self.recuperar_mana()
				self.recarregando = True
				# Função sprint/correr
			if teclas[pygame.K_LSHIFT]:
				self.vel = 11
				self.vel_animacao = 0.2
			else:
				self.vel = 5
				self.vel_animacao = 0.15
				# movimento no eixo y/cima e baixo
			if teclas[pygame.K_w] or teclas[pygame.K_UP]:
				self.direcao.y = -1
			elif teclas[pygame.K_s] or teclas[pygame.K_DOWN]:
				self.direcao.y = 1
			else:
				self.direcao.y = 0
			# movimento no eixo x/ esquerda e direita
			if teclas[pygame.K_a] or teclas[pygame.K_LEFT]:
				self.direcao.x = -1
			elif teclas[pygame.K_d] or teclas[pygame.K_RIGHT]:
				self.direcao.x = 1
			else:
				self.direcao.x = 0

			# entradas para o ataque
			# botao do mouse
			lmb = pygame.mouse.get_pressed()[0]
			if lmb:
				self.atacando = True
				self.fogo = True
				self.tempoD_atk = pygame.time.get_ticks()
				modelo = "flame"
				forca = list(dados_poderes.values())[0]["forca"] + self.stats["poder"]
				custo = list(dados_poderes.values())[0]["custo"]
				self.faze_poder(modelo,forca,custo)
				self.som_atk.play()

			# entradas para a habilidade do personagem
			if teclas[pygame.K_q]:
				self.atacando = True
				self.cura = True
				self.tempoD_atk = pygame.time.get_ticks()
				modelo = "heal"
				forca = list(dados_poderes.values())[1]["forca"] + self.stats["poder"]
				custo = list(dados_poderes.values())[1]["custo"]
				self.faze_poder(modelo,forca,custo)

				self.poder = list(dados_poderes.keys())[self.indice_poder]
				# entradas para a troca de armas
		for evento in pygame.event.get():
			mousex = pygame.mouse.get_pos()[0]

			if evento.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

			if evento.type == pygame.KEYDOWN:
				# if evento.key == pygame.K_e:
				# 	self.menu()
				if evento.key == pygame.K_F11:
					pygame.display.toggle_fullscreen()
				if evento.key == pygame.K_ESCAPE:
					self.pausa = True


			if evento.type == pygame.MOUSEMOTION:
				if mousex <= largura/2:
					self.status = "left_idle"
				if mousex > largura/2:
					self.status = "right_idle"

	def define_status(self):
		# parado
		if self.direcao.x == 0 and self.direcao.y == 0:
			if not "idle" in self.status and not "attack" in self.status and "charging" in self.status:
				self.status = self.status + "_idle"

		if self.atacando:
			self.direcao.x = 0
			self.direcao.y = 0
			if not "attack" in self.status:
				if "idle" in self.status:
					self.status = self.status.replace("_idle", "_attack")

				else:
					self.status = self.status + "_attack"

		else:
			if "attack" in self.status:
				self.status = self.status.replace("_attack", "_idle")
		if self.stats["vida"] == 0:
			self.direcao.x = 0
			self.direcao.y = 0
			if "_idle" in self.status:
				self.status = self.status.replace("_idle", "_death")
			if "_attack" in self.status:
				self.status = self.status.replace("_attack", "_death")
			if "_charging" in self.status:
				self.status = self.status.replace("_charging", "_death")

	def cooldowns(self):
		# temporizadores
		momento_atual = pygame.time.get_ticks()
		if self.atacando:
			if momento_atual - self.tempoD_atk >= self.cooldown:
				self.atacando = False

		if self.cura:
			if momento_atual - self.tempoD_atk >= self.cooldown:
				self.cura = False
		if self.fogo:
			if momento_atual - self.tempoD_atk >= self.cooldown:
				self.fogo = False
		if not self.vulneravel:
			if momento_atual - self.foi_hitado >= self.duracao:
				self.vulneravel = True

	def animar(self):
		animacao = self.animacoes[self.status]

		# faz a animação de movimento
		self.indice_frame += self.vel_animacao
		if self.indice_frame >= len(animacao):
			self.indice_frame = 0
		# definir as imagems da animacao
		self.image = animacao[int(self.indice_frame)]
		self.rect = self.image.get_rect(center = self.hitbox.center)

		if not self.vulneravel:
			alpha = self.valor_flutuante()
			self.image.set_alpha(alpha)
		else:
			self.image.set_alpha(255)



	def dano_magico(self):
		dano_base = self.stats["poder"]
		dano_magia = dados_poderes[self.poder]["forca"]
		return dano_base + dano_magia

	def pausar(self):
		self.pausa = not self.pausa

	def menu(self):
		teclas = pygame.key.get_pressed()
		if self.xp >= self.nivel:
			self.upando = True

		if teclas[pygame.K_ESCAPE]:
			self.upando = False

	def pegarValor_indice(self,indice):
		return list(self.stats.values())[indice]

	def pegarCusto_indice(self,indice):
		return list(self.custo_up.values())[indice]

	def recuperar_mana(self):
		if self.mana < self.stats["mana"]:
			self.mana += 0.2
		else:
			self.mana = self.stats["mana"]



	def update(self):
		# autualiza as ações e modificações do jogo no tickrate determinado
		self.entradas()
		self.menu()
		self.cooldowns()
		self.define_status()
		self.animar()
		self.movimento(self.stats["vel"])

		self.image = pygame.transform.scale_by(self.image, 1.2)


		self.som_atk.set_volume(config.volume["efeitos"])

