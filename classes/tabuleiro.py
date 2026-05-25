from OpenGL.GL import *
from pyglm import glm
from classes.cubo import *
from classes.modelo_obj import *
import numpy as np

class Tabuleiro:
    def __init__(self, cubo1, cubo2):
        self.cubo1 = cubo1
        self.cubo2 = cubo2
        
        self.rio = Cubo(0, 0, 235/255, 0.1)
        
        self.tab_matrix = np.zeros((8, 8))
        self.tab_matrix[7][7] = 1
        self.tab_matrix[7][6] = 1
        self.tab_matrix[7][5] = 1
        self.tab_matrix[6][7] = 1
        self.tab_matrix[5][1] = 1
        self.tab_matrix[5][2] = 1

        self.personagens = []

        self.personagens.append({
            "obj": ModeloOBJ("modelos/retangulo.obj"),
            "linha": 2,
            "coluna": 1
        })
        self.personagens.append({
            "obj": ModeloOBJ("modelos/retangulo.obj"),
            "linha": 5,
            "coluna": 6
        })
    
    def render(self, shaderId, size, ang):
        modelMatrix_loc = glGetUniformLocation(shaderId, 'modelMatrix')
        viewMatrix_loc = glGetUniformLocation(shaderId, 'viewMatrix')
        projMatrix_loc = glGetUniformLocation(shaderId, 'projMatrix')
        
        V = glm.lookAt(glm.vec3(0.0, 0.0, 1.0),
                       glm.vec3(0.0, 0.0, 0.0),
                       glm.vec3(0.0, 1.0, 0.0))
        P = glm.ortho(-1.2, 1.2, -1.2, 1.2, -2, 2)
        
        glUniformMatrix4fv(viewMatrix_loc, 1, GL_FALSE, glm.value_ptr(V))
        glUniformMatrix4fv(projMatrix_loc, 1, GL_FALSE, glm.value_ptr(P))
        
        n = np.int32(0.8/size)
        R_Z = glm.rotate(glm.radians(ang), glm.vec3(0.0, 0.0, 1.0))
        R_X = glm.rotate(glm.radians(-50), glm.vec3(1.0, 0.0, 0.0))
        R = R_X * R_Z
        
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
                glUniformMatrix4fv(modelMatrix_loc, 1, GL_FALSE, glm.value_ptr(M))
                
                if self.tab_matrix[i][j] == 1: self.rio.render(shaderId)
                else:
                    if (i + j) % 2 == 0: self.cubo1.render(shaderId)
                    else: self.cubo2.render(shaderId)

        # colocar personagens 
        for personagem in self.personagens:
            linha = personagem["linha"]
            coluna = personagem["coluna"]

            x = (linha * size * 2) - (0.8 - size)
            y = (coluna * size * 2) - (0.8 - size)
                
            personagem["obj"].render(shaderId,
                               glm.vec3(x, y, 0.08),
                               R)
            
        