# Classe que simula uma heap, em que a tupla (F, Item) com o menor F está sempre no inicio
class FilaHeap:
    def __init__(self):
        self.elementos = []

    def vazia(self):
        return (len(self.elementos) == 0)

    def insere(self, f, item):
        self.elementos.append((f, item))
        self.elementos.sort(key=lambda x: x[0])

    def remove(self):
        return self.elementos.pop(0)[1]

    def busca(self, item):
        return ((item.F, item) in self.elementos)

class No(object):
    def __init__(self, pos, no_pai=None):
        self.pos = pos # tupla (pos_x, pos_y)
        self.no_pai = no_pai
        self.H = 0
        self.G = 0
        self.F = 0
        self.vizinhos = []

    # Cálculo do F
    def calcF(self):
        return (self.H + self.G)

    # Cálculo da heurística
    def calcHeuristica(self, no, no_fim):
        return ((abs(no.pos[0] - no_fim.pos[0]) + abs(no.pos[1] - no_fim.pos[1]) * 10)) # multiplicação por 10 pra melhor vizualização apenas

    # Recalcula valores para o nó e atribui para ele um nó pai
    def atualizaNo(self, no, no_fim):
        self.G = no.G + 10
        self.H = self.calcHeuristica(self, no_fim)
        self.F = self.calcF()
        self.no_pai = no

    def __str__(self):
        return(str(self.pos))







#
