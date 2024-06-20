# definições do jogo
largura = 1280
altura = 720
fps = 60
tamanhosprite= 32
quantidade_inimigos = 52
velocidade_dia = 0.01

deslocamento_hitbox = {
    'personagem': -26,
    'objetos': -40,
    'grama': -10,
    'invisivel': 0}

volume = {
    "musica": 0.2,
    "efeitos":  0.2
}
volume_max = {
    "musica": 1,
    "efeitos":  1
}

# interface
altura_barra = 20
largura_barra_vida = 200
largura_barra_mana = 140
tamanho_item = 80
fonte_inter = "./graficos/font/joystix.ttf"
tamanho_fonte = 18

# cores gerais
aqua = "#71ddee"
cor_fundo_inter = '#222222'
cor_borda_inter = '#111111'
cor_texto = '#EEEEEE'

# cores da interface
vida_cor = 'red'
mana_cor = 'blue'
bordaD_ativa = 'gold'

# menu de upgrades
texto_selecionado = "#111111"
cor_barra = "#EEEEEE"
cor_barra_selecionado = "#111111"
cor_fundo_upgrade = "#EEEEEE"

# armas
dados_armas = {
    "sword": {"cooldown": 100, "damage": 15, "graphic": "./graficos/weapons/sword/full.png"},
    "lance": {"cooldown": 400, "damage": 30, "graphic": "./graficos/weapons/lance/full.png"},
    "axe": {"cooldown": 300, "damage": 25, "graphic": "./graficos/weapons/axe/full.png"},
    "rapier": {"cooldown": 50, "damage": 8, "graphic": "./graficos/weapons/rapier/full.png"},
    "sai": {"cooldown": 80, "damage": 10, "graphic": "./graficos/weapons/sai/full.png"}}
# poderes
dados_poderes = {
    'flame': {'forca': 5,'custo': 10,'graficos':'./graficos/particles/flame/fire.png'},
    'heal' : {'forca': 20,'custo': 10,'graficos':'./graficos/particles/heal/heal.png'},}

# inimigos
mob_data = {

    'raccoon': {'vida': 300,'xp':100,'forca':12,'tipo_atk': 'claw',  'attack_sound':'./audio/attack/claw.wav','vel': 2, 'resistance': 1, 'atk_range': 70, 'visao_range': 250},
    'spirit': {'vida': 50,'xp':40,'forca':2,'tipo_atk': 'thunder', 'attack_sound':'./audio/attack/fireball.wav', 'vel': 2, 'resistance': 1, 'atk_range': 100, 'visao_range': 250},
    'bamboo': {'vida': 70,'xp':60,'forca':6,'tipo_atk': 'leaf_attack', 'attack_sound':'./audio/attack/slash.wav', 'vel': 2, 'resistance':1 , 'atk_range': 50, 'visao_range': 250}}
