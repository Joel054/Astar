import pygame
import random
from pygame.locals import *
from sys import exit
import time

from No import *

TELA_W = 600
TELA_H = 600

# inicializa o grid
def createGrid(tam):
    g = []
    for i in range(tam):
        l = []
        for j in range(tam):
            l.append(0)
        g.append(l)
    return g

# Gera obstáculos aleatórios no grid
def geraAleatorio(grid, tam, p):
    g = grid
    for ob in range(int(p * tam * tam)):
        x = random.randint(0, (tam - 1))
        y = random.randint(0, (tam - 1))
        if g[x][y] == 0:
            g[x][y] = 3
    return g

def marcaCaminho(grid, caminho, i, f):
    g = grid
    if caminho:
        for pos in caminho:
            if (pos != i) and (pos != f):
                g[pos[0]][pos[1]] = 4
    return g

# Função para desenho do grid
def drawGrid(grid, surf, tela_w, tela_h):
    n = len(grid)
    for i in range(n):
        for j in range(n):
            if (grid[i][j] == 1):
                pygame.draw.rect(surf, (50, 205, 50), [((tela_w / n) * j), ((tela_h / n) * i), (tela_w / n), (tela_h / n)])
            elif (grid[i][j] == 2):
                pygame.draw.rect(surf, (178, 34, 34), [((tela_w / n) * j), ((tela_h / n) * i), (tela_w / n), (tela_h / n)])
            elif (grid[i][j] == 3):
                pygame.draw.rect(surf, (119, 136, 153), [((tela_w / n) * j), ((tela_h / n) * i), (tela_w / n), (tela_h / n)])
            elif (grid[i][j] == 4):
                pygame.draw.rect(surf, (135, 206, 235), [((tela_w / n) * j), ((tela_h / n) * i), (tela_w / n), (tela_h / n)])
            elif (grid[i][j] == 5):
                pygame.draw.rect(surf, (255, 69, 0), [((tela_w / n) * j), ((tela_h / n) * i), (tela_w / n), (tela_h / n)])
            else:
                pygame.draw.rect(surf, (0, 0, 0), [((tela_w / n) * j), ((tela_h / n) * i), (tela_w / n), (tela_h / n)], 1)

# Retorna False se for borda
def testaBorda(p, tam):
    return ((p[0] >= 0) and (p[0] < tam)) and ((p[1] >= 0) and (p[1] < tam))

# Retorna True se posição for um obstáculo
def testaObstaculo(grid, pos):
    return (grid[pos[0]][pos[1]] == 3)

# Retorna a lista de vizinhos de um nó
def procuraVizinhos(grid, no, tam):
    #print ("no: "+str(no))
    v_orto = [(no.pos[0]-1, no.pos[1]), (no.pos[0], no.pos[1]+1), (no.pos[0]+1, no.pos[1]), (no.pos[0], no.pos[1]-1)]
    v_diag = [(no.pos[0]-1, no.pos[1]+1), (no.pos[0]+1, no.pos[1]+1), (no.pos[0]+1, no.pos[1]-1), (no.pos[0]-1, no.pos[1]-1)]
    vz = v_orto + v_diag
    #print ("vz: "+str(vz))
    vizinhos = []
    for v in vz:
        if (testaBorda(v, tam)): # se não for borda
            if (testaObstaculo(grid, v) is False): # se nao for obstáculo
                nodo = No(v, no)
                vizinhos.append(nodo)
    return vizinhos

caminho = []
# Retorna o caminho encontrado
def retornaCaminho(no):
    #print(str(no.pos))
    caminho.append(no.pos)
    # se o nó possui um pai chama a função recursivamente com o pai
    if (no.no_pai is not None):
        retornaCaminho(no.no_pai)


# função que faz a busca A*
def A_star(grid, no_ini, no_fim, tam):
    ini = time.time()
    # definicao das duas filas: nós abertos e nós fechados
    filaAbertos = FilaHeap()
    filaFechados = []

    filaAbertos.insere(no_ini.H, no_ini) #adiciona o nó inicial na fila de abertos
    cont = 0

    while filaAbertos.vazia() is False:
        no = filaAbertos.remove() #retira da fila o elemento com menor custo f

        fim = time.time()

        if int(fim-ini) > 30:
            print("Tempo de processamento esgotado!")

            return
        if (no.pos == no_fim.pos): # se o no verificado atualmente foro o nó final finaliza e retorna o caminho
            retornaCaminho(no)
            return caminho
        else:
            if filaFechados:
                no.H += filaFechados[-1].H
            filaFechados.append(no)
            vizinhos = procuraVizinhos(grid, no, tam) # captura a lista de vizinhos alcançáveis

            for v in vizinhos: # para cada vizinho alcançável, faça:
                if (filaAbertos.busca(v) == False) and ((v.H, v) not in filaFechados):
                    v.atualizaNo(no, no_fim)
                    filaAbertos.insere(v.H, v)


        grid[no.pos[0]][no.pos[1]] = 5
        surface.fill((255, 255, 255))
        drawGrid(grid, surface, TELA_W, TELA_H)
        pygame.display.update()
        grid[no.pos[0]][no.pos[1]] = 0
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
        # define fps
        pygame.time.Clock().tick(10)


tam = 50

p_ini = (0, 0)
p_fim = (tam-1, tam-1)

no_final = No(p_fim)
no_inicial = No(p_ini)
no_inicial.calcHeuristica(no_final)


grid = createGrid(tam)
grid = geraAleatorio(grid, tam, 0.40)

grid[no_inicial.pos[0]][no_inicial.pos[1]] = 1
grid[no_final.pos[0]][no_final.pos[1]] = 2



pygame.init()
surface = pygame.display.set_mode((TELA_W, TELA_H), 0, 32)
pygame.display.set_caption('Busca A*')

grid = marcaCaminho(grid, A_star(grid, no_inicial, no_final, tam), no_inicial.pos, no_final.pos)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
    surface.fill((255, 255, 255))
    #grid = marcaCaminho(grid, A_star(grid, no_inicial, no_final, tam), no_inicial.pos, no_final.pos)
    # desenha grid
    drawGrid(grid, surface, TELA_W, TELA_H)
    pygame.display.update()

    # define fps
    pygame.time.Clock().tick(60)






#
