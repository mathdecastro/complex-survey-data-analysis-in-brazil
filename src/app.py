from pnadc import mapping_dataframe, pnad_dataframe
import streamlit as st
import pandas as pd

# TITLE
st.sidebar.title('PNADC Dashboard')

# CREATING MAPPING DATAFRAME
dictionary_url = 'https://ftp.ibge.gov.br/Trabalho_e_Rendimento/Pesquisa_Nacional_por_Amostra_de_Domicilios_continua/Trimestral/Microdados/Documentacao/Dicionario_e_input_20221031.zip'
dictionary_filename = 'dicionario_PNADC_microdados_trimestral.xls'
variables_filename = 'https://ftp.ibge.gov.br/Trabalho_e_Rendimento/Pesquisa_Nacional_por_Amostra_de_Domicilios_continua/Trimestral/Microdados/Documentacao/Variaveis_PNADC_Trimestral.xls'
df_mapping = mapping_dataframe(dictionary_url = dictionary_url, dictionary_filename = dictionary_filename, variables_filename = variables_filename)

# SELECTING THE YEAR, QUARTER AND VARIABLES
select_year = st.sidebar.selectbox('Select the year of the survey: ', [2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025])
select_quarter = st.sidebar.selectbox('Select the quarter of the survey: ', [1, 2, 3, 4])
try:
    select_variables = st.sidebar.multiselect('Select the variables of the survey: ', df_mapping[(df_mapping['survey_period'] == f'{select_quarter}º tri/{select_year}') & (df_mapping['in_the_survey'] == 1)]['variable'].unique(), default = ['Ano', 'Trimestre', 'UF', 'Estrato', 'V1028'])
except Exception as e:
    st.sidebar.exception(Exception('There is no survey for this year or quarter'))

# DOWNLOAD DATA
if st.sidebar.button('Create dashboard'):
    with st.spinner('Downloading data and creating dashboard.'):
        df = pnad_dataframe(year = select_year, quarter = select_quarter, variables = select_variables, df_mapping = df_mapping)

    # HEADER
    st.header(f'PNADC in the {select_quarter}{["st", "nd", "rd", "th"][select_quarter - 1]} quarter of {select_year}')

    # RAW DATA
    st.subheader('Raw Data')
    st.dataframe(df)

    # UNEMPLOYMENT RATE
    st.subheader('Unemployment Rate by State')

    # CREATING A DATAFRAME FOR THE UNEMPLOYMENT RATE BY STATE
    df_employment = df[['UF', 'VD4002', 'V1028']].groupby(['UF', 'VD4002'], as_index = False).sum()
    df_employment = df_employment.pivot(index = 'UF', columns = 'VD4002', values = 'V1028').reset_index().rename(columns = {1 : 'people_employed', 2 : 'people_unemployed'})
    df_employment.columns.set_names('', inplace = True)

    # CREATING AN UNEMPLOYMENT RATE
    df_employment['unemployment_rate'] = df_employment.apply(lambda row: row.people_unemployed/(row.people_employed + row.people_unemployed)*100, axis = 1)

    # REPLACING WITH THE ACRONYM OF THE STATE
    list_states = {11 : 'RO', 12 : 'AC', 13 : 'AM', 14 : 'RR', 15 : 'PA', 16 : 'AP', 17 : 'TO', 21 : 'MA', 22 : 'PI', 23 : 'CE', 24 : 'RN', 25 : 'PB', 26 : 'PE', 27 : 'AL', 28 : 'SE', 29 : 'BA', 31 : 'MG', 32 : 'ES', 33 : 'RJ', 35 : 'SP', 41 : 'PR', 42 : 'SC', 43 : 'RS', 50 : 'MS', 51 : 'MT', 52 : 'GO', 53 : 'DF'}
    df_employment['UF'] = df_employment['UF'].map(list_states)

    # CREATING A FUNCTION TO GET THE REGION OF THE STATE AND APPLYING IT TO THE DATAFRAME TO CREATE A NEW COLUMN
    def region(state):
        if state in ['RO', 'AC', 'AM', 'RR', 'PA', 'AP', 'TO']:
            return 'N'
        elif state in ['MA', 'PI', 'CE', 'RN', 'PB', 'PE', 'AL', 'SE', 'BA']:
            return 'NE'
        elif state in ['MG', 'ES', 'RJ', 'SP']:
            return 'SE'
        elif state in ['PR', 'SC', 'RS']:
            return 'S'
        elif state in ['MS' ,'MT', 'GO', 'DF']:
            return 'CW'
    df_employment['region'] = df_employment['UF'].map(region)

    # TRANSFORMING THE DATAFRAME
    df_employment = df_employment[['UF', 'region', 'unemployment_rate']]
    df_employment.columns = ['state', 'region', 'unemployment_rate']

    # SHOWING THE DATAFRAME
    st.bar_chart(df_employment, x = 'state', y = ['unemployment_rate'], color = 'region', x_label = 'State', y_label = 'Unemployment Rate (%)')

    st.markdown('#### :grey[Ranking]')
    st.table(df_employment.sort_values(by = ['unemployment_rate'], ascending = False).set_index(pd.RangeIndex(1, len(df_employment) + 1)))