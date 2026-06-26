from OpenGL.GL import *
from pyglm import glm
from classes.cubo import *
from classes.modelo_obj import *
import math

class Movimento:
    def __init__(self, size, matriz):
        self.size = size
        self.tab_matrix = matriz
        
    
    # iremos calcular a posição de clique usando um tipo de ray casting.
    # no ray casting, se simulam raios saindo da câmera e indo pra cena.
    # como a cena tem projeção ortográfica, os raios são paralelos entre si;
    # logo, podemos usar esses raios para detectar a posição do clique.

    def calcular_posicao(self, x_pos, y_pos, width, height, ang):
        
        # antes de calcular a posição, iremos "encaixar" o espaço de clique.
        # isso porque a classe aqui não sabe da função window_resize,
        # e acha que o tabuleiro está esticado ou achatado ao alterar o tamanho da janela.
        # logo, vamos recriar a função window_resize aqui na classe, para corrigir esse problema.
        window_size = 800
        if width < 800:
            x = 0
            y = (height - window_size)//2
            w = width
            h = window_size
            # equivale a glViewport(0, y, width, window_size).
        elif height < 800:
            x = (width - window_size)//2
            y = 0
            w = window_size
            h = height
            # equivale a glViewport(x, 0, window_size, height).
        else:
            size = min(width, height)
            x = (width - size)//2
            y = (height - size)//2
            w = size
            h = size
            # equivale a glViewport(x, y, size, size).
        
        # se removermos as áreas ajustadas, podemos tratar os cliques
        # como se a janela estivesse no tamanho original.
        x_pos_ajust = x_pos - x
        y_pos_ajust = y_pos - y
        
        # ndc = normalized device coordinates (coordenadas de dispositivo nornalizadas)
        # basicamente vamos converter as coordenadas de clique do mouse,
        # para que fiquem entre -1.0 e 1.0.
        ndc_x = (2.0 * x_pos_ajust) / w - 1.0
        ndc_y = 1.0 - (2.0 * y_pos_ajust) / h
        
        V = glm.lookAt(glm.vec3(0.0, 0.0, 1.0),
                       glm.vec3(0.0, 0.0, 0.0),
                       glm.vec3(0.0, 1.0, 0.0))
        P = glm.ortho(-1.2, 1.2, -1.2, 1.2, -2, 2)
        
        R_Z = glm.rotate(glm.radians(ang), glm.vec3(0.0, 0.0, 1.0))
        R_X = glm.rotate(glm.radians(-45), glm.vec3(1.0, 0.0, 0.0))
        R = R_X * R_Z
        
        # vamos pegar as matrizes do tabuleiro e criar uma matriz model invertida.
        # faremos isso porque ao invés de passar informações 3D para gerar uma imagem 2D,
        # queremos que a imagem 2D receba o clique e o identifique no espaço 3D.
        # logo, iremos "desfazer" as transformações geométricas pra descobrir a posição.
        M_inv = glm.inverse(P * V * R)
        
        # esses pontos simulam o tamanho da cena.
        ponto_near = glm.vec4(ndc_x, ndc_y, -1.0, 1.0)
        ponto_far =  glm.vec4(ndc_x, ndc_y,  1.0, 1.0)
        
        # essas coordenadas representam de onde o clique saiu (mundo_near),
        # e onde aterrissou (mundo_far).
        mundo_near = M_inv * ponto_near
        mundo_far =  M_inv * ponto_far
        
        # normalizar
        mundo_near /= mundo_near.w
        mundo_far  /= mundo_far.w
        
        # como um vetor é o ponto final menos o inicial, iremos calcular o vetor
        # que vai da tela até o tabuleiro.
        direcao = glm.vec3(mundo_near - mundo_far)
        if abs(direcao.z) < 1e-6: return -1, -1 # se o vetor for paralelo ao plano (z ~= 0), não continuar.
        
        # equação de reta paramétrica para calcular o ponto de interseção entre a reta e o plano.
        # a variável t é o valor que modifica o módulo do vetor direção, para que, ao ser somado com mundo_near,
        # gere o ponto de interseção entre o vetor e o tabuleiro.
        t = (self.size - mundo_near.z)/ direcao.z
        p_intersecao = glm.vec3(mundo_near) + t * direcao
        
        click_x = p_intersecao.x
        click_y = p_intersecao.y
        tamanho_casa = self.size * 2
        
        # calcula a posição e pega o piso para que seja emparelhado com uma casa do tabuleiro.
        posicao_i = math.floor((click_x + 0.8 - self.size) / tamanho_casa + 0.5)
        posicao_j = math.floor((click_y + 0.8 - self.size) / tamanho_casa + 0.5)
        
        return posicao_i, posicao_j
    
    def colisao(self, i, j, l, c):
        if   i - 1 >= 0 and self.tab_matrix[i - 1][j] != 0 and (i - 2 == l and j == c): return False
        elif i + 1 <= 7 and self.tab_matrix[i + 1][j] != 0 and (i + 2 == l and j == c): return False
        elif j - 1 >= 0 and self.tab_matrix[i][j - 1] != 0 and (i == l and j - 2 == c): return False
        elif j + 1 <= 7 and self.tab_matrix[i][j + 1] != 0 and (i == l and j + 2 == c): return False
        return True
    
    # usaremos distância de manhattan para calcular as distâncias possívels a partir da casa selecionada.
    # distância de manhattan para vetores 2D = |x1 - x2| + |y1 - y2|
    # nesse caso, x1 e y1 são as casas do tabuleiro, e x2 e y2 são as posições da casa selecionada.
    
    def opcoes_movimento(self, l, c, alcance = 2):
        movimentos_validos = []
        
        for i in range(8):
            for j in range(8):
                # distância de manhattan
                distancia = abs(i - l) + abs(j - c)
                
                if distancia <= alcance and (i != l or j != c):
                    if self.tab_matrix[i][j] == 0 and self.colisao(i, j, l, c) == True: # se não for estrutura ou rio, é movimento válido
                        movimentos_validos.append((i, j))
        
        return movimentos_validos