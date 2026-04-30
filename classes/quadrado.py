from OpenGL.GL import *
import numpy as np
import ctypes

class Quadrado:
    def __init__(self, r, g, b, size=1):
        vertices = [ # 6 faces = 12 triangulos = 36 vertices
            [-size, -size, -size, r, g, b],
            [-size, -size,  size, r, g, b],
            [ size, -size, -size, r, g, b], # ABC
            [-size, -size,  size, r, g, b],
            [ size, -size, -size, r, g, b],
            [ size, -size,  size, r, g, b], # BCD
            [ size, -size, -size, r, g, b],
            [ size, -size,  size, r, g, b],
            [ size,  size, -size, r, g, b], # CDE
            [ size, -size,  size, r, g, b],
            [ size,  size, -size, r, g, b],
            [ size,  size,  size, r, g, b], # DEF
            [ size,  size, -size, r, g, b],
            [ size,  size,  size, r, g, b],
            [-size,  size, -size, r, g, b], # EFG
            [ size,  size,  size, r, g, b],
            [-size,  size, -size, r, g, b],
            [-size,  size,  size, r, g, b], # FGH
            [-size,  size, -size, r, g, b],
            [-size,  size,  size, r, g, b],
            [-size, -size, -size, r, g, b], # AGH
            [-size,  size,  size, r, g, b],
            [-size, -size, -size, r, g, b],
            [-size, -size,  size, r, g, b], # BAG
            [-size, -size,  size, r, g, b],
            [-size,  size,  size, r, g, b],
            [ size, -size,  size, r, g, b], # BHD
            [-size,  size,  size, r, g, b],
            [ size, -size,  size, r, g, b],
            [ size,  size,  size, r, g, b], # HDF
            [-size, -size, -size, r, g, b],
            [-size,  size, -size, r, g, b],
            [ size, -size, -size, r, g, b], # AGC
            [-size,  size, -size, r, g, b],
            [ size, -size, -size, r, g, b],
            [ size,  size, -size, r, g, b]  # GCE
        ]
        
        self.vertices = vertices
        self.qtdVertices = len(self.vertices)
        
        self.vertices = np.array(self.vertices, np.float32)
        
        self.vaoId = glGenVertexArrays(1)
        glBindVertexArray(self.vaoId)
        
        vboId = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vboId)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)
        glEnableVertexAttribArray(0) # posicao
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6*4, ctypes.c_void_p(0))
        glEnableVertexAttribArray(1) # cor
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6*4, ctypes.c_void_p(3*4))
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        
        glBindVertexArray(0)
    
    def render(self, shaderId):
        glBindVertexArray(self.vaoId)
        
        glDrawArrays(GL_TRIANGLES, 0, self.qtdVertices)
        glBindVertexArray(0)