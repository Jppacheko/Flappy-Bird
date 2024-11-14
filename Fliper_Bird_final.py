import pygame
import os
import random
import sys

pygame.init()
pygame.display.set_caption("Flappy Bird")

TELA_LARGURA = 900
TELA_ALTURA = 800
GRAVIDADE = 0.15
VELOCIDADE_JOGO_INICIAL = 10
FORCA_PULO = -2
MAX_VELOCIDADE_QUEDA = 9

IMAGEM_CANO = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'pipe.png')))
IMAGEM_CHAO = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'base.png')))
IMAGEM_BACKGROUND = pygame.transform.scale(
    pygame.image.load(os.path.join('imgs', 'bg.png')), 
    (TELA_LARGURA, TELA_ALTURA)
)
IMAGEM_LOGIN = pygame.transform.scale(
    pygame.image.load(os.path.join('imgs', 'login.png')),
    (TELA_LARGURA, TELA_ALTURA)
)
IMAGENS_PASSARO = [
    pygame.transform.scale(pygame.image.load(os.path.join('imgs', 'bird1.png')), (34, 24)),
    pygame.transform.scale(pygame.image.load(os.path.join('imgs', 'bird2.png')), (34, 24)),
    pygame.transform.scale(pygame.image.load(os.path.join('imgs', 'bird3.png')), (34, 24))
]

FONTE_PONTOS = pygame.font.SysFont('arial', 50)
FONTE_LOGIN = pygame.font.SysFont('arial', 32)

def calcular_velocidade(pontos):
    return VELOCIDADE_JOGO_INICIAL + (pontos // 2)

class Passaro:
    IMGS = IMAGENS_PASSARO
    ROTACAO_MAXIMA = 25
    VELOCIDADE_ROTACAO = 20
    TEMPO_ANIMACAO = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angulo = 0
        self.velocidade = 0
        self.altura = self.y
        self.tempo = 0
        self.contagem_imagem = 0
        self.imagem = self.IMGS[0]

    def pular(self):
        self.velocidade = FORCA_PULO
        self.tempo = 0

    def mover(self):
        self.tempo += 1
        deslocamento = GRAVIDADE * (self.tempo**2) + self.velocidade * self.tempo

        if deslocamento > MAX_VELOCIDADE_QUEDA:
            deslocamento = MAX_VELOCIDADE_QUEDA
        elif deslocamento < 0:
            deslocamento -= 2

        self.y += deslocamento

        if deslocamento < 0 or self.y < (self.altura + 50):
            if self.angulo < self.ROTACAO_MAXIMA:
                self.angulo = self.ROTACAO_MAXIMA
        else:
            if self.angulo > -90:
                self.angulo -= self.VELOCIDADE_ROTACAO

    def desenhar(self, tela):
        self.contagem_imagem += 1

        if self.contagem_imagem < self.TEMPO_ANIMACAO:
            self.imagem = self.IMGS[0]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*2:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*3:
            self.imagem = self.IMGS[2]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*4:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem >= self.TEMPO_ANIMACAO*4 + 1:
            self.imagem = self.IMGS[0]
            self.contagem_imagem = 0

        if self.angulo <= -80:
            self.imagem = self.IMGS[1]
            self.contagem_imagem = self.TEMPO_ANIMACAO*2

        imagem_rotacionada = pygame.transform.rotate(self.imagem, self.angulo)
        pos_centro_imagem = self.imagem.get_rect(topleft=(self.x, self.y)).center
        retangulo = imagem_rotacionada.get_rect(center=pos_centro_imagem)
        tela.blit(imagem_rotacionada, retangulo.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.imagem)

class Cano:
    DISTANCIA = 200
    ESPACO_HORIZONTAL = 500

    def __init__(self, x):
        self.x = x
        self.altura = 0
        self.pos_topo = 0
        self.pos_base = 0
        self.CANO_TOPO = pygame.transform.flip(IMAGEM_CANO, False, True)
        self.CANO_BASE = IMAGEM_CANO
        self.passou = False
        self.definir_altura()

    def definir_altura(self):
        self.altura = random.randrange(50, 450)
        self.pos_topo = self.altura - self.CANO_TOPO.get_height()
        self.pos_base = self.altura + self.DISTANCIA

    def mover(self, velocidade):
        self.x -= velocidade

    def desenhar(self, tela):
        tela.blit(self.CANO_TOPO, (self.x, self.pos_topo))
        tela.blit(self.CANO_BASE, (self.x, self.pos_base))

    def colidir(self, passaro):
        passaro_mask = passaro.get_mask()
        topo_mask = pygame.mask.from_surface(self.CANO_TOPO)
        base_mask = pygame.mask.from_surface(self.CANO_BASE)

        distancia_topo = (self.x - passaro.x, self.pos_topo - round(passaro.y))
        distancia_base = (self.x - passaro.x, self.pos_base - round(passaro.y))

        topo_ponto = passaro_mask.overlap(topo_mask, distancia_topo)
        base_ponto = passaro_mask.overlap(base_mask, distancia_base)

        if base_ponto or topo_ponto:
            return True
        else:
            return False

class Chao:
    LARGURA = IMAGEM_CHAO.get_width()
    IMAGEM = IMAGEM_CHAO

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.LARGURA

    def mover(self, velocidade):
        self.x1 -= velocidade
        self.x2 -= velocidade

        if self.x1 + self.LARGURA < 0:
            self.x1 = self.x2 + self.LARGURA
        if self.x2 + self.LARGURA < 0:
            self.x2 = self.x1 + self.LARGURA

    def desenhar(self, tela):
        tela.blit(self.IMAGEM, (self.x1, self.y))
        tela.blit(self.IMAGEM, (self.x2, self.y))

def desenhar_tela(tela, passaros, canos, chao, pontos):
    tela.blit(IMAGEM_BACKGROUND, (0, 0))
    for passaro in passaros:
        passaro.desenhar(tela)
    for cano in canos:
        cano.desenhar(tela)

    texto = FONTE_PONTOS.render(f"Pontuação: {pontos}", 1, (255, 255, 255))
    tela.blit(texto, (TELA_LARGURA - 10 - texto.get_width(), 10))
    chao.desenhar(tela)
    pygame.display.update()

def tela_login(tela):
    input_box = pygame.Rect(TELA_LARGURA // 2 - 100, TELA_ALTURA // 2 + 180, 200, 40)  # Mais para baixo
    button_box = pygame.Rect(TELA_LARGURA // 2 - 60, TELA_ALTURA // 2 + 240, 120, 40)  # Mais para baixo
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                elif button_box.collidepoint(event.pos) and text.strip():
                    return text
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN and text.strip():
                        return text
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        if len(text) < 15:
                            text += event.unicode

        tela.blit(IMAGEM_LOGIN, (0, 0))

        # Padronizando o texto "Enter username" com o botão "Enter"
        label_text = "Enter username:"
        label_text_shadow = FONTE_LOGIN.render(label_text, True, (0, 0, 0))
        label_text_surface = FONTE_LOGIN.render(label_text, True, (255, 255, 255))
        label_text_rect = label_text_surface.get_rect(center=(TELA_LARGURA // 2, TELA_ALTURA // 2 + 150))  # Mais para baixo
        tela.blit(label_text_shadow, (label_text_rect.x + 2, label_text_rect.y + 2))
        tela.blit(label_text_surface, label_text_rect)

        pygame.draw.rect(tela, color, input_box, 2)
        txt_surface_shadow = FONTE_LOGIN.render(text, True, (0, 0, 0))
        txt_surface = FONTE_LOGIN.render(text, True, (255, 255, 255))
        text_rect = txt_surface.get_rect(center=input_box.center)
        tela.blit(txt_surface_shadow, (text_rect.x + 2, text_rect.y + 2))
        tela.blit(txt_surface, text_rect)

        # Desenhando o texto "Enter" sem o fundo azul
        button_text_shadow = FONTE_LOGIN.render("Enter", True, (0, 0, 0))
        button_text = FONTE_LOGIN.render("Enter", True, (255, 255, 255))
        button_text_rect = button_text.get_rect(center=button_box.center)
        tela.blit(button_text_shadow, (button_text_rect.x + 2, button_text_rect.y + 2))
        tela.blit(button_text, button_text_rect)

        pygame.display.flip()
        clock.tick(30)


def main():
    tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
    username = tela_login(tela)

    while True:
        passaros = [Passaro(230, 350)]
        chao = Chao(730)
        canos = [Cano(TELA_LARGURA)]
        pontos = 0
        relogio = pygame.time.Clock()

        rodando = True
        game_over = False
        while rodando:
            relogio.tick(30)

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_SPACE and not game_over:
                        for passaro in passaros:
                            passaro.pular()
                    if evento.key == pygame.K_r and game_over:
                        game_over = False
                        passaros = [Passaro(230, 350)]
                        canos = [Cano(TELA_LARGURA)]
                        pontos = 0
                    if evento.key == pygame.K_t and game_over:
                        return  # Retorna para a tela de login

            velocidade_atual = calcular_velocidade(pontos)

            if not game_over:
                for passaro in passaros:
                    passaro.mover()
                chao.mover(velocidade_atual)

                adicionar_cano = False
                remover_canos = []
                for cano in canos:
                    for i, passaro in enumerate(passaros):
                        if cano.colidir(passaro):
                            game_over = True
                        if not cano.passou and passaro.x > cano.x:
                            cano.passou = True
                            adicionar_cano = True
                    cano.mover(velocidade_atual)
                    if cano.x + cano.CANO_TOPO.get_width() < 0:
                        remover_canos.append(cano)

                if adicionar_cano:
                    pontos += 1
                    canos.append(Cano(TELA_LARGURA))

                for cano in remover_canos:
                    canos.remove(cano)

                for i, passaro in enumerate(passaros):
                    if (passaro.y + passaro.imagem.get_height()) > chao.y or passaro.y < 0:
                        game_over = True

            desenhar_tela(tela, passaros, canos, chao, pontos)

            if game_over:
                overlay = pygame.Surface((TELA_LARGURA, TELA_ALTURA))
                overlay.fill((0, 0, 0))
                overlay.set_alpha(128)
                tela.blit(overlay, (0, 0))

                fonte_game_over = pygame.font.SysFont('arial', 70)
                texto_game_over = fonte_game_over.render("GAME OVER", 1, (255, 0, 0))
                tela.blit(texto_game_over, (TELA_LARGURA/2 - texto_game_over.get_width()/2, TELA_ALTURA/2 - texto_game_over.get_height()/2))

                fonte_reiniciar = pygame.font.SysFont('arial', 30)
                texto_reiniciar = fonte_reiniciar.render("Pressione R para reiniciar", 1, (255, 255, 255))
                tela.blit(texto_reiniciar, (TELA_LARGURA/2 - texto_reiniciar.get_width()/2, TELA_ALTURA/2 + 50))

                fonte_trocar_jogador = pygame.font.SysFont('arial', 30)
                texto_trocar_jogador = fonte_trocar_jogador.render("Pressione T para trocar de jogador", 1, (255, 255, 255))
                tela.blit(texto_trocar_jogador, (TELA_LARGURA/2 - texto_trocar_jogador.get_width()/2, TELA_ALTURA/2 + 100))

                fonte_username = pygame.font.SysFont('arial', 30)
                texto_username = fonte_username.render(f"Jogador: {username}", 1, (255, 255, 255))
                tela.blit(texto_username, (TELA_LARGURA/2 - texto_username.get_width()/2, TELA_ALTURA/2 + 150))

                pygame.display.update()

if __name__ == "__main__":
    while True:
        main()