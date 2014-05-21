#!/usr/bin/env python
# -*- coding: utf-8 -*-

from heapq import heappush, heappop

PESO = 0
RESTO = 1

class Problem(object):
    """docstring for ClassName"""
    def __init__(self, peso, estoque):
        self.estoque = tuple([x for (x, _) in
            sorted(zip(estoque, peso),key=lambda(x): x[1], reverse=True)])
        self.peso = tuple(sorted(peso, reverse=True))
        self.inicial = (0, self.estoque)

    @staticmethod
    def trata_objetivo(novo, peso_novo, melhor, peso_melhor):
        """Retorna o melhor nó entre novo e melhor segundo os ordems do problema."""
        if peso_novo > peso_melhor:
            return novo, peso_novo
        elif peso_novo == peso_melhor and novo.custo < melhor.custo:
            return novo, peso_novo
        return melhor, peso_melhor

    def solucao(self, no, passos):
        """Retorna uma descrição de texto do resultado."""
        resposta = ["O melhor caminho teve custo de %d" % no.custo,
                    "O peso calculado para se coletar foi de %d" % no.estado[PESO],
                    "A busca levou %d passos.\nA sequência de ações é:" % passos]
        acoes = [str(self.estoque[i] - resto) for i, resto in enumerate(no.estado[RESTO])]
        descricao = ["{} do item {} ({} kg)".format(n, i, self.peso[i]) for (i, n) in enumerate(acoes) if n > 0]
        resposta.append("pegar " + ", ".join(descricao))
        return "\n".join(resposta)


class Node(object):
    """docstring for No"""
    def __init__(self, estado, indice, nivel):
        self.estado = estado
        self.indice = indice  # posicao para evitar repetição de estado.
        self.custo = nivel

    def expandir(self, eh_inicial=False):
        # TODO indice/set
        indice = self.indice
        peso = self.estado[PESO]
        resto = self.estado[RESTO]
        return [((peso +  P[x], resto[:x] + (resto[x] - 1,) + resto[x+1:]),
                  x) for x in xrange(indice, N) if resto[x] > 0 and META >= peso + P[x]]


def busca_a_asterisko(problema):
    P = problema.peso
    borda = [ (META/P[-1], Node(problema.inicial, 0, 0))]
    melhor = borda[0][1]
    peso_melhor = 0
    passos = 0
    vistos = set()
    repetidos = 0
    while borda != []:
        atual = heappop(borda)[1]
        #for k in atual.__dict__.keys():
            #print "atual.",k,"=",atual.__dict__[k]
        peso_atual = atual.estado[PESO]
        melhor, peso_melhor = problema.trata_objetivo(atual, peso_atual, melhor, peso_melhor)
        if peso_melhor == META:
            print "========= repetidos: %d" % repetidos
            return melhor, passos
        for estado_sucessor, ipeso_sucessor in atual.expandir():
            if estado_sucessor in vistos:
                repetidos += 1
            else:
                vistos.add(estado_sucessor)
            no_filho = Node(estado_sucessor, ipeso_sucessor, atual.custo + 1)
            h = no_filho.custo + (META - estado_sucessor[PESO]) / P[ipeso_sucessor]
            heappush(borda, (h, no_filho))
            passos += 1
    print "========= repetidos: %d" % repetidos
    return melhor, passos

NOME = "IABCDEF"
META = 287
ESTOQUE = [100, 101, 100, 110, 115, 113]
PESOS = [10, 7, 2, 13, 11, 26]
N = len(ESTOQUE)

# NOME = "IABCDEF"
# META = 25
# ESTOQUE = [2,3,4]
# PESOS = [2,6,4]
# ORDEM = [1, 0, 2, 4, 3, 5]
# N = len(ESTOQUE)

problema = Problem(PESOS, ESTOQUE)
P = problema.peso

if __name__ == "__main__":
    # for k in sol.__dict__.keys():
        # print "sol.",k,"=",sol.__dict__[k]
    print "================="
    print "Resultado da busca A*:"
    print problema.solucao(*busca_a_asterisko(problema))
