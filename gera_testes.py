meta = 25  # o peso maximo da mochila
amostra_teste = = [12, 22, 13]  # tem 3 tipos de item
pesos = [10, 7, 1]  # sempre coloque em ordem decrescente de peso
pesos_teste

def custo(meta , items):
    """Retorna o menor numero de itens que enche a mochila."""
    pilha = [ ]
    tabela = []  # para "memoização"
    melhor = [ ]
