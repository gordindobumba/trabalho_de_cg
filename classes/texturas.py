from PIL import Image
from OpenGL.GL import *

class Textura:
    def __init__(self, fileName):
        img = Image.open(fileName)
        img = img.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        imgData = img.convert('RGBA').tobytes()

        self.texId = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texId)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR_MIPMAP_LINEAR)
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