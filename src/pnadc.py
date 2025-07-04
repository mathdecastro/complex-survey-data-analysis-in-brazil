from zipfile import ZipFile
from io import BytesIO
import pandas as pd
import numpy as np
import requests
import time

# GETTING DATA FROM EXCEL IN A WEBSITE
def get_data_excel(url):
    response = requests.get(url)
    return pd.read_excel(BytesIO(response.content), usecols = None)

# GETTING DATA FROM EXCEL IN ZIPPED FILE IN A WEBSITE
def get_data_excel_zip(url, excel_name):
    response = requests.get(url)
    archive = ZipFile(BytesIO(response.content))
    return pd.read_excel(BytesIO(archive.read(excel_name)), usecols = None)

# CREATING A MAPPING DATAFRAME FOR THE PNADC READING
def mapping_dataframe(dictionary_url, dictionary_filename, variables_filename):
    # READING THE FILES
    df_dictionary = get_data_excel_zip(url = dictionary_url, excel_name = dictionary_filename)
    df_variables = get_data_excel(url = variables_filename)

    # VARIABLES
    df_variables = pd.melt(df_variables, id_vars = ['Variável'], value_vars = df_variables.columns[1:], var_name = 'survey_period', value_name = 'in_the_survey')
    df_variables.rename(columns = {'Variável' : 'variable'}, inplace = True)
    df_variables['in_the_survey'] = np.select([df_variables['in_the_survey'] == 'X'], [1])

    # DICTIONARY
    df_dictionary = df_dictionary.iloc[3:, :3]
    df_dictionary.columns = ['initial_position', 'data_length', 'variable']
    df_dictionary.dropna(inplace = True)

    # MERGED DATAFRAME
    df_mapping = pd.merge(left = df_variables, right = df_dictionary, left_on = 'variable', right_on = 'variable')

    return df_mapping

# CREATING A DATAFRAME WITH THE DATA
def pnad_dataframe(year, quarter, variables, df_mapping):
    
    initial_variables = ['UF', 'VD4002', 'V1028']
    additional_variables = variables
    filter = (df_mapping['survey_period'] == f'{quarter}º tri/{year}') & (df_mapping['in_the_survey'] == 1) & (df_mapping['variable'].isin(list(set(initial_variables + additional_variables))))

    df_read = df_mapping[filter][['variable', 'initial_position', 'data_length']].reset_index(drop = True)
    df_read['initial_position'] = df_read['initial_position'].apply(lambda position: position - 1)
    df_read['final_position'] = df_read.apply(lambda row: row.initial_position + row.data_length, axis = 1)

    colnames = df_read['variable'].to_list()
    colspecs = [k for k in zip(df_read['initial_position'].tolist(), df_read['final_position'].tolist())]

    df = pd.DataFrame()

    max_retry = 3
    timeout = 12
    for retry in range(1, max_retry + 1):
        try:
            response = requests.get(f'https://ftp.ibge.gov.br/Trabalho_e_Rendimento/Pesquisa_Nacional_por_Amostra_de_Domicilios_continua/Trimestral/Microdados/{year}/{get_zip_name(year, quarter)}', timeout = timeout)
            archive = ZipFile(BytesIO(response.content))
            df = pd.read_fwf(BytesIO(archive.read(f'PNADC_0{quarter}{year}.txt')), colspecs = colspecs, names = colnames)
            break
        except requests.exceptions.Timeout:
            time.sleep(1)
        except requests.exceptions.RequestException as e:
            break

    return df

def get_zip_name(year, quarter):
    url = 'https://servicodados.ibge.gov.br/api/v1/downloads/estatisticas?caminho=Trabalho_e_Rendimento/Pesquisa_Nacional_por_Amostra_de_Domicilios_continua/Trimestral/Microdados&nivel=1'
    response = requests.get(url)
    for folder in response.json():
        if folder['children'] != None:
            for file in folder['children']:
                if file['name'].startswith(f'PNADC_0{quarter}{year}') & file['name'].endswith('.zip'):
                    return file['name']