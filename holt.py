# ******* Python versao 3.6.1 *********
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
    aux_z = []
    with open(arquivo) as csvarquivo:
        dataset = csv.reader(csvarquivo)
        for row in dataset:
            aux_z.append([row[0], [float(row[1])]])
        return aux_z


def holt(alpha, beta, dados, h):

    z = []  # vetor q armazena os valores e previsoes
    t = 1  # indice dos valores

    # variaveis para grafico
    y_linha = []
    y2_linha = []
    x_linha = []

    # carrega dados para analise
    z = abre_arquivo(dados)

    # configura o setup - linha 0
    z.insert(0, ['setup', ['', z[0][1][0], z[1][1][0] - z[0][1][0]]])

    mae = 0
    mape = 0
    for t in range(1, len(z)):
        # calcula l e armazena resultado em Z
        l = alpha * z[t][1][0] + (1 - alpha) * (z[t - 1][1][1] + z[t - 1][1][2])
        z[t][1].append(l)

        # calculo do b e insere resultado em Z
        b = beta * (z[t][1][1] - z[t - 1][1][1]) + (1 - beta) * z[t - 1][1][2]
        z[t][1].append(b)

        # calculo valor previsto e insere resultado em z
        y = l + b

        z[t][1].append(y)

        mae = y - z[t][1][0] + mae
        mape = ((y - z[t][1][0]) / z[t][1][0]) * 100 + mape

    forecast = []
    aux_forecast = z[-1]
    forecast.append(aux_forecast[1][1] + aux_forecast[1][2])  # formula calculo previsao y = l + hb para h = 1
    for i in range(1, h):
        forecast.append(forecast[-1] + aux_forecast[1][2])  # formula calculo previsao y = l + hb para h = 1

    for i in z[1:]:
        print(i)  # visualizar em tela os valores do vetor z
        y_linha.append(i[1][0])
        y2_linha.append(i[1][3])
        x_linha.append(int(i[0]))


    # calculo do MAE e MAPE
    mae = mae / (len(z) -1)
    mape = mape / (len(z)-1)
    print(mape, mae)

    # plotar valores no grafico e mostrar grafico na tela
    plt.plot(x_linha, y_linha, label='observados')
    plt.plot(x_linha, y2_linha, 'ro', label='previstos')
    plt.legend()
    plt.title('Holt Exponencial Simples')
    plt.grid()

    plt.figtext(0.20, 0.035, 'Previsoes : ', backgroundcolor='blue', color='white', weight='roman', size='x-small')
    plt.figtext(0.30, 0.035, '   '.join(str(round(x, 2)) for x in forecast), backgroundcolor='blue', color='white',
                weight='roman', size='x-small')
    plt.figtext(0.60, 0.035, 'MAPE : '+str(round(mape, 2))+'% MAE : '+str(round(mae, 2)), backgroundcolor='blue'
                , color='white', weight='roman', size='x-small')

    limy1, limy2 = extremos(y_linha, y2_linha)
    limx1, limx2 = extremos(x_linha)

    plt.yticks(np.arange(limy1 - 1, limy2 + 1))
    plt.xticks(np.arange(limx1 - 1, limx2 + 1))

    plt.show()


holt(0.4, 0.4, 'valores.csv', 4)  # valores de alpha, beta, arquivo com os dados, e total de previsoes
