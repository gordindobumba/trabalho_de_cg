from OpenGL.GL import *
import numpy as np
from pyglm import glm
import os
import ctypes

class ModeloOBJ:
    def __init__(self, caminho):
        # carregar obj
        self.vertices = []
        self.carregar_obj(caminho)
        self.vertices = np.array(self.vertices, dtype=np.float32)

        # criar e ativar vao e vbo
        self.vao = glGenVertexArrays(1)
        self.vbo = glGenBuffers(1)
        glBindVertexArray(self.vao)
        glBindBuffer(GL_ARRAY_BUFFER, 
                     self.vbo)
        
        # enviar dados pra gpu
        glBufferData(GL_ARRAY_BUFFER, 
                     self.vertices.nbytes, 
                     self.vertices, 
                     GL_STATIC_DRAW)
        
        # configurar e habilitar atributo de posição
        glVertexAttribPointer(0, 
                              3, 
                              GL_FLOAT, 
                              GL_FALSE, 
                              6*4, 
                              ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        # configurar e habilitar atributo de normal
        glVertexAttribPointer(1, 
                              3, 
                              GL_FLOAT, 
                              GL_FALSE, 
                              6*4, 
                              ctypes.c_void_p(3*4))
        glEnableVertexAttribArray(1)

        # desativar vao e vbo no final
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    def carregar_obj(self, caminho):
        vertices_temp = []
        normais_temp = []

        # abrir arquivo e ler por linha
        here = os.path.dirname(os.path.abspath(caminho))
        with open(os.path.join(here, 'retangulo.obj'), 'r') as arquivo:
            for linha in arquivo:
                valores = linha.split()

                # ignorar linhas vazias
                if not valores: continue

                # se forem vértices, lê e salva
                if valores[0] == 'v':
                    vertices_temp.append([
                        float(valores[1]),
                        float(valores[2]),
                        float(valores[3])
                    ])

                # se forem normais, lê e salva
                elif valores[0] == 'vn':
                    normais_temp.append([
                        float(valores[1]),
                        float(valores[2]),
                        float(valores[3])
                    ])

                # se forem faces, lê, processa cada vértice e normal, pega o índice e adiciona
                elif valores[0] == 'f':
                    for face in valores[1:]:
                        dados = face.split('/')

                        indice_vertice = int(dados[0]) - 1
                        indice_normal = int(dados[2]) - 1

                        vertice = vertices_temp[indice_vertice]
                        normal = normais_temp[indice_normal]

                        self.vertices.extend(vertice)
                        self.vertices.extend(normal)

    def render(self, shader, posicao, R, cor):
        # mover objeto no mundo
        model = glm.mat4(1.0)
        model = glm.translate(model, posicao)
        model = glm.rotate(model, glm.radians(90.0), glm.vec3(1, 0 ,0))
        model = glm.scale(model, glm.vec3(0.03))
        model = R * model

        # pegar localização dos uniforms
        modelLoc = glGetUniformLocation(shader, "modelMatrix")
        normalLoc = glGetUniformLocation(shader, "normalMatrix")
        colorLoc = glGetUniformLocation(shader, "objectColor")

        # calcular normal matrix
        normalMatrix = glm.transpose(glm.inverse(model))

        # enviar model matrix
        glUniformMatrix4fv(modelLoc, 
                           1, 
                           GL_FALSE, 
                           glm.value_ptr(model))

        # enviar normal matrix
        glUniformMatrix4fv(normalLoc,
                           1,
                           GL_FALSE,
                           glm.value_ptr(normalMatrix))
        
        # enviar cor
        glUniform3f(colorLoc, cor[0], cor[1], cor[2])
        
        
        # ativar vao
        glBindVertexArray(self.vao)

        # desenhar triângulos
        glDrawArrays(GL_TRIANGLES, 0, len(self.vertices)//6)
        
        # desativar vao
        glBindVertexArray(0)
