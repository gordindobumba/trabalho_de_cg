from PIL import Image
from OpenGL.GL import *
import os

class Textura:
    def __init__(self, fileFolder, fileName):
        path = os.path.dirname(os.path.abspath(__file__))
        filePath = os.path.abspath(os.path.join(path, '..', 'texturas', fileFolder, fileName))
        img = Image.open(filePath)
        img = img.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        imgData = img.convert('RGBA').tobytes()

        self.texId = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texId)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexImage2D(GL_TEXTURE_2D,
                     0,
                     GL_RGBA,
                     img.width,
                     img.height,
                     0,
                     GL_RGBA,
                     GL_UNSIGNED_BYTE,
                     imgData)
        glGenerateMipmap(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, 0)
    
    def bind(self, texNumber = 0):
        glActiveTexture(GL_TEXTURE0 + texNumber)
        glBindTexture(GL_TEXTURE_2D, self.texId)