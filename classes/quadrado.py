from OpenGL.GL import *
import numpy as np
import ctypes

class Quadrado:
    def __init__(self, r, g, b, size=1):
        self.vertices = [
            [-1*size,  1*size, r, g, b],
            [-1*size, -1*size, r, g, b],
            [ 1*size,  1*size, r, g, b],
            [ 1*size, -1*size, r, g, b]
        ]
        self.qtdVertices = len(self.vertices)
        
        self.vertices = np.array(self.vertices, np.float32)
        
        self.vaoId = glGenVertexArrays(1)
        glBindVertexArray(self.vaoId)
        
        vboId = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vboId)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)
        glEnableVertexAttribArray(0) # posicao
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 5*4, ctypes.c_void_p(0))
        glEnableVertexAttribArray(1) # cor
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 5*4, ctypes.c_void_p(2*4))
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        
        glBindVertexArray(0)
    
    def render(self, shaderId):
        glBindVertexArray(self.vaoId)
        
        glDrawArrays(GL_TRIANGLE_STRIP, 0, self.qtdVertices)
        glBindVertexArray(0)