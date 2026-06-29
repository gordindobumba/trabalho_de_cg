from OpenGL.GL import *
from pyglm import glm
from classes.cubo import *
from classes.modelo_obj import *
from classes.movimento import *
from classes.luz import *
import numpy as np

class Tabuleiro:
    def __init__(self, cubo1, cubo2):
        self.cubo1 = cubo1
        self.cubo2 = cubo2
        self.size = 0.1
        
        self.rio = Cubo(0.9, 0.9, 0.9, self.size, 1)
        self.predio = Cubo(0.1, 0.1, 0.1, self.size, 2)
        self.luz = Luz([-0.6, 0.7, 1.0], [0.0, 0.0, 1.0])
        
        self.tab_matrix = np.zeros((8, 8))
        self.tab_matrix[7][7] = 1
        self.tab_matrix[7][6] = 1
        self.tab_matrix[7][5] = 1
        self.tab_matrix[6][7] = 1
        self.tab_matrix[5][1] = 1
        self.tab_matrix[5][2] = 1
        self.tab_matrix[6][2] = 2
        self.tab_matrix[2][3] = 2
        
        self.movimento = Movimento(self.size, self.tab_matrix)

        self.personagens = []

        self.personagens.append({
            "obj": ModeloOBJ('retangulo.obj'),
            "linha": 1,
            "coluna": 1,
            "tipo": "medico",
            "cor": [0.0, 1.0, 1.0]
        })
        self.personagens.append({
            "obj": ModeloOBJ('retangulo.obj'),
            "linha": 2,
            "coluna": 1,
            "tipo": "medico",
            "cor": [0.0, 1.0, 1.0]
        })
        self.personagens.append({
            "obj": ModeloOBJ('retangulo.obj'),
            "linha": 3,
            "coluna": 1,
            "tipo": "medico",
            "cor": [0.0, 1.0, 1.0]
        })
        self.personagens.append({
            "obj": ModeloOBJ('retangulo.obj'),
            "linha": 4,
            "coluna": 6,
            "tipo": "virus",
            "cor": [1.0, 0.0, 1.0]
        })
        self.personagens.append({
            "obj": ModeloOBJ('retangulo.obj'),
            "linha": 5,
            "coluna": 6,
            "tipo": "virus",
            "cor": [1.0, 0.0, 1.0]
        })
        self.personagens.append({
            "obj": ModeloOBJ('retangulo.obj'),
            "linha": 6,
            "coluna": 6,
            "tipo": "virus",
            "cor": [1.0, 0.0, 1.0]
        })

        self.personagem_selecionado = 0
        self.cubo_selecionado = Cubo(0.0 , 1.0, 0.0, 0.1, 2)

        self.turno = "medico"
        
        self.modo_movimentar = False
        self.movimentos_validos = []
        self.cubo_alcance = Cubo(1, 1, 0.0, 0.1, 2)
    
    def render(self, shader, size, ang):
        shader.setUniformLocation('modelMatrix')
        shader.setUniformLocation('viewMatrix')
        shader.setUniformLocation('projMatrix')
        shader.setUniformLocation('normalMatrix')
        
        V = glm.lookAt(glm.vec3(0.0, 0.0, 1.0),
                       glm.vec3(0.0, 0.0, 0.0),
                       glm.vec3(0.0, 1.0, 0.0))
        P = glm.ortho(-1.2, 1.2, -1.2, 1.2, -2, 2)
        
        shader.setUniformMatrix('viewMatrix', V)
        shader.setUniformMatrix('projMatrix', P)
        
        n = np.int32(0.8/size)
        R_Z = glm.rotate(glm.radians(ang), glm.vec3(0.0, 0.0, 1.0))
        R_X = glm.rotate(glm.radians(-45), glm.vec3(1.0, 0.0, 0.0))
        R = R_X * R_Z

        # descobrir posição do personagem selecionado
        personagem = self.personagens[self.personagem_selecionado]
        linha_selecionada = personagem["linha"]
        coluna_selecionada = personagem["coluna"]
        
        for i in range(n):
            for j in range(n):
                x_axis = (i * size * 2) - (0.8 - size)
                y_axis = (j * size * 2) - (0.8 - size)
                if self.tab_matrix[i][j] == 1:
                    S = glm.scale(glm.vec3(1, 1, 0.8))
                    T = glm.translate(glm.vec3(x_axis, y_axis, -0.02))
                    X = T * S
                else: 
                    T = glm.translate(glm.vec3(x_axis, y_axis, 0))
                    X = T
                M = R * X
                N = glm.transpose(glm.inverse(M))
                shader.setUniformMatrix('modelMatrix', M)
                shader.setUniformMatrix('normalMatrix', N)
                
                if self.tab_matrix[i][j] == 1: 
                    self.rio.render(shader)
                else:
                    if i == linha_selecionada and j == coluna_selecionada:
                        self.cubo_selecionado.render(shader)
                    elif self.modo_movimentar and (i, j) in self.movimentos_validos:
                        self.cubo_alcance.render(shader)
                    else:
                        if (i + j) % 2 == 0: 
                            self.cubo1.render(shader)
                        else: 
                            self.cubo2.render(shader)
                        if self.tab_matrix[i][j] == 2:
                            S = glm.scale(glm.vec3(0.4, 0.4, 2.0))
                            T = glm.translate(glm.vec3(x_axis, y_axis, 0.15))
                            M = R * (T * S)
                            shader.setUniformMatrix('modelMatrix', M)
                            self.predio.render(shader)
        
        self.luz.render(shader)

        # colocar personagens 
        for personagem in self.personagens:
            linha = personagem["linha"]
            coluna = personagem["coluna"]

            x = (linha * size * 2) - (0.8 - size)
            y = (coluna * size * 2) - (0.8 - size)
                
            personagem["obj"].render(shader,
                               glm.vec3(x, y, 0.08),
                               R,
                               personagem["cor"])

    # trocar de personagem - passa pro próximo da lista
    def proximo_personagem(self):
        self.personagem_selecionado += 1
        if self.personagem_selecionado >= len(self.personagens):
            self.personagem_selecionado = 0


    def mudar_posicao_personagem(self, x_pos, y_pos, width, height, ang):
        clicado_i, clicado_j = self.movimento.calcular_posicao(x_pos, y_pos, width, height, ang)
        
        if 0 <= clicado_i < 8 and 0 <= clicado_j < 8:
            personagem = self.personagens[self.personagem_selecionado]
            
            if not self.modo_movimentar:
                
                # se clicou no mesmo personagem, mostra as casas válidas
                if clicado_i == personagem["linha"] and clicado_j == personagem["coluna"]:
                    if personagem["tipo"] != self.turno:
                        return
                    self.modo_movimentar = True 
                    movimentos = self.movimento.opcoes_movimento(clicado_i, clicado_j)
                    self.movimentos_validos = []
                    for casa in movimentos:
                        i, j = casa
                        if not self.casa_ocupada(i, j, personagem):
                            self.movimentos_validos.append(casa)
                
                # se não clicou no mesmo personagem, checa se clicou no outro personagem
                else:   
                    for id, p in enumerate(self.personagens):
                        if p["linha"] == clicado_i and p["coluna"] == clicado_j:
                            if p["tipo"] != self.turno:
                                return
                            self.personagem_selecionado = id
                            personagem = p
                            self.modo_movimentar = True
                            movimentos = self.movimento.opcoes_movimento(clicado_i, clicado_j)
                            self.movimentos_validos = []
                            for casa in movimentos:
                                i, j = casa
                                if not self.casa_ocupada(i, j, personagem):
                                    self.movimentos_validos.append(casa)
                            break
            else:
                # verifica se a casa selecionada é válida
                if (clicado_i, clicado_j) in self.movimentos_validos:
                    personagem["linha"] = clicado_i
                    personagem["coluna"] = clicado_j
                    self.passar_turno()

                self.modo_movimentar = False
                self.movimentos_validos = []

    # verificar se a casa já é ocupada por outro personagem
    def casa_ocupada(self, linha, coluna, ignorar=None):
        for personagem in self.personagens:
            if personagem is ignorar:
                continue
            if (personagem["linha"] == linha and personagem["coluna"] == coluna):
                return True
        return False
    
    # passar para o próximo turno
    def passar_turno(self):
        self.modo_movimentar = False
        self.movimentos_validos = []    
        if self.turno == "medico":
            self.turno = "virus"
        else:
            self.turno = "medico"
        for i, p in enumerate(self.personagens):
            if p["tipo"] == self.turno:
                self.personagem_selecionado = i
                break