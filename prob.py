#!/usr/bin/env python
# -*- coding: utf-8 -*-
from random import shuffle


class Problem(object):
    """Problema representa uma especificação do problema e dos estados mantidos."""
    def __init__(self, meta, criterio, peso, estoque, tipo):
        self.meta = meta
        self.peso = [0] + peso
        self.inicial = No(0, 1, None, 0)
        self.estoque = [0] + estoque
        self.criterio = [0] + [x + 1 for x in criterio]  # criterio para ordem de visita de nó filho
        self.criterio.append(None)

    @staticmethod
    def trata_objetivo(novo, peso_novo, melhor, peso_melhor):
        """Retorna o melhor nó entre novo e melhor segundo os criterios do problema."""
        if peso_novo > peso_melhor:
            return novo, peso_novo
        elif peso_novo == peso_melhor and novo.custo < melhor.custo:
            return novo, peso_novo
        return melhor, peso_melhor

    def solucao(self):
        """Retorna uma descrição de texto do resultado."""
        no = self.melhor
        acoes = [0] * (len(self.criterio) - 1)
        peso = self.melhor_precisao
        resposta = "O melhor caminho teve custo"
        "{}, o peso calculado para se coletar foi de {}".format(no.custo, peso)
        while no != self.inicial:
            acoes[no.estado] += 1
            no = no.pai
        acoes = ["{} de {} ({} kilos)".format(n, i, self.peso[i]) for (i, n) in enumerate(acoes) if n > 0]
        return "{}. A sequencia do objetivo é: pegar {}.".format(resposta, ", ".join(acoes))

    def __str__(self):
        val_vars = [self.meta, self.peso, self.inicial, self.estoque, self.criterio]
        n_vars = ["meta", "peso", "inicial", "estoque", "criterio"]
        var_list = [": ".join(map(str, [x, y])) for x, y in zip(n_vars, val_vars)]
        return "\n".join(var_list)


class No(object):
    """Class da nó da arvore de busca"""
    def __init__(self, indice_item, link, pai, custo):
        self.estado = indice_item  # Indice do item em problema.peso e problema.estoque do objeto candidato.
        self.pai = pai
        self.custo = custo
        self.eh_folha = True  # A principio é folha, caso tenha filho valido, deixa de ser.
        self.prox = link

    def __str__(self):
        return "{}".format(self.estado)

INICIAL = 1

def dfs(problema, criterio, para_na_solucao=False):
    """Retorna uma solução de menor custo dado uma especificação de problema.

    :param problema: A especificação com estado inicial, estoque, ...
    :param para_na_solucao: se deve-se para na primeira solução
    :param criterio: representa uma função de avaliação ou não (se for randomico).

    """
    pilha = [problema.inicial]
    melhor = problema.inicial    # O nó com peso mais próximo à meta e de menor custo...
    peso_melhor = 0              # e o peso alcançado nesse nó.
    peso_atual = 0
    memo = [problema.meta+1] * problema.meta    # para memoização.

    while pilha != []:
        atual = pilha[-1]

        if criterio[atual.prox_filho] is None:
            # O nó atual foi explorado por completo.
            if atual.eh_folha:
                # so precisa checar objetivo nas folhas
                melhor, peso_melhor = problema.trata_objetivo(atual, peso_atual, melhor, peso_melhor)
                if para_no_melhor and peso_do_melhor == problema.meta:
                    return problema.solucao(melhor)

            peso_atual -= problema.peso[atual.estado]
            if atual.estado != INICIAL:
                problema.estoque[atual.estado] += 1
            del pilha[-1]
        else:
            # ainda tem estados sucessores para expandir / nós filhos para visitar.
            while (criterio[atual.prox_filho] is not None):
                # encontra proximo no filho valido, i.e. soma do peso < meta,
                # e sem caminho de mesmo peso e menor custo.
                peso_filho = peso_atual + problema.peso[criterio[atual.prox_filho]]
                if (peso_filho < problema.meta) and (atual.custo + 1 < memo[peso_filho]):
                    break
                atual.prox_filho += 1

            # atual.prox agora é o proximo filho segundo CRITERIO ou acabou os filhos.
            if criterio[atual.prox_filho] is not None:
                item = criterio[atual.prox_filho]
                atual.eh_folha = False  # teve filho
                novo = No(item, atual.prox_filho, atual, atual.custo + 1)
                atual.prox += 1
                peso_atual += problema.peso[item]
                if novo.custo < memo[peso_atual]:
                    memo[peso_atual] = novo.custo
                problema.estoque[item] -= 1
                if problema.estoque[item] == 0:
                    novo.prox += 1  # o próximo item é o mesmo do anterior a menos que acabe o estoque
                pilha.append(novo)
                #print atual

def busca_em_profundidade(meta, criterio, peso, estoque):
    shuffle(criterio)
    problema = Problem(meta, criterio, peso, estoque, "profundidade")
    dfs(problema)
    return problema.solucao()

def busca_a_asterisco(meta, criterio, peso, estoque):
    criterio = sorted([(i, v) for i, v in enumerate(peso)], key=lambda x: x[1])
    criterio = reversed([x[0] for x in criterio])
    problema = Problem(META, criterio, PESO, ESTOQUE, "a*")
    dfs(problema)
    return problema.solucao()

META = 4137
ESTOQUE = [100, 101, 100, 110, 115, 113]
PESO = [10, 7, 2, 13, 11, 26]
NOME = "IABCDEF"
CRITERIO = [1, 0, 2, 4, 3, 5]

if __name__ == "__main__":
    print "capacidade do robô de %d kilos" % META
    print "objetos para levar são esses:\n\n(codigo, peso, estoque)"
    print "\n".join(" ".join([str(x), str(y), str(z)]) for x, y, z in zip(xrange(len(ESTOQUE)), PESO, ESTOQUE))
    print "================="
    print "pela busca em profundidade:"
    print busca_em_profundidade(META, CRITERIO, PESO, ESTOQUE)
    print "================="
    print "Pela busca A*:"
    print busca_a_asterisco(META, CRITERIO, PESO, ESTOQUE)
