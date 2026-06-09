from OpenGL.GL import *
from pyglm import glm
from classes.cubo import *
from classes.modelo_obj import *

class Movimento:
    def __init__(self, size):
        self.size = size

    def calcular_posicao(self, x_pos, y_pos, width, height, ang):
        ndc_x = (2.0 * x_pos) / width - 1.0
        ndc_y = 1.0 - (2.0 * y_pos) / height
        
        V = glm.lookAt(glm.vec3(0.0, 0.0, 1.0),
                       glm.vec3(0.0, 0.0, 0.0),
                       glm.vec3(0.0, 1.0, 0.0))
        P = glm.ortho(-1.2, 1.2, -1.2, 1.2, -2, 2)
        
        R_Z = glm.rotate(glm.radians(ang), glm.vec3(0.0, 0.0, 1.0))
        R_X = glm.rotate(glm.radians(-45), glm.vec3(1.0, 0.0, 0.0))
        R = R_X * R_Z
        
        M_inv = glm.inverse(P * V * R)
        
        ponto_near = glm.vec4(ndc_x, ndc_y, -1.0, 1.0)
        ponto_far =  glm.vec4(ndc_x, ndc_y,  1.0, 1.0)
        
        mundo_near = M_inv * ponto_near
        mundo_far =  M_inv * ponto_far
        
        mundo_near /= mundo_near.w
        mundo_far  /= mundo_far.w
        
        direcao = glm.vec3(mundo_near - mundo_far)
        if abs(direcao.z) < 1e-6: return
        
        t = (-1)*mundo_near.z / direcao.z
        p_intersecao = glm.vec3(mundo_near) + t * direcao
        
        click_x = p_intersecao.x
        click_y = p_intersecao.y
        
        clicado_i = round(((click_x + (0.8 - self.size)) / (self.size * 2)))
        clicado_j = round(((click_y + (0.8 - self.size)) / (self.size * 2)))
        
        return clicado_i, clicado_j