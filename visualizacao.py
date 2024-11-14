import csv
from sys import argv
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Verificando se o nome do gráfico foi passado como argumento
if len(argv) < 2:
    print("Uso: python visualizacao.py <nome-do-grafico>")
    exit(1)

# Nome do gráfico a ser salvo
nome_do_grafico = argv[1]

# Extraindo as colunas 'hora' e 'taxa' do arquivo CSV
df = pd.read_csv('./taxa-cdi.csv')

# Configurando o estilo do Seaborn
sns.set(style='whitegrid')

# Criando o gráfico de linha com Seaborn
plt.figure(figsize=(10, 6))
grafico = sns.lineplot(x=df['hora'], y=df['taxa'], marker='o', linestyle='-')

# Ajustando o rótulo do eixo X e rotacionando para uma melhor visualização
grafico.set(xlabel='Hora', ylabel='Taxa CDI', title='Gráfico da Taxa CDI ao Longo do Dia')
grafico.set_xticklabels(labels=df['hora'], rotation=90)

# Salvando o gráfico no formato PNG com o nome passado como argumento
grafico.get_figure().savefig(f"{nome_do_grafico}.png", bbox_inches='tight')

print(f"Gráfico salvo como {nome_do_grafico}.png")
