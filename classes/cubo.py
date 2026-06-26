from OpenGL.GL import *
import numpy as np
import ctypes
from classes.shader import *
from classes.texturas import *

class Cubo:
    def __init__(self, r, g, b, size=1):
        vertices = [
            #      vertices        normal     cor   textura
            [-size, -size, -size, 0, -1, 0, r, g, b, 0, 0],
            [ size, -size, -size, 0, -1, 0, r, g, b, 1, 0],
            [-size, -size,  size, 0, -1, 0, r, g, b, 0, 1],
            
            [-size, -size,  size, 0, -1, 0, r, g, b, 0, 1],
            [ size, -size, -size, 0, -1, 0, r, g, b, 1, 0],
            [ size, -size,  size, 0, -1, 0, r, g, b, 1, 1],
            
            # face da direita, normal = x positivo
            [ size, -size, -size,  1, 0, 0, r, g, b, 0, 0],
            [ size,  size, -size,  1, 0, 0, r, g, b, 1, 0],
            [ size, -size,  size,  1, 0, 0, r, g, b, 0, 1],
            
            [ size, -size,  size,  1, 0, 0, r, g, b, 0, 1],
            [ size,  size, -size,  1, 0, 0, r, g, b, 1, 0],
            [ size,  size,  size,  1, 0, 0, r, g, b, 1, 1],
            
            # face de cima, normal = y positivo
            [-size,  size,  size, 0,  1, 0, r, g, b, 0, 0],
            [ size,  size,  size, 0,  1, 0, r, g, b, 1, 0],
            [-size,  size, -size, 0,  1, 0, r, g, b, 0, 1],
            
            [-size,  size, -size, 0,  1, 0, r, g, b, 0, 1],
            [ size,  size,  size, 0,  1, 0, r, g, b, 1, 0],
            [ size,  size, -size, 0,  1, 0, r, g, b, 1, 1],
            
            # face da esquerda, normal = x negativo
            [-size, -size,  size, -1, 0, 0, r, g, b, 0, 0],
            [-size,  size,  size, -1, 0, 0, r, g, b, 1, 0],
            [-size, -size, -size, -1, 0, 0, r, g, b, 0, 1],
            
            [-size, -size, -size, -1, 0, 0, r, g, b, 0, 1],
            [-size,  size,  size, -1, 0, 0, r, g, b, 1, 0],
            [-size,  size, -size, -1, 0, 0, r, g, b, 1, 1],
            
            # face frontal, normal = z positivo
            [-size, -size,  size, 0, 0,  1, r, g, b, 0, 0],
            [ size, -size,  size, 0, 0,  1, r, g, b, 1, 0],
            [-size,  size,  size, 0, 0,  1, r, g, b, 0, 1],
            
            [-size,  size,  size, 0, 0,  1, r, g, b, 0, 1],
            [ size, -size,  size, 0, 0,  1, r, g, b, 1, 0],
            [ size,  size,  size, 0, 0,  1, r, g, b, 1, 1],
            
            # face do fundo, normal = z negativo
            [ size, -size, -size, 0, 0, -1, r, g, b, 0, 0],
            [-size, -size, -size, 0, 0, -1, r, g, b, 1, 0],
            [ size,  size, -size, 0, 0, -1, r, g, b, 0, 1],
            
            [ size,  size, -size, 0, 0, -1, r, g, b, 0, 1],
            [-size, -size, -size, 0, 0, -1, r, g, b, 1, 0],
            [-size,  size, -size, 0, 0, -1, r, g, b, 1, 1]  # GCE
        ]
        
        self.cores = [r, g, b]
        self.vertices = vertices
        self.qtdVertices = len(self.vertices)
        
        self.vertices = np.array(self.vertices, np.float32)
        self.textura1 = Textura('marmore_cor.jpg')
        self.textura2 = Textura('marmore_rugosa.jpg')
        self.textura3 = Textura('marmore_normal.jpg')
        
        self.vaoId = glGenVertexArrays(1)
        glBindVertexArray(self.vaoId)
        
        vboId = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vboId)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)
        
        # posição
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(
            0,
            3,
            GL_FLOAT,
            GL_FALSE,
            11*4,
            ctypes.c_void_p(0)
        )

        # normal
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(
            1,
            3,
            GL_FLOAT,
            GL_FALSE,
            11*4,
            ctypes.c_void_p(3*4)
        )

        # cor
        glEnableVertexAttribArray(2)
        glVertexAttribPointer(
            2,
            3,
            GL_FLOAT,
            GL_FALSE,
            11*4,
            ctypes.c_void_p(6*4)
        )
        
        # textura
        glEnableVertexAttribArray(3)
        glVertexAttribPointer(
            3,
            2,
            GL_FLOAT,
            GL_FALSE,
            11*4,
            ctypes.c_void_p(9*4)
        )
                
        glBindVertexArray(0)
    
    def render(self, shader):
        glBindVertexArray(self.vaoId)
        shader.setUniform('objectColor', self.cores[0], self.cores[1], self.cores[2])
        glDrawArrays(GL_TRIANGLES, 0, self.qtdVertices)
        glBindVertexArray(0)