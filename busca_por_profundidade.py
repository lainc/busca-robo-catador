#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Problem(object):
    """Problema representa uma especificação do problema e dos estados mantidos."""
    def __init__(self, meta, ordem, peso, estoque):
        self.meta = meta
        self.peso = [0] + peso
        self.inicial = No(0, 1, None, 0)
        self.estoque = [0] + estoque
        self.ordem = [0] + [x + 1 for x in ordem] + [None]  #  ordem de visita de nó filho

    @staticmethod
    def trata_objetivo(novo, peso_novo, melhor, peso_melhor):
        """Retorna o melhor nó entre novo e melhor segundo os ordems do problema."""
        if peso_novo > peso_melhor:
            return novo, peso_novo
        elif peso_novo == peso_melhor and novo.custo < melhor.custo:
            return novo, peso_novo
        return melhor, peso_melhor

    def solucao(self, no, peso_alcancado, passos):
        """Retorna uma descrição de texto do resultado."""
        resposta = ["O melhor caminho teve custo de %d" % no.custo,
                    "O peso calculado para se coletar foi de %d" % peso_alcancado,
                    "A busca levou %d passos.\nA sequência de ações é:" % passos]
        acoes = [0] * (len(self.ordem) - 1)
        while no != self.inicial:
            acoes[no.estado] += 1
            no = no.pai
        descricao = ["{} do item {} ({} kg)".format(n, i, self.peso[i]) for (i, n) in enumerate(acoes) if n > 0]
        resposta.append("pegar " + ", ".join(descricao))
        return "\n".join(resposta)

    def __str__(self):
        val_vars = [self.meta, self.peso, self.inicial, self.estoque, self.ordem]
        n_vars = ["meta", "peso", "inicial", "estoque", "ordem"]
        var_list = [": ".join(map(str, [x, y])) for x, y in zip(n_vars, val_vars)]
        return "\n".join(var_list)


class No(object):
    """Classe do nó da arvore de busca"""
    def __init__(self, indice_item, link, pai, custo):
        self.estado = indice_item  # Indice do item em problema.peso e problema.estoque do objeto candidato.
        self.pai = pai
        self.custo = custo
        self.eh_folha = True  # A principio é folha, caso tenha filho valido, deixa de ser.
        self.prox_filho = link

    def __str__(self):
        return str(self.estado)

INICIAL = 1

def _dfs(problema, ordem, para_na_solucao=False):
    """
    Retorna uma solução de menor custo dado uma especificação de problema.

    problema: A especificação com estado inicial, estoque, etc.
    para_na_solucao: se deve-se parar na primeira solução encontrada.
    ordem: representa uma função de avaliação ou sem heuristica (se for randomico).

    """
    pilha = [problema.inicial]
    melhor = problema.inicial                   # O nó com peso mais próximo à meta e de menor custo...
    peso_melhor = 0                             # E o peso alcançado nesse nó.
    peso_atual = 0
    #memo = [problema.meta+1] * problema.meta    # Para memoização.
    passos = 0                                  # Para contar e comparar os 2 algoritmos.

    while pilha != []:
        atual = pilha[-1]

        if ordem[atual.prox_filho] is None:
            # O nó atual foi explorado por completo.
            if atual.eh_folha:
                # so precisa checar objetivo nas folhas
                melhor, peso_melhor = problema.trata_objetivo(atual, peso_atual, melhor, peso_melhor)
                if para_na_solucao and peso_melhor == problema.meta:
                    return problema.solucao(melhor, peso_melhor, passos)
            peso_atual -= problema.peso[atual.estado]
            if atual.estado != INICIAL:
                problema.estoque[atual.estado] += 1
            del pilha[-1]
        else:
            # Ainda tem estados sucessores para expandir / nós filhos para visitar.
            while (ordem[atual.prox_filho] is not None):
                # Encontra proximo no filho valido, i.e. soma do peso < meta,
                # e sem caminho de mesmo peso e menor custo.
                peso_filho = peso_atual + problema.peso[ordem[atual.prox_filho]]
                if (peso_filho < problema.meta): #and (atual.custo + 1 <= memo[peso_filho]):
                    break
                atual.prox_filho += 1

            # Atual.prox agora é o proximo filho segundo ordem ou acabou os filhos.
            if ordem[atual.prox_filho] is not None:
                item = ordem[atual.prox_filho]
                novo = No(item, atual.prox_filho, atual, atual.custo + 1)
                peso_atual += problema.peso[item]
                # if novo.custo < memo[peso_atual]:
                #     memo[peso_atual] = novo.custo
                problema.estoque[item] -= 1
                if problema.estoque[item] == 0:
                    novo.prox_filho += 1  # o próximo item é o mesmo do anterior a menos que acabe o estoque
                pilha.append(novo)
                atual.eh_folha = False  # teve filho
                atual.prox_filho += 1
                passos += 1
        # end while
    return melhor, peso_melhor, passos

def busca_em_profundidade(meta, ordem, peso, estoque):
    """
    Retorna uma solução de menor custo paro o problema.

    para_na_solucao: se deve-se para na primeira solução
    ordem: representa uma função de avaliação ou não (se for randomico).
    peso: uma lista de pesos dos objetos.
    estoque: listo de quantidades dos objetos.
    """
    problema = Problem(meta, ordem, peso, estoque)
    return problema.solucao(*_dfs(problema, problema.ordem))

def busca_gulosa_pela_melhor_escolha(meta, ordem, peso, estoque):
     """
     Retorna uma solução de menor custo paro o problema.

     para_na_solucao: se deve-se para na primeira solução
     ordem: representa uma função de avaliação ou não (se for randomico).
     peso: uma lista de pesos dos objetos.
     estoque: listo de quantidades dos objetos.
     """
     ordem = sorted([(i, v) for i, v in enumerate(peso)], key=lambda x: x[1], reverse=True)
     ordem = [x for x, _ in ordem]
     problema = Problem(meta, ordem, peso, estoque)
     return problema.solucao(*_dfs(problema, problema.ordem, True))

if __name__ == "__main__":
    NOME = "IABCDEF"
    META = 287
    ESTOQUE = [100, 101, 100, 110, 115, 113]
    PESO = [10, 7, 2, 13, 11, 26]
    ORDEM = [1, 0, 2, 4, 3, 5]

    print "capacidade do robô de %d quilogramas" % META
    print "objetos para levar são esses:\n\n(codigo, peso, estoque)"
    print "\n".join(" ".join([str(x), str(y), str(z)]) for x, y, z in zip(xrange(len(ESTOQUE)), PESO, ESTOQUE))
    print "================="
    print "Resultado da busca em profundidade:"
    print busca_em_profundidade(META, ORDEM, PESO, ESTOQUE)
