#!/usr/bin/env python
# -*- coding: utf-8 -*-
from random import shuffle


class Problem(object):
    """Problema representa """
    def __init__(self, meta, criterio, peso, estoque, tipo):
        self.meta = meta
        self.peso = [0] + peso
        self.inicial = No(0, 1, None, 0)
        self.estoque = [0] + estoque
        self.criterio = [0] + [x + 1 for x in criterio]  # criterio para ordem de visita de nó filho
        self.criterio.append(None)
        self.memo = [meta+1] * meta
        self.melhor = self.inicial
        self.melhor_precisao = 0
        self.tipo = tipo

    def trata_objetivo(self, no, peso_total):
        """Atualiza o melhor candidato. Retorna True se é pra finalizar busca."""
        nova_precisao = peso_total  # quão perto chegou da capacidade
        if (peso_total == self.meta) and (self.tipo == "a*"):
            return True
        if nova_precisao > self.melhor_precisao:
            self.melhor = no  # medida de desempenho primária é se chega no alvo
            self.melhor_precisao = nova_precisao
        elif nova_precisao == self.melhor_precisao:
            if no.custo < self.melhor.custo: # segundo objetivo é o custo em passos
                self.melhor = no
                self.melhor_precisao = nova_precisao
        return False

    def solucao(self):
        no = self.melhor
        acoes = [0] * (len(self.criterio) - 1)
        peso = self.melhor_precisao
        resposta = "O melhor caminho teve custo {}, o peso calculado para se coletar foi de {}".format(no.custo, peso)

        while no != self.inicial:
            acoes[no.estado] += 1
            no = no.pai
        acoes = ["{} de {} ({} kilos)".format(n, i, self.peso[i]) for (i, n) in enumerate(acoes) if n > 0]
        return "{}. A sequencia do objetivo é: pegar {}.".format(resposta, ", ".join(acoes))

    def __str__(self):
        val_vars = [self.meta, self.peso, self.inicial, self.estoque,
            self.criterio, self.melhor, self.melhor_precisao]
        n_vars = ["meta", "peso", "inicial", "estoque",
            "criterio", "melhor", "melhor_precisao"]
        var_list = [": ".join(map(str, [x, y])) for x, y in zip(n_vars, val_vars)]
        return "\n".join(var_list)


class No(object):
    """Class da nó da arvore de busca"""
    def __init__(self, indice_item, link, pai, custo):
        self.estado = indice_item  # Indice do item em problema.peso e problema.estoque do objeto candidato
        self.pai = pai
        self.custo = custo
        self.eh_folha = True  # a principio é folha, caso tenha filho valido, deixa de ser
        self.prox = link

    def __str__(self):
        return "{}".format(self.estado)

def dfs(problema, criterio, para_na_solucao=False):
    """Retorna uma solução de menor custo dado uma especificação de problema.

    :param problema: A especificação com estado inicial, estoque, ...
    :param para_na_solucao: se deve-se para na primeira solução
    :param criterio: representa uma função de avaliação ou não (se for randomico).

    """
    pilha = [problema.inicial]
    peso_atual = 0
    melhor = problema.inicial  # nó com peso mais próximo à meta e de menor custo

    while pilha != []:
        atual = pilha[-1]

        if criterio[atual.prox] is None:  # nó atual foi explorado por completo
            if atual.eh_folha:
                problem.trata_objetivo(atual, peso_atual, para_na_solucao):
                if problem
                    break
                # atual é nó folha, nó interno não precisa tratar, nunca é ótimo
            peso_atual -= problema.peso[atual.estado]
            if atual.estado != 0:
                problema.estoque[atual.estado] += 1
            pilha.pop()
        else:
            while (criterio[atual.prox_filho] is not None): # pega o prox no filho valido
                peso_filho = peso_atual + problema.peso[criterio[atual.prox_filho]]
                if (peso_filho < problema.meta) and (atual.custo + 1 < memo[peso_filho]):
                    break
                atual.prox_filho += 1 # pega o arco/link pro próximo filho válido

            # atual.prox agora é o proximo filho segundo CRITERIO ou acabou os filhos
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
