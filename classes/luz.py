from OpenGL.GL import *
from pyglm import glm
from classes.shader import *
from classes.cubo import *

class Luz:
    def __init__(self, lightPos, camPos):
        self.lightPos = lightPos
        self.camPos = camPos
        self.light = Cubo(1, 1, 1, 0.05, 2)
        
    def render(self, shader):
        shader.setUniform('lightPos', self.lightPos[0], self.lightPos[1], self.lightPos[2])
        shader.setUniform('camPos', self.camPos[0], self.camPos[1], self.camPos[2])
        shader.setUniform('lightColor', 1, 1, 1)
        
        T = glm.translate(glm.vec3(self.lightPos[0], self.lightPos[1], self.lightPos[2]))
        R_Z = glm.rotate(glm.radians(45), glm.vec3(0.0, 0.0, 1.0))
        R_X = glm.rotate(glm.radians(-45), glm.vec3(1.0, 0.0, 0.0))
        R = R_X * R_Z
        M = T * R
        N = glm.transpose(glm.inverse(M))
        shader.setUniformMatrix('modelMatrix', M)
        shader.setUniformMatrix('normalMatrix', N)
        self.light.render(shader)