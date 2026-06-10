from OpenGL.GL import *
import numpy as np
import ctypes

class Cubo:
    def __init__(self, r, g, b, size=1):
        vertices = [ # 6 faces = 12 triangulos = 36 vertices
            [-size, -size, -size, 0, -1, 0, r, g, b],
            [-size, -size,  size, 0, -1, 0, r, g, b],
            [ size, -size, -size, 0, -1, 0, r, g, b], # ABC
            [-size, -size,  size, 0, -1, 0, r, g, b],
            [ size, -size, -size, 0, -1, 0, r, g, b],
            [ size, -size,  size, 0, -1, 0, r, g, b], # BCD
            [ size, -size, -size,  1, 0, 0, r, g, b],
            [ size, -size,  size,  1, 0, 0, r, g, b],
            [ size,  size, -size,  1, 0, 0, r, g, b], # CDE
            [ size, -size,  size,  1, 0, 0, r, g, b],
            [ size,  size, -size,  1, 0, 0, r, g, b],
            [ size,  size,  size,  1, 0, 0, r, g, b], # DEF
            [ size,  size, -size, 0,  1, 0, r, g, b],
            [ size,  size,  size, 0,  1, 0, r, g, b],
            [-size,  size, -size, 0,  1, 0, r, g, b], # EFG
            [ size,  size,  size, 0,  1, 0, r, g, b],
            [-size,  size, -size, 0,  1, 0, r, g, b],
            [-size,  size,  size, 0,  1, 0, r, g, b], # FGH
            [-size,  size, -size, -1, 0, 0, r, g, b],
            [-size,  size,  size, -1, 0, 0, r, g, b],
            [-size, -size, -size, -1, 0, 0, r, g, b], # AGH
            [-size,  size,  size, -1, 0, 0, r, g, b],
            [-size, -size, -size, -1, 0, 0, r, g, b],
            [-size, -size,  size, -1, 0, 0, r, g, b], # BAG
            [-size, -size,  size, 0, 0,  1, r, g, b],
            [-size,  size,  size, 0, 0,  1, r, g, b],
            [ size, -size,  size, 0, 0,  1, r, g, b], # BHD
            [-size,  size,  size, 0, 0,  1, r, g, b],
            [ size, -size,  size, 0, 0,  1, r, g, b],
            [ size,  size,  size, 0, 0,  1, r, g, b], # HDF
            [-size, -size, -size, 0, 0, -1, r, g, b],
            [-size,  size, -size, 0, 0, -1, r, g, b],
            [ size, -size, -size, 0, 0, -1, r, g, b], # AGC
            [-size,  size, -size, 0, 0, -1, r, g, b],
            [ size, -size, -size, 0, 0, -1, r, g, b],
            [ size,  size, -size, 0, 0, -1, r, g, b]  # GCE
        ]
        
        self.r = r
        self.g = g
        self.b = b
        self.vertices = vertices
        self.qtdVertices = len(self.vertices)
        
        self.vertices = np.array(self.vertices, np.float32)
        
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
            9*4,
            ctypes.c_void_p(0)
        )

        # normal
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(
            1,
            3,
            GL_FLOAT,
            GL_FALSE,
            9*4,
            ctypes.c_void_p(3*4)
        )

        # cor
        glEnableVertexAttribArray(2)
        glVertexAttribPointer(
            2,
            3,
            GL_FLOAT,
            GL_FALSE,
            9*4,
            ctypes.c_void_p(6*4)
        )
                
        glBindVertexArray(0)
    
    def render(self, shaderId):
        glBindVertexArray(self.vaoId)
        colorLoc = glGetUniformLocation(shaderId, "objectColor")
        glUniform3f(colorLoc, self.r, self.g, self.b)
        glDrawArrays(GL_TRIANGLES, 0, self.qtdVertices)
        glBindVertexArray(0)