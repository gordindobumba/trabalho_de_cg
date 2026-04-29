from OpenGL.GL import *
from pyglm import glm
from classes.quadrado import *
import numpy as np

class Tabuleiro:
    def __init__(self, quadrado1, quadrado2):
        self.quadrado1 = quadrado1
        self.quadrado2 = quadrado2
    
    def render(self, shaderId, T, size):
        x_axis = 0.8 - size
        y_axis = 0.8 - size
        n = np.int32(0.8/size)
        for i in range(n):
            for j in range(n):
                T = glm.translate(glm.vec3(x_axis, y_axis, 0))
                modelMatrix_loc = glGetUniformLocation(shaderId, 'modelMatrix')
                glUniformMatrix4fv(modelMatrix_loc, 1, GL_FALSE, glm.value_ptr(T))
                if j % 2 == 0:
                    if i % 2 == 0: self.quadrado1.render(shaderId)
                    else: self.quadrado2.render(shaderId)
                else:
                    if i % 2 == 0: self.quadrado2.render(shaderId)
                    else: self.quadrado1.render(shaderId)
                x_axis -= size * 2
            y_axis -= size * 2
            x_axis = 0.8 - size
        
        