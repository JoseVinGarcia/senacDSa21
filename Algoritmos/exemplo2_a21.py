# EXEMPLO 2 - EXPANDINDO ATIVIDADE

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# OBTENDO DADOS
try:
    os.system("cls")
    print("Obtendo dados...")
    ENDERECO_DADOS="https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv"
    
    df_ocorrencias = pd.read_csv(ENDERECO_DADOS, sep=";", encoding="iso-8859-1")

    df_recuperacao_cisp = df_ocorrencias[["cisp","recuperacao_veiculos"]]
    df_recuperacao_cisp = df_recuperacao_cisp.groupby(["cisp"]).sum(["recuperacao_veiculos"]).reset_index()

    print("Dados obtidos com sucesso!")

except Exception as e:
    print(f"Erro ao obter dados: {e}")
    exit()

# CALCULANDO DADOS
try:
    print("Calculando informações...")

    # Transformando em Array
    array_recuperacao = np.array(df_recuperacao_cisp["recuperacao_veiculos"])

    # Calculando e printando medidas centrais
    media_recuperacao = np.mean(array_recuperacao)
    mediana_recuperacao = np.median(array_recuperacao)
    dist_recuperacao = abs((media_recuperacao-mediana_recuperacao)/mediana_recuperacao)*100 # Sempre multiplicar por 100. Será 138%, bem assimetrico

    # Calculando e printando medidas dispersao
    maximo = np.max(array_recuperacao)
    minimo = np.min(array_recuperacao)
    amplitude = maximo - minimo # relata a mesma coisa que o iqr, porem dessa vez considerando outliers etc. quanto mais perto do valor maximo, mais heterogeneos os dados

    # Calculando e printando medidas de posição
    q1 = np.quantile(array_recuperacao, 0.25, method="weibull")
    q3 = np.quantile(array_recuperacao, 0.75, method="weibull")
    iqr = q3 - q1 # Esta bem proximo de Q3, entao os dados estao bem disperso

    limite_superior = q3 + (1.5 * iqr)
    limite_inferior = q1 - (1.5 * iqr)

    print("\nMEDIDAS DE TENDÊNCIA CENTRAL")
    print(f"Média de recuperação de veículos: {media_recuperacao}")
    print(f"Mediana de recuperação de veículos: {mediana_recuperacao}")
    print(f"Distância entre média e mediana: {dist_recuperacao}%")

    print("\nMEDIDAS DE DISPERSÃO")
    print(f"Máximo: {maximo}")
    print(f"Mínimo: {minimo}")
    print(f"Amplitude total: {amplitude}")

    print("\nMEDIDAS DE POSIÇÃO")
    print(f"Mínimo: {minimo}")
    print(f"Limite inferior: {limite_inferior}")
    print(f"Q1: {q1}")
    print(f"Q3: {q3}")
    print(f"IQR: {iqr}")
    print(f"Limite superior: {limite_superior}")
    print(f"Máximo: {maximo}")

    # Descobrindo outliers
    df_recuperacao_out_inf = df_recuperacao_cisp[df_recuperacao_cisp["recuperacao_veiculos"] < limite_inferior]
    df_recuperacao_out_sup = df_recuperacao_cisp[df_recuperacao_cisp["recuperacao_veiculos"] > limite_superior]

    if len(df_recuperacao_out_inf) == 0:
        print("\nSEM CISPS COM OUTLIERS INFERIORES!")
    else:
        print("\nCISPS COM OUTLIERS INFERIORES:")
        print(df_recuperacao_out_inf.sort_values(by="recuperacao_veiculos", ascending=True).to_string())

    if len(df_recuperacao_out_sup) == 0:
        print("\nSEM CISPS COM OUTLIERS SUPERIORES")
    else:
        print("\nCISPS COM OUTLIERS SUPERIORES:")
        print(df_recuperacao_out_sup.sort_values(by="recuperacao_veiculos", ascending=False).to_string()) # to_string mostra tudo

except Exception as e:
    print(f"Erro ao obter informações: {e}")
    exit()

# AULA 21 - DISTRIBUIÇÃO
try:
    print("\nCalculando Medidas de Distribuição...")

    # Calculando Assimetria
    assimetria = df_recuperacao_cisp["recuperacao_veiculos"].skew()

    # Calculando Curtose
    curtose = df_recuperacao_cisp["recuperacao_veiculos"].kurtosis()

    print("\nMedidas de distribuição:")
    print(f"Assimetria: {assimetria}")
    print(f"Curtose: {curtose}")
except Exception as e:
    print(f"Erro {e}")

# AULA 21 - GRÁFICOS
try:
    plt.subplots(2,2, figsize=(16,7))
    plt.suptitle("Análise de Recuperação de Veículos no RJ", fontsize=20)

    plt.subplot(2,2,1)
    plt.boxplot(array_recuperacao, vert=False, showmeans=True)
    plt.title("Boxplot dos Dados")

    # Histograma
    plt.subplot(2, 2, 2)
    plt.hist(array_recuperacao, bins=50, edgecolor="black")
    plt.axvline(media_recuperacao, color="g", linewidth=1)
    plt.axvline(mediana_recuperacao, color="y", linewidth=1)

    # Terceira posição
    plt.subplot(2, 2, 3)
    plt.text(0.1, 1.0, f'Média: {media_recuperacao}', fontsize=12)
    plt.text(0.1, 0.9, f'Mediana: {mediana_recuperacao}', fontsize=12)
    plt.text(0.1, 0.8, f'Distância: {dist_recuperacao}', fontsize=12)
    plt.text(0.1, 0.7, f'Menor valor: {minimo}', fontsize=12) 
    plt.text(0.1, 0.6, f'Limite inferior: {limite_inferior}', fontsize=12)
    plt.text(0.1, 0.5, f'Q1: {q1}', fontsize=12)
    plt.text(0.1, 0.4, f'Q3: {q3}', fontsize=12)
    plt.text(0.1, 0.3, f'Limite superior: {limite_superior}', fontsize=12)
    plt.text(0.1, 0.2, f'Maior valor: {maximo}', fontsize=12)
    plt.text(0.1, 0.1, f'Amplitude Total: {amplitude}', fontsize=12)
    plt.title("Medidas Observadas")

    # Quarta posição
    # plt.subplot(2, 2, 4)

    plt.axis("off")
    plt.tight_layout()
    plt.show()

except Exception as e:
    print(f"Erro {e}")
    exit()
