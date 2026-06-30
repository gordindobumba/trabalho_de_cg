from OpenGL.GL import *

class Combate:
    def __init__(self, personagens, matrix):
        self.matrix = matrix
        self.personagens = personagens
        self.vida_torres = {}
        self.iniciar_torres()
    
    def iniciar_torres(self):
        for i in range(8):
            for j in range(8):
                if self.matrix[i][j] == 2:
                    self.vida_torres[(i, j)] = 3
    
    def opcoes_ataque(self, l, c, personagem_tipo):
        celulas_ataque = []
        vizinhos = [(l + 1, c), (l - 1, c), (l, c + 1), (l, c - 1)]
        
        # vamos visitar todos os vizinhos de uma celula.
        # se puder atacar algum deles, iremos colocar a posição do vizinho em um vetor.
        for i, j in vizinhos:
            if 0 <= i < 8 and 0 <= j < 8:
                if personagem_tipo == "medico" and self.matrix[i][j] == 4:
                    celulas_ataque.append((i, j))
                elif personagem_tipo == "virus" and self.matrix[i][j] == 2:
                    celulas_ataque.append((i, j))
        return celulas_ataque

    def atacar(self, personagem, alvo_i, alvo_j, movimento):
        tipo = personagem["tipo"]
        
        if tipo == "medico":
            alvo = None
            for p in self.personagens:
                if p["linha"] == alvo_i and p["coluna"] == alvo_j and p["tipo"] == "virus":
                    alvo = p
                    break
        
            if alvo != None:
                alvo["vida"] -= 1
                
                # o empurro será para uma célula vizinha, logo fica fácil calcular o deslocamento.
                empurro_i = alvo_i + (alvo_i - personagem["linha"])
                empurro_j = alvo_j + (alvo_j - personagem["coluna"])
                
                if 0 <= empurro_i < 8 and 0 <= empurro_j < 8 and self.matrix[empurro_i][empurro_j] == 0:
                    self.matrix[alvo_i][alvo_j] = 0
                    x1, y1 = movimento.coordenadas_float(alvo_i, alvo_j)
                    x2, y2 = movimento.coordenadas_float(empurro_i, empurro_j)
                    alvo["animacao"].iniciar(x1, y1, x2, y2)
                    
                    alvo["linha"] = empurro_i
                    alvo["coluna"] = empurro_j
                    self.matrix[empurro_i][empurro_j] = 4
                
                if alvo["vida"] == 0:
                    self.matrix[alvo["linha"]][alvo["coluna"]] = 0
                    self.personagens.remove(alvo)
            
        elif tipo == "virus":
            coord_torre = (alvo_i, alvo_j)
            if coord_torre in self.vida_torres:
                self.vida_torres[coord_torre] -= 1
                
                if self.vida_torres[coord_torre] == 0:
                    self.matrix[alvo_i][alvo_j] = 0
                    del self.vida_torres[coord_torre]