from math import sqrt

# Classe que simula uma heap, em que a tupla (F, Item) com o menor F está sempre no inicio
class FilaHeap:
    def __init__(self):
        self.elementos = []

    def vazia(self):
        return (len(self.elementos) == 0)

    def insere(self, h, item):
        self.elementos.append((h, item))

    def remove(self):
        v = min(self.elementos, key = lambda t: t[0])
        self.elementos.remove(v)
        return v[1]

    def busca(self, item):
        return ((item.H, item) in self.elementos)

class No(object):
    def __init__(self, pos, no_pai=None):
        self.pos = pos # tupla (pos_x, pos_y)
        self.no_pai = no_pai
        self.H = 0 # CUSTO Heuristica

        self.G = 0
        self.F = 0
        self.vizinhos = []

    # Cálculo do F
    def calcF(self):
        return (self.H + self.G)

    # Cálculo da heurística manhattan
    def calcHeuristica(self, no_fim):
        self.H += sqrt((pow(no_fim.pos[0] - self.pos[0], 2)) + (pow(no_fim.pos[1] - self.pos[1], 2)))
        #self.H += abs(self.pos[0] - no_fim.pos[0]) + abs(self.pos[1] - no_fim.pos[1]) # multiplicação por 10 pra melhor vizualização apenas

    # Recalcula valores para o nó e atribui para ele um nó pai
    def atualizaNo(self, no, no_fim):
        #self.G = no.G + 10
        self.calcHeuristica(no_fim)
        #self.F = self.calcF()
        self.no_pai = no

    def __str__(self):
        return(str(self.pos))







#
