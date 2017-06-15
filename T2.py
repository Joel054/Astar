import pygame
import random
from pygame.locals import *
from sys import exit

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
    for l in range(tam):
        x = random.sample(range(0, tam), int(tam * p))
        for c in range(len(x)):
            if (g[l][x[c]] == 0):
                g[l][x[c]] = 3
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
            else:
                pygame.draw.rect(surf, (0, 0, 0), [((tela_w / n) * j), ((tela_h / n) * i), (tela_w / n), (tela_h / n)], 1)

# Retorna False se for borda
def testaBorda(p, tam):
    #print(str(p) + " tam: " +str(tam))
    return ((p[0] >= 0) and (p[0] < tam)) and ((p[1] >= 0) and (p[1] < tam))

# Retorna True se posição for um obstáculo
def testaObstaculo(grid, pos):
    return (grid[pos[0]][pos[1]] == 3)

# Retorna a lista de vizinhos de um nó
def procuraVizinhos(grid, no, tam):
    #print ("no: "+str(no))
    vz = [(no.pos[0]-1, no.pos[1]), (no.pos[0], no.pos[1]+1), (no.pos[0]+1, no.pos[1]), (no.pos[0], no.pos[1]-1)]
    #print ("vz: "+str(vz))
    vizinhos = []
    for v in vz:
        if (testaBorda(v, tam)): # se não for borda
            if (testaObstaculo(grid, v) is False): # se nao for obstáculo
                nodo = No(v, no)
                vizinhos.append(nodo)
    return vizinhos

# Retorna o caminho encontrado
def retornaCaminho(no_ini, no_fim):
    final = no_fim
    caminho = [(final.pos)]
    while final.no_pai is not no_ini:
        final = final.no_pai
        caminho.append(final.pos)

    caminho.append(no_ini.pos)
    caminho.reverse() #inverte para que se tenha caminho do inicio para o fim
    return caminho

# função que faz a busca A*
def A_star(grid, no_ini, no_fim, tam):
    # definicao das duas filas: nós abertos e nós fechados
    filaAbertos = FilaHeap()
    filaFechados = []

    filaAbertos.insere(no_ini.F, no_ini) #adiciona o nó inicial na fila de abertos
    cont = 0
    while filaAbertos.vazia() is False:
        no = filaAbertos.remove() # remove o elemento com F mais baixo da fila de abertos
        filaFechados.append(no) # adiciona nó removido da fila de abertos para a fila de fechados

        if (no is no_fim): # se o no verificado atualmente foro o nó final finaliza e retorna o caminho
            return retornaCaminho(no_ini, no_fim)

        vizinhos = procuraVizinhos(grid, no, tam) # captura a lista de vizinhos alcançáveis

        ##### prints abaixo são apenas para debug
        print ("filaFechados: "+str(len(filaFechados)))
        for w in filaFechados:
            print(str(w.pos))

        print ("filaAbertos: "+str(len(filaAbertos.elementos)))
        for z in filaAbertos.elementos:
            print(str(z[0])+" - "+str(z[1].pos))

        for x in vizinhos:
            print("no: "+str(no.pos) + "vizinhos: " +str(x.pos))
        ################

        for v in vizinhos: # para cada vizinho alcançável, faça:
            if v not in filaFechados: # se o nó vizinho não estiver na fila de fechados, então
                if filaAbertos.busca(v): # testa se o vizinho está na lista de abertos
                    if v.G > (no.G + 10): # testa se o G do vizinho sendo verificado é maior que o G do nó, se for atualiza os valores do nó
                        v.atualizaNo(no, no_fim)
                else: # se o vizinho n estiver na fila de abertos então atualiza o vizinho e insere ele na fila de abertos
                    v.atualizaNo(no, no_fim)
                    filaAbertos.insere(v.F, v)

        # contador para testes, para evitar o loop infinito
        cont +=1
        if cont == 10:
            break


tam = 10

p_ini = (0, 0)
p_fim = (tam-1, tam-1)

no_inicial = No(p_ini)
no_final = No(p_fim)

grid = createGrid(tam)
grid = geraAleatorio(grid, tam, 0.2)

grid[no_inicial.pos[0]][no_inicial.pos[1]] = 1
grid[no_final.pos[0]][no_final.pos[1]] = 2
'''
for l in grid:
    print(l)
'''
print(A_star(grid, no_inicial, no_final, tam))

pygame.init()
surface = pygame.display.set_mode((TELA_W, TELA_H), 0, 32)
pygame.display.set_caption('Busca heurística - A*')

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
    surface.fill((255, 255, 255))

    # desenha grid
    drawGrid(grid, surface, TELA_W, TELA_H)

    pygame.display.update()

    # define fps
    pygame.time.Clock().tick(60)






#
