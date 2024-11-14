import os
import time
import json
from random import random
from datetime import datetime
import requests

# URL da API do Banco Central para pegar a taxa CDI
URL = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.4392/dados?formato=json'

def obter_taxa_cdi():
    try:
        # Fazendo a requisição para a API do Banco Central
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

def salvar_dados_csv(data, hora, cdi):
    if not os.path.exists('./taxa-cdi.csv'):
        with open('./taxa-cdi.csv', mode='w', encoding='utf8') as fp:
            fp.write('data,hora,taxa\n')
    with open('./taxa-cdi.csv', mode='a', encoding='utf8') as fp:
        fp.write(f'{data},{hora},{cdi}\n')

def main():
    for _ in range(10):
        data_e_hora = datetime.now()
        data = data_e_hora.strftime('%Y/%m/%d')
        hora = data_e_hora.strftime('%H:%M:%S')

        cdi = obter_taxa_cdi()
        if cdi is not None:
            salvar_dados_csv(data, hora, cdi)

        time.sleep(2 + (random() - 0.5))

    print("Sucesso")

if __name__ == "__main__":
    main()
