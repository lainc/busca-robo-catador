#!/usr/bin/env python
# -*- coding: utf-8 -*-

#import random

#PESO = (1, 5, 10, 25, 50, 100)
#ESTOQUE = (20, 10, 15, 20, 10)
#PESO = (80, 16, 40, 26, 50)
#ESTOQUE = (4, 10, 15, 20, 10)
PESO = [2, 6, 10]
ESTOQUE = [15, 20, 10]
NOMES = "ABCI"
CRITERIO = [0, 1, 2]
META = 101

# TODO : botar nomes conforme nos slides.

class Problem(object):
    """docstring for problem"""
# TODO botar docstrings
    def __init__(self, meta, criterio, peso, estoque):
        self.meta = meta
        self.peso = [0] + peso
        self.inicial = No(0, 0, None, 0)
        self.estoque = [1] + estoque
        self.criterio = [0] + [ x + 1 for x in criterio ]  # criterio para ordem de visita de nó filho
        self.criterio.append(None)
        self.melhor = self.inicial
        self.melhor_precisao = 0

        # TODO variaveis globais?

    def trata_objetivo(self, no, peso_total):
        """Atualiza o melhor candidato."""
        nova_precisao = peso_total  # quão perto chegou da capacidade
        if nova_precisao > self.melhor_precisao:
            self.melhor = no  # medida de desempenho primária é se chega no alvo
            self.melhor_precisao = nova_precisao
        elif nova_precisao == self.melhor_precisao:
            if no.custo < self.melhor.custo: # segundo objetivo é o custo em passos
                self.melhor = no
                self.melhor_precisao = nova_precisao

    def solucao(self):
        no = self.melhor
        acoes = []
        peso = self.melhor_precisao
        resposta = "O melhor caminho teve custo {}, o peso calculado para coletar foi de {}".format(no.custo, peso)
        while no != self.inicial:
            acoes.append("pegar item {}".format(no.estado))
            no = no.pai
        return "{}. A sequencia que leva ao objetivo é: {}.".format(resposta, ", ".join(acoes))

    def __str__(self):
        val_vars = [
            self.meta, self.peso, self.inicial, self.estoque,
            self.criterio, self.melhor, self.melhor_precisao ]
        n_vars = [
            "meta", "peso", "inicial", "estoque",
            "criterio", "melhor", "melhor_precisao" ]
        return "\n".join([": ".join(map(str, [x, y])) for x, y in zip(n_vars, val_vars)])


class No(object):
    """Class da nó da arvore de busca"""
    def __init__(self, indice_item, link, pai, custo):
        self.estado = indice_item  # Indice do item em problema.peso e problema.estoque do objeto candidato
        self.pai = pai
        self.custo = custo
        self.eh_folha = True  # a principio é folha, caso tenha filho valido, deixa de ser
        self.prox = link

    def __str__(self):
        return "{} -> {}".format(self.estado, self.prox)


def dfs(problema):
    """Retorna uma solução de menor custo, dado um Problema problema"""
    peso = problema.peso
    criterio = problema.criterio
    pilha = [problema.inicial]
    peso_atual = 0
    print problema

    while pilha != []:
        atual = pilha[-1]
        #print "no", atual.estado
        if criterio[atual.prox] is None:  # nó atual foi explorado por completo
            if atual.eh_folha:
                problema.trata_objetivo(atual, peso_atual)
                # atual é nó folha, nó interno não precisa tratar, nunca é ótimo
            peso_atual -= peso[atual.estado]
            problema.estoque[atual.estado] += 1
            del pilha[-1]
        else:
            while (criterio[atual.prox] is not None) and \
                  (peso_atual + peso[criterio[atual.prox]] > problema.meta):
                atual.prox += 1 # pega o arco/link pro próximo filho válido
            # atual.prox agora é o proximo filho segundo CRITERIO ou acabou os filhos
            if criterio[atual.prox] is not None:
                item = criterio[atual.prox]
                atual.eh_folha = False  # teve filho
                novo = No(item, atual.prox, atual, atual.custo + 1)
                atual.prox += 1
                peso_atual += peso[item]
                problema.estoque[item] -= 1
                if problema.estoque[item] == 0:
                    novo.prox += 1  # o próximo item a pegar é o mesmo do anterior a não ser que acabe o estoque
                pilha.append(novo)
                #print atual

def busca_em_profundidade():
    pass

if __name__ == "__main__":
    problema = Problem(META, CRITERIO, PESO, ESTOQUE)
    dfs(problema)
    print "capacidade do robô de {} kilos, criterio {}".format(META, ", ".join(map(str, CRITERIO)))
    print "objetos para levar são esses:\n(codigo, peso, estoque)"
    print "\n".join(" ".join([str(x), str(y), str(z)]) for x, y, z in zip(xrange(len(ESTOQUE)), PESO, ESTOQUE))
    print problema.solucao()
