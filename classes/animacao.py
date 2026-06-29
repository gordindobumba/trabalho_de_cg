import glfw
from OpenGL.GL import *

class Animacao():
    def __init__(self, vel = 0.0075):
        self.animando = False
        self.origem = [0.0, 0.0]
        self.destino = [0.0, 0.0]
        self.atual = [0.0, 0.0]
        self.t = 0.0
        self.vel = vel
    
    def iniciar(self, x1, y1, x2, y2):
        self.origem = [x1, y1]
        self.destino = [x2, y2]
        self.atual = [x1, y1]
        self.t = 0.0
        self.animando = True
    
    def animar(self):
        if self.animando == False: return
        
        self.t += self.vel
        if self.t >= 1.0:
            self.t = 1.0
            self.animando = False
        
        ease_out = 1 - (1 - self.t) ** 2
        self.atual[0] = self.origem[0] + (self.destino[0] - self.origem[0]) * ease_out
        self.atual[1] = self.origem[1] + (self.destino[1] - self.origem[1]) * ease_out