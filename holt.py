import csv
import numpy as np
import matplotlib.pyplot as plt

# retorna o valor min e max para legenda x e y no grafico
def extremos(*args):
    if len(args) > 1:
        minimo = maximo = args[0][0]
        for arg in args:
            aux_minimo = min(arg)
            aux_maximo = max(arg)
            if aux_minimo <= minimo :
                minimo = aux_minimo
            if aux_maximo >= maximo :
                maximo = aux_maximo
        return int(minimo), int(maximo)

    else:
        return min(args[0]), max(args[0])

def abre_arquivo(arquivo) :
    aux_Z = []
    with open(arquivo) as csvarquivo:
        dataset = csv.reader(csvarquivo)
        for row in dataset:
            aux_Z.append([row[0], [float(row[1])]])
        return aux_Z

def holtwinters(alpha, beta, dados) :

    Z = [] # vetor q armazena os valores e previsoes
    t = 1  # indice dos valores

    # variaveis para grafico
    y_linha = []
    y2_linha = []
    x_linha = []

    # carrega dados para analise
    Z = abre_arquivo(dados)

    # configura o setup - linha 0
    Z.insert(0, ['setup', ['', Z[0][1][0], Z[1][1][0] - Z[0][1][0]]])

    for t in range(1, len(Z)):
        # calcula l e armazena resultado em Z
        l = alpha * Z[t][1][0] + (1 - alpha) * (Z[t - 1][1][1] + Z[t - 1][1][2])
        Z[t][1].append(l)

        # calculo do b e insere resultado em Z
        b = beta * (Z[t][1][1] - Z[t - 1][1][1]) + (1 - beta) * Z[t - 1][1][2]
        Z[t][1].append(b)

        # calculo da previsao e insere resultado em Z
        y = l + b
        Z[t][1].append(y)

    for i in Z[1:]:
        print(i) # visualizar em tela os valores do vetor Z
        y_linha.append(i[1][0])
        y2_linha.append(i[1][3])
        x_linha.append(int(i[0]))

    # plotar valores no grafico e mostrar na tela
    plt.plot(x_linha, y_linha)
    plt.plot(x_linha, y2_linha)
    plt.grid()

    limY1, limY2 = extremos(y_linha, y2_linha)
    limX1, limX2 = extremos(x_linha)


    plt.yticks(np.arange(limY1 - 1, limY2 + 1))
    plt.xticks(np.arange(limX1 - 1, limX2 + 1))

    plt.show()


holtwinters(0.4, 0.4, 'valores.csv') # valores de alpha, beta e arquivo com os dados
