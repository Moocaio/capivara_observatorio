'''
Função: Programa para consolidar os arquivos coletados em um único arquivo CSV
Criadores: Caio Henrique Silva Gonçalves e Aline Vieira dos Santos
Data: 19/05/2023
'''

import os
import pandas as pd

folder_path = r'C:\Users\TG2\Ocorrencias_Registradas'

dataframes = []

for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        file_path = os.path.join(folder_path, filename)
        df = pd.read_csv(file_path, delimiter=';', encoding='utf-16-le')
        df['Nome da Origem'] = filename  # Adicione uma coluna com o nome do arquivo
        dataframes.append(df)

combined_df = pd.concat(dataframes, ignore_index=True)

header = ['Mês de Ocorrência', 'OCORRÊNCIAS DE PORTE DE ENTORPECENTES', 'OCORRÊNCIAS DE TRÁFICO DE ENTORPECENTES', 
          'OCORRÊNCIAS DE APREENSÃO DE ENTORPECENTES(1)', 	'OCORRÊNCIAS DE PORTE ILEGAL DE ARMA',
          'Nº DE ARMAS DE FOGO APREENDIDAS', 'Nº DE FLAGRANTES LAVRADOS', 'Nº DE INFRATORES APREENDIDOS EM FLAGRANTE', 
          'Nº DE INFRATORES APREENDIDOS POR MANDADO', 'Nº DE PESSOAS PRESAS EM FLAGRANTE', 
          'Nº DE PESSOAS PRESAS POR MANDADO', 'Nº DE PRISÕES EFETUADAS', 'Nº DE VEÍCULOS RECUPERADOS', 
          'TOT. DE INQUÉRITOS POLICIAIS INSTAURADOS', 'Nome da Origem']

output_file = r'C:\Users\TG2\Teste\ocorrencias_registradas.csv'
combined_df.to_csv(output_file, sep=';', index=False, header=header, encoding='utf-16-le')