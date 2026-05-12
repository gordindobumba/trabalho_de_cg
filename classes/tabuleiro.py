from OpenGL.GL import *
from pyglm import glm
from classes.cubo import *
import numpy as np

class Tabuleiro:
    def __init__(self, quadrado1, quadrado2):
        self.quadrado1 = quadrado1
        self.quadrado2 = quadrado2
        
        tab_matriz = np.array((8, 8)) # pra quando for botar os elementos no tabuleiro
    
    def render(self, shaderId, size, ang):
        modelMatrix_loc = glGetUniformLocation(shaderId, 'modelMatrix')
        viewMatrix_loc = glGetUniformLocation(shaderId, 'viewMatrix')
        projMatrix_loc = glGetUniformLocation(shaderId, 'projMatrix')
        
        V = glm.translate(glm.vec3(0.0, 0.0, 0.0))
        P = glm.ortho(-1.2, 1.2, -1.2, 1.2, -2, 2)
        
        glUniformMatrix4fv(viewMatrix_loc, 1, GL_FALSE, glm.value_ptr(V))
        glUniformMatrix4fv(projMatrix_loc, 1, GL_FALSE, glm.value_ptr(P))
        
        n = np.int32(0.8/size)
        R_Z = glm.rotate(glm.radians(ang), glm.vec3(0.0, 0.0, 1.0))
        R_X = glm.rotate(glm.radians(-60), glm.vec3(1.0, 0.0, 0.0))
        R = R_X * R_Z
        
        for i in range(n):
            for j in range(n):
                x_axis = (i * size * 2) - (0.8 - size)
                y_axis = (j * size * 2) - (0.8 - size)
                T = glm.translate(glm.vec3(x_axis, y_axis, 0))
                M = R * T
                glUniformMatrix4fv(modelMatrix_loc, 1, GL_FALSE, glm.value_ptr(M))
                
                if (i + j) % 2 == 0: self.quadrado1.render(shaderId)
                else: self.quadrado2.render(shaderId)
        
        