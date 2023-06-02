'''
Função: Programa para coleta automatizada dos arquivos em csv do site de dados estatísticos da SSP-SP
Criadores: Caio Henrique Silva Gonçalves e Aline Vieira dos Santos
Data: 16/05/2023
'''

'início do programa'

# Importando as bibliotecas necessárias
'início da etapa'

import os
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import pandas as pd
import json

'fim da etapa'
'-------------------------------------------------------------------------------------------------------------------------------------------------------'

# Início do programa, informações base para iniciar o looping
'início da etapa'

# Aponta o caminho para a pasta que os arquivos coletados serão armazenados
folder_path = r'C:\Users\TG2\Produtividade_Policial'

# Aponta o caminho do navegador que será utilizado
options = Options()
options.binary_location = 'C:/Program Files/Mozilla Firefox/firefox.exe'

# Aponta a pasta do Web Driver e a página web que será acessada
driver = webdriver.Firefox(options=options, executable_path=r'C:\Users\Documentos\ChromeDrive\geckodriver.exe')
driver.get('https://www.ssp.sp.gov.br/estatistica/pesquisa.aspx')

# Importando os arquivos de referência dos códigos (xlsx) e dos nomes dos arquivos (json)
dfr = pd.read_excel('C:/Users/TG2/codigo_nome_arquivo_json.xlsx', usecols=["codigo"])
with open('C:/Users/TG2/codigo_nome_arquivo.json') as file:
    referencias = json.load(file)
codigos = dfr["codigo"].tolist()
counter = 0

'fim da etapa'
'-------------------------------------------------------------------------------------------------------------------------------------------------------'

# Looping para coleta dos dados
'início da etapa'

for i in range(0, 1345):

    codigo = f"{codigos[i]}"
    if codigo in referencias:
        nome_arquivo = referencias[codigo]
    delegacia = [str(valor) for valor in codigos]

    dropdown_element = driver.find_element_by_id('conteudo_ddlDelegacias')
    dropdown = Select(dropdown_element)
    dropdown.select_by_value(delegacia[i])

    counter += 1
    
    for j in range(2001, 2024):

        anos = str(j)
        file_name = f'{nome_arquivo} {j}.csv'
        
        # Aplica o filtro no conteúdo "Anos" por meio do código valor apontado no select_by_value
        dropdown_element = driver.find_element_by_id('conteudo_ddlAnos')
        dropdown = Select(dropdown_element)
        dropdown.select_by_value(anos)
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        table = soup.find('table')
        
        try:
            if table is not None:
                df = pd.read_html(str(table))[0]
                df = df.drop(df.columns[-1:], axis=1)
                # transponha o DataFrame
                df = df.transpose()
                # Resetar o index
                df = df.reset_index()
            else:
                # ignora erro caso alguma tabela não esteja preenchida
                continue
        except ValueError:
            # ignora o erro "ValueError"
             continue

        # salve o arquivo transposto com o nome original do arquivo
        file_path = os.path.join(folder_path, file_name)
        df.to_csv(file_path, sep=';', index=False, header=False, encoding='utf-16-le')        


    # Aplica o filtro no conteúdo "Anos" por meio do código valor apontado no select_by_value
    dropdown_element = driver.find_element_by_id('conteudo_ddlAnos')
    dropdown = Select(dropdown_element)
    dropdown.select_by_value('0')

    # Aplica o filtro no conteúdo "Anos" por meio do código valor apontado no select_by_value
    dropdown_element = driver.find_element_by_id('conteudo_ddlRegioes')
    dropdown = Select(dropdown_element)
    dropdown.select_by_value('0')

    # Aplica o filtro no conteúdo "Anos" por meio do código valor apontado no select_by_value
    dropdown_element = driver.find_element_by_id('conteudo_ddlMunicipios')
    dropdown = Select(dropdown_element)
    dropdown.select_by_value('0')

    # Aplica o filtro no conteúdo "Delegacias" por meio do código valor apontado no select_by_value
    dropdown_element = driver.find_element_by_id('conteudo_ddlDelegacias')
    dropdown = Select(dropdown_element)
    dropdown.select_by_value('0')
    
    if counter == 15:
        # Quit the webdriver
        driver.quit()
        counter = 0  # Reset the counter
        time.sleep(3)  # Wait for a few seconds before restarting

        # Restart the webdriver
        driver = webdriver.Firefox(options=options, executable_path=r'C:\Users\Documentos\ChromeDrive\geckodriver.exe')
        driver.get('https://www.ssp.sp.gov.br/estatistica/pesquisa.aspx')


driver.quit()
'fim da etapa'
'-------------------------------------------------------------------------------------------------------------------------------------------------------'
'fim do programa'