# EXEMPLO 2 - OUTLIERS (EXEMPLO 2 DA AULA PASSADA)

# Numeros discrepantes
# Para descobrir os outliers precisamos descobrir o IQR (intervalo interquartil) e depois o Limite superior e o Limite inferior
# IQR = Q3 - Q1
# Limite superior = Q3 + (1.5 * IQR)
# Limite inferior = Q1 - (1.5 * IQR)
# Outliers superiores - Maiores que o limite superior
# Outliers inferiores - Menores que o limite inferior

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Obter dados
try:
    os.system("cls")
    print("Obtendo dados...")

    ENDERECO_DADOS="https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv"
    
    #encodings: utf-8, iso-8859-1, latin1, cp1252
    df_ocorrencias = pd.read_csv(ENDERECO_DADOS, sep=";", encoding="iso-8859-1")
    # Delimitando somente as variáveis do Exemplo01: munic e roubo_veiculo
    df_roubo_veiculo = df_ocorrencias[["munic","roubo_veiculo"]]

    # totalizar roubo veiculo por munic
    # utilizando varios metodos de uma vez:
    df_roubo_veiculo = df_roubo_veiculo.groupby(["munic"]).sum(["roubo_veiculo"]).reset_index()

    # print(df_roubo_veiculo.head())

    print("\nDados obtidos com sucesso!")

except Exception as e:
    print(f"Erro ao obter dados: {e}")
    exit()


# Gerando informações
try:
    print("Calculando informações sobre padrão de roubo de veículos...")
    # Array Numpy
    array_roubo_veiculo = np.array(df_roubo_veiculo["roubo_veiculo"])


    media_roubo_veiculo = np.mean(array_roubo_veiculo)
    mediana_roubo_veiculo = np.median(array_roubo_veiculo)
    dist_roubo_veiculo = abs((media_roubo_veiculo-mediana_roubo_veiculo)/mediana_roubo_veiculo)

    print("\nMEDIDAS DE TENDÊNCIA CENTRAL:")
    print(f"Média de roubo de veículo: {media_roubo_veiculo}")
    print(f"Mediana de roubo de veículo: {mediana_roubo_veiculo}")
    print(f"Distância entre média e mediana: {dist_roubo_veiculo}%")

    # medidas de dispersao
    maximo = np.max(array_roubo_veiculo)
    minimo = np.min(array_roubo_veiculo)
    # amplitude: quanto mais proxima de 0 maior homogeneidade, quanto mais proximo do maximo maior a dispersao
    amplitude = maximo - minimo

    print("\nMEDIDAS DE DISPERSÃO:")
    print(f"Máximo: {maximo}")
    print(f"Mínimo: {minimo}")
    print(f"Amplitude total: {amplitude}")

    # Quartis
    q1 = np.quantile(array_roubo_veiculo, 0.25, method="weibull")
    q2 = np.quantile(array_roubo_veiculo, 0.50, method="weibull")
    q3 = np.quantile(array_roubo_veiculo, 0.75, method="weibull")

    # iqr nao sofre interferencia dos outliers, quanto mais proximo de 0 mais homogeneo, quanto mais proximo de q3 mais heterogeneo
    iqr = q3 - q1
    # vai identificar os outliers acima de q3
    limite_superior = q3 + (1.5 * iqr)
    limite_inferior = q1 - (1.5 * iqr)

    # ! Para existir outliers inferiores o limite inferior precisa ser maior que o minimo da distribuicao
    # ! Caso contrario quer dizer que os dados tendem a manter um padrao
    # ! Mesma coisa para os outliers superiores, o limite superior precisa ser menor que o maximo

    print("\nMEDIDAS DE POSIÇÃO:")
    print(f"Mínimo: {minimo}")
    print(f"Limite inferior: {limite_inferior}")
    print(f"Q1: {q1}")
    print(f"Q2: {q2}")
    print(f"Q3: {q3}")
    print(f"IQR: {iqr}")
    print(f"Limite superior: {limite_superior}")
    print(f"Máximo: {maximo}")

    # RESPONDENDO O ENUNCIADO, FILTRANDO OS OUTLIERS
    df_roubo_veiculo_out_inf = df_roubo_veiculo[df_roubo_veiculo["roubo_veiculo"] < limite_inferior]
    df_roubo_veiculo_out_sup = df_roubo_veiculo[df_roubo_veiculo["roubo_veiculo"] > limite_superior]

    print("\nMUNICÍPIOS COM OUTLIERS INFERIORES:")
    if len(df_roubo_veiculo_out_inf) == 0:
        print("Não existem outliers inferiores!")
    else:
        print(df_roubo_veiculo_out_inf.sort_values(by="roubo_veiculo", ascending=True))

    print("\nMUNICÍPIOS COM OUTLIERS SUPERIORES:")
    if len(df_roubo_veiculo_out_sup) == 0:
        print("Não existem outliers superiores!")
    else:
        print(df_roubo_veiculo_out_sup.sort_values(by="roubo_veiculo", ascending=False))

except Exception as e:
    print(f"Erro ao obter informações sobre padrão de roubo de veículos: {e}")
    exit()

# AULA 21 - CALCULANDO MEDIDAS DE DISTRIBUIÇÃO
try:
    print("\nCalculando Medidas de Distribuição...")

    # Calculando Assimetria
    assimetria = df_roubo_veiculo["roubo_veiculo"].skew()

    # Calculando Curtose
    curtose = df_roubo_veiculo["roubo_veiculo"].kurtosis()

    print("\nMedidas de distribuição:")
    print(f"Assimetria: {assimetria}")
    print(f"Curtose: {curtose}")
except Exception as e:
    print(f"Erro {e}")


# AULA 21 - CRIANDO GRÁFICO BOXPLOT
try:
    # plt.boxplot(array_roubo_veiculo)
    # imprimindo na horizontal, exibindo media e ignorando outliers (não é boa prática)
    # plt.boxplot(array_roubo_veiculo, vert=False, showmeans=True, showfliers=True)
    # plt.show()

    # DIVIDINDO O GRAFICO EM SUBPLOTS
    # 1, 2 = uma linha, 2 colunas
    plt.subplots(1, 2, figsize=(16,7))
    plt.suptitle("Análise de roubo de veículos no RJ")

    # 1,2,1 = Primeiro espaço de 1 linha e 2 colunas
    plt.subplot(1,2,1)
    plt.boxplot(array_roubo_veiculo, vert=False, showmeans=True)
    plt.title("Boxplot dos Dados")

    # Segundo gráfico
    plt.subplot(1, 2, 2)  # Configurar o segundo gráfico no lado direito
    plt.text(0.1, 0.9, f'Média: {media_roubo_veiculo}', fontsize=12)
    plt.text(0.1, 0.8, f'Mediana: {mediana_roubo_veiculo}', fontsize=12)
    plt.text(0.1, 0.7, f'Distância: {dist_roubo_veiculo}', fontsize=12)
    plt.text(0.1, 0.6, f'Menor valor: {minimo}', fontsize=12) 
    plt.text(0.1, 0.5, f'Limite inferior: {limite_inferior}', fontsize=12)
    plt.text(0.1, 0.4, f'Q1: {q1}', fontsize=12)
    plt.text(0.1, 0.3, f'Q3: {q3}', fontsize=12)
    plt.text(0.1, 0.2, f'Limite superior: {limite_superior}', fontsize=12)
    plt.text(0.1, 0.1, f'Maior valor: {maximo}', fontsize=12)
    plt.text(0.1, 0.0, f'Amplitude Total: {amplitude}', fontsize=12)
    plt.title("Medidas Observadas")

    # Desativar os eixos
    plt.axis("off")

    # Ajustar o layout
    plt.tight_layout()

    plt.show()
except Exception as e:
    print(f"Erro ao imprimir dados: {e}")
    exit()
