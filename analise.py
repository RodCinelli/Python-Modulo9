import os
import time
import json
from random import random
from datetime import datetime
import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sys import argv

# URL da API do Banco Central para pegar a taxa CDI
URL = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.4392/dados?formato=json'

# Função para obter a taxa CDI
def obter_taxa_cdi():
    try:
        response = requests.get(URL)
        response.raise_for_status()
        dados = response.json()

        # Pegando o valor mais recente disponível
        if len(dados) > 0:
            ultimo_dado = dados[-1]  # Pega o dado mais recente
            return float(ultimo_dado['valor'])
        else:
            print("Nenhum dado disponível.")
            return None
    except requests.HTTPError as exc:
        print(f"Erro HTTP ao tentar acessar a URL: {exc}")
        return None
    except Exception as exc:
        print(f"Erro inesperado: {exc}")
        raise

# Função para salvar os dados no arquivo CSV
def salvar_dados_csv(data, hora, cdi):
    if not os.path.exists('./taxa-cdi.csv'):
        with open('./taxa-cdi.csv', mode='w', encoding='utf8') as fp:
            fp.write('data,hora,taxa\n')
    with open('./taxa-cdi.csv', mode='a', encoding='utf8') as fp:
        fp.write(f'{data},{hora},{cdi}\n')

# Função para extrair os dados 10 vezes e salvar no CSV
def extrair_dados():
    for _ in range(10):
        data_e_hora = datetime.now()
        data = data_e_hora.strftime('%Y/%m/%d')
        hora = data_e_hora.strftime('%H:%M:%S')

        cdi = obter_taxa_cdi()
        if cdi is not None:
            salvar_dados_csv(data, hora, cdi)

        time.sleep(2 + (random() - 0.5))

    print("Extração concluída com sucesso.")

# Função para gerar o gráfico da taxa CDI
def gerar_grafico(nome_do_grafico):
    # Extraindo as colunas 'hora' e 'taxa' do arquivo CSV
    df = pd.read_csv('./taxa-cdi.csv')

    # Configurando o estilo do Seaborn
    sns.set(style='whitegrid')

    # Criando o gráfico de linha com Seaborn
    plt.figure(figsize=(10, 6))
    grafico = sns.lineplot(x=df['hora'], y=df['taxa'], marker='o', linestyle='-')

    # Ajustando o rótulo do eixo X e rotacionando para uma melhor visualização
    grafico.set(xlabel='Hora', ylabel='Taxa CDI', title='Gráfico da Taxa CDI ao Longo do Dia')
    plt.xticks(rotation=90)  # Rotacionando os rótulos do eixo X

    # Salvando o gráfico no formato PNG com o nome passado como argumento
    grafico.get_figure().savefig(f"{nome_do_grafico}.png", bbox_inches='tight')

    print(f"Gráfico salvo como {nome_do_grafico}.png")

# Função principal que combina a extração e visualização
def main():
    # Verificando se o nome do gráfico foi passado como argumento
    if len(argv) < 2:
        print("Uso: python analise.py <nome-do-grafico>")
        exit(1)

    # Nome do gráfico a ser salvo
    nome_do_grafico = argv[1]

    # Extraindo os dados e salvando no CSV
    extrair_dados()

    # Gerando o gráfico com base nos dados extraídos
    gerar_grafico(nome_do_grafico)

if __name__ == "__main__":
    main()
