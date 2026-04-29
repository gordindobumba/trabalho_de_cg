import glfw
from OpenGL.GL import *
import os
import OpenGL.GL.shaders as gls
from classes.quadrado import *
from classes.mainaxis import *
from classes.tabuleiro import *
from pyglm import glm

quadrado1 = None
quadrado2 = None
mainAxis = None
tabuleiro = None
size = 0
shaderId = 0

def init():
    global quadrado1, quadrado2, mainAxis, tabuleiro, shaderId, size

    size = 0.1
    quadrado1 = Quadrado(255/255, 209/255, 171/255, size)
    quadrado2 = Quadrado(156/255, 104/255, 0, size)
    tabuleiro = Tabuleiro(quadrado1, quadrado2)
    mainAxis = MainAxis()
    
    glClearColor(0,0,0,1)
    glLineWidth(3)
    
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, 'shaderVertex.glsl'), 'r') as file:
        vsSource = file.read()
    with open(os.path.join(here, 'shaderFragment.glsl'), 'r') as file:
        fsSource = file.read()
    
    vsId = gls.compileShader(vsSource, GL_VERTEX_SHADER)
    fsId = gls.compileShader(fsSource, GL_FRAGMENT_SHADER)
    shaderId = gls.compileProgram(vsId, fsId)

def render():
        glClear(GL_COLOR_BUFFER_BIT)
        glUseProgram(shaderId)
        
        M = glm.mat4(1.0)
        modelMatrix_loc = glGetUniformLocation(shaderId, 'modelMatrix')
        glUniformMatrix4fv(modelMatrix_loc, 1, GL_FALSE, glm.value_ptr(M))
        
        tabuleiro.render(shaderId, M, size)
        
        glUseProgram(0)
    
def main():
    glfw.init()
    janela = glfw.create_window(700, 700, 'poligonos', None, None)
    glfw.make_context_current(janela)
    init()
    
    while not glfw.window_should_close(janela):
        glfw.poll_events()
        render()
        glfw.swap_buffers(janela)
    glfw.terminate()

if __name__ == '__main__':
    main()