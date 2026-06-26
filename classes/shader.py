from OpenGL.GL import *
import OpenGL.GL.shaders as gls
from classes.cubo import *
from classes.modelo_obj import *
from classes.movimento import *

class Shader:
    def __init__(self):
        path = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(path, '..', 'shaders', 'shaderVertex.glsl'), 'r') as file:
            vsSource = file.read()
        with open(os.path.join(path, '..', 'shaders', 'shaderFragment.glsl'), 'r') as file:
            fsSource = file.read()
        
        vsId = gls.compileShader(vsSource, GL_VERTEX_SHADER)
        fsId = gls.compileShader(fsSource, GL_FRAGMENT_SHADER)
        self.shaderId = gls.compileProgram(vsId, fsId)
        self.uniforms = {}
    
    def bind(self):
        glUseProgram(self.shaderId)
    
    def unbind(self):
        glUseProgram(0)
    
    def setUniformLocation(self, name):
        if name not in self.uniforms:
            loc = glGetUniformLocation(self.shaderId, name)
            self.uniforms[name] = loc
    
    def setTexture(self, name, idx):
        loc = self.getUniformLocation(name)
        glUniform1i(loc, idx)
    
    def setUniform(self, name, x, y = None, z = None):
        loc = self.getUniformLocation(name)
        if y == None and z == None:
            glUniform1f(loc, x)
        elif z == None:
            glUniform2f(loc, x, y)
        else:
            glUniform3f(loc, x, y, z)
    
    def getUniformLocation(self, name, idx = None):
        if name in self.uniforms:
            loc = self.uniforms[name]
        else:
            loc = glGetUniformLocation(self.shaderId, name)
            self.uniforms[name] = loc
        return loc
    
    def setUniformMatrix(self, name, matrix):
        loc = self.getUniformLocation(name)
        glUniformMatrix4fv(loc, 1, GL_FALSE, glm.value_ptr(matrix))