from pnadc import mapping_dataframe, pnad_dataframe
import pandas as pd
import streamlit as st

# TITLE
st.title('PNADC Dashboard')

# CREATING MAPPING DATAFRAME
dictionary_url = 'https://ftp.ibge.gov.br/Trabalho_e_Rendimento/Pesquisa_Nacional_por_Amostra_de_Domicilios_continua/Trimestral/Microdados/Documentacao/Dicionario_e_input_20221031.zip'
dictionary_filename = 'dicionario_PNADC_microdados_trimestral.xls'
variables_filename = 'https://ftp.ibge.gov.br/Trabalho_e_Rendimento/Pesquisa_Nacional_por_Amostra_de_Domicilios_continua/Trimestral/Microdados/Documentacao/Variaveis_PNADC_Trimestral.xls'
df_mapping = mapping_dataframe(dictionary_url = dictionary_url, dictionary_filename = dictionary_filename, variables_filename = variables_filename)

# SELECTING THE YEAR, QUARTER AND VARIABLES
select_year = st.selectbox('Select the year of the survey: ', [2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025])
select_quarter = st.selectbox('Select the quarter of the survey: ', [1, 2, 3, 4])
select_variables = st.multiselect('Select the variables of the survey: ', df_mapping[(df_mapping['survey_period'] == f'{select_quarter}º tri/{select_year}') & (df_mapping['in_the_survey'] == 1)]['variable'].unique(), default = ['Ano', 'Trimestre', 'UF', 'Estrato', 'V1028'])

# DOWNLOAD DATA
if st.button('Download Data'):
    df = pnad_dataframe(year = select_year, quarter = select_quarter, variables = select_variables, df_mapping = df_mapping)
    st.subheader('Raw Data')
    st.dataframe(df)