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
ang = 45

def init():
    global quadrado1, quadrado2, mainAxis, tabuleiro, shaderId, size

    size = 0.1
    quadrado1 = Quadrado(255/255, 209/255, 171/255, size)
    quadrado2 = Quadrado(156/255, 104/255, 0, size)
    tabuleiro = Tabuleiro(quadrado1, quadrado2)
    mainAxis = MainAxis()
    
    glClearColor(0,0,0,1)
    glEnable(GL_DEPTH_TEST);
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
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glUseProgram(shaderId)
        
        tabuleiro.render(shaderId, size, ang)
        
        glUseProgram(0)

def keyboard(window, key, scancode, action, mods):
    if action == glfw.PRESS:
        if key == glfw.KEY_ESCAPE: glfw.window_should_close(window)

def process_input(window):
    global ang
    if glfw.get_key(window, glfw.KEY_RIGHT) == glfw.PRESS:
        ang += 1
    if glfw.get_key(window, glfw.KEY_LEFT) == glfw.PRESS:
        ang -= 1

def main():
    glfw.init()
    window = glfw.create_window(1000, 1000, 'projeto', None, None)
    glfw.make_context_current(window)
    glfw.set_key_callback(window, keyboard)
    init()
    
    intervalo_input = 1.0/60.0
    tempo_acumulado = 0.0
    ultimo_tempo = glfw.get_time()
    
    while not glfw.window_should_close(window):
        tempo_atual = glfw.get_time()
        delta_t = tempo_atual - ultimo_tempo
        ultimo_tempo = tempo_atual
        
        tempo_acumulado += delta_t
        
        glfw.poll_events()
        
        if tempo_acumulado >= intervalo_input:
            process_input(window)
            tempo_acumulado -= intervalo_input
            
        render()
        glfw.swap_buffers(window)
    glfw.terminate()

if __name__ == '__main__':
    main()