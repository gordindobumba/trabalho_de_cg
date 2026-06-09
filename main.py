import glfw
from OpenGL.GL import *
import os
import OpenGL.GL.shaders as gls
from classes.cubo import *
from classes.mainaxis import *
from classes.tabuleiro import *
from pyglm import glm

cubo1 = None
cubo2 = None
tabuleiro = None
size = 0
shaderId = 0
ang = 45
window_size = 800

def init():
    global cubo1, cubo2,  tabuleiro, shaderId, size

    size = 0.1
    cubo1 = Cubo(255/255, 209/255, 171/255, size)
    cubo2 = Cubo(156/255, 104/255, 0, size)
    tabuleiro = Tabuleiro(cubo1, cubo2)
    
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
        # fechar jogo
        if key == glfw.KEY_ESCAPE: glfw.window_should_close(window)

        #trocar personagem
        elif key == glfw.KEY_TAB:
            tabuleiro.proximo_personagem()

def process_mouse(window, button, action, mods):
    if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS:
        width, height = glfw.get_window_size(window)
        x_pos, y_pos = glfw.get_cursor_pos(window)
        tabuleiro.processar_clique(x_pos, y_pos, width, height, ang)

def process_input(window):
    global ang
    if glfw.get_key(window, glfw.KEY_RIGHT) == glfw.PRESS:
        ang += 1
    if glfw.get_key(window, glfw.KEY_LEFT) == glfw.PRESS:
        ang -= 1

def window_resize(window, width, height):
    if width < window_size:
        y = (height - window_size)//2
        glViewport(0, y, width, window_size)
    elif height < window_size:
        x = (width - window_size)//2
        glViewport(x, 0, window_size, height)
    else:
        size = min(width, height)
        x = (width - size)//2
        y = (height - size)//2
        glViewport(x, y, size, size)
        

def main():
    glfw.init()
    width, height = 800, 800

    window = glfw.create_window(width, height, 'projeto', None, None)
    glfw.make_context_current(window)
    glfw.set_window_size_callback(window, window_resize)
    glfw.set_key_callback(window, keyboard)
    glfw.set_mouse_button_callback(window, process_mouse)
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