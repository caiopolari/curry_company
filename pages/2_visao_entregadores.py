# Libraries
from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import pandas as pd
from datetime import datetime
from PIL import Image
import folium
from streamlit_folium import folium_static

st.set_page_config(page_title = 'Visão Entregadores', layout = 'wide')

# =======================================
# Funções
# =======================================

def top_delivers(df1, top_asc):
                
    """ Esta função tem a responsabilidade de calcular os entregadores mais rápidos/lentos do dataframe através da função top_asc
    
    Input: Dataframe
    Output: Dataframe """
    
    col = ['Time_taken(min)', 'City', 'Delivery_person_ID']
    
    df_aux = df1.loc[:, col].groupby(['City', 'Delivery_person_ID']).min().sort_values(['City', 'Time_taken(min)'], ascending = top_asc).reset_index()
    df_aux01 = df_aux.loc[df_aux['City'] == 'Metropolitian'].head(10)
    df_aux02 = df_aux.loc[df_aux['City'] == 'Urban'].head(10)
    df_aux03 = df_aux.loc[df_aux['City'] == 'Semi-Urban'].head(10)
    df3 = pd.concat([df_aux01, df_aux02, df_aux03]).reset_index(drop = True)
    return (df3)

    """ Esta função tem a responsabilidade de calcular os entregadores mais lentos do dataframe
    
    Input: Dataframe
    Output: Dataframe """
    
## Limpeza dos dados

def clean_code(df1):
    
    """ Esta função tem a responsabilidade de limpar o dataframe
    
    Tipos de Limpeza:
    1. Remove espaços de maneira massiva
    2. Remove o NaN de linhas específicas
    3. Conversão de colunas
    4. Retira o (min) de time_taken
    
    Input: Dataframe
    Output: Dataframe """
    
    # Removendo NaN de linhas

    df1 = df.copy()
    
    df1 = df1.loc[df1['Road_traffic_density'] != 'NaN', :].copy()
    df1 = df1.loc[df1['City'] != 'NaN', :].copy()
    df1 = df1.loc[df1['Weatherconditions'] != 'NaN', :].copy()
    
    # Conversão de colunas
    
    df1['Delivery_person_Ratings'] = (df1['Delivery_person_Ratings'].astype(float))
    
    linhas_selecionadas = (df1['Delivery_person_Age'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas, :].copy()
    df1['Delivery_person_Age'] = (df1['Delivery_person_Age'].astype(int)).copy()
    
    linhas_selecionadas = (df1['Weatherconditions'] != 'conditions NaN')
    df1 = df1.loc[linhas_selecionadas, :].copy()
    
    linhas_selecionadas = (df1['Festival'] != 'NaN')
    df1 = df1.loc[linhas_selecionadas, :].copy()
    
    df1 = df1.loc[df1['multiple_deliveries'] != 'NaN ', :].copy()
    df1['multiple_deliveries'] = (df1['multiple_deliveries'].astype(int)).copy()
    
    df1['Order_Date'] = pd.to_datetime(df1['Order_Date'], format = '%d-%m-%Y').copy()
    
    # Retirando espaços de maneira massiva
    
    df1['ID'] = df1.loc[:, 'ID'].str.strip()
    df1['Delivery_person_ID'] = df1.loc[:, 'Delivery_person_ID'].str.strip()
    df1['Road_traffic_density'] = df1.loc[:, 'Road_traffic_density'].str.strip()
    df1['Type_of_order'] = df1.loc[:, 'Type_of_order'].str.strip()
    df1['Type_of_vehicle'] = df1.loc[:, 'Type_of_vehicle'].str.strip()
    df1['Festival'] = df1.loc[:, 'Festival'].str.strip()
    df1['City'] = df1.loc[:, 'City'].str.strip()
    df1['Road_traffic_density'] = df1.loc[:, 'Road_traffic_density'].str.strip()
    
    # Retirando o (min) de time_taken
    
    df1['Time_taken(min)'] = df1['Time_taken(min)'].str.strip('(min) ')
    df1['Time_taken(min)'] = (df1['Time_taken(min)'].astype(int)).copy()

    return (df1)

# ----------------------- Início da Estrutura Lógica de Programação -----------------------

# Import dataset
df = pd.read_csv('dataset/train.csv')

# Limpando dataset
df1 = clean_code(df)

# =======================================
# Barra lateral
# =======================================

st.header('Marketplace - Visão Entregadores', divider='rainbow')

#image_path = r"C:\Users\User\Documents\repos\ftc_programacao_python\logo.jpg"
image = Image.open('logo.jpg')
st.sidebar.image(image, width=120)

st.sidebar.markdown ('# Pluto Company')
st.sidebar.markdown ('## Fastest Delivery in Town')
st.sidebar.markdown ("""---""")

st.sidebar.markdown ('## Selecione uma data limite')
date_slider = st.sidebar.slider('Até qual valor?', value=datetime(2022, 3, 3), min_value=datetime(2022, 2, 11), max_value=datetime(2022, 4, 6), format = 'DD/MM/YYYY')

st.sidebar.markdown ("""---""")

traffic_options = st.sidebar.multiselect(
    'Quais as condições do trânsito?',
    ['Low','Medium','High','Jam'],
    default=['Low','Medium','High','Jam'])

weatherconditions = st.sidebar.multiselect(
    'Quais as condições climáticas?',
    ['conditions Cloudy','conditions Fog','conditions Sandstorm','conditions Sunny', 'conditions Windy'],
    default=['conditions Cloudy','conditions Fog','conditions Sandstorm','conditions Sunny', 'conditions Windy'])

st.sidebar.markdown ("""---""")
st.sidebar.markdown ('### Powered by Comunidade DS')

# Filtro de data

linhas_selecionadas = df1['Order_Date'] < date_slider
df1 = df1.loc[linhas_selecionadas, :]

# Filtro de trânsito

linhas_selecionadas = df1['Road_traffic_density'].isin(traffic_options)
df1 = df1.loc[linhas_selecionadas, :]

# Filtro de condições climáticas

linhas_selecionadas = df1['Weatherconditions'].isin(weatherconditions)
df1 = df1.loc[linhas_selecionadas, :]

# =======================================
# Layout no Streamlit
# =======================================

tab1 =  st.tabs(['Visão Gerencial'])

with st.container():
    st.title('Overall Metrics')
    col1, col2, col3, col4 = st.columns(4, gap = 'large')
    
    with col1:
        # Exibir a maior idade dos entregadores
        maior_idade = (df1.loc[:, 'Delivery_person_Age'].max())
        col1.metric('Maior Idade', maior_idade)
        
    with col2:
        # Exibir a menor idade dos entregadores
        menor_idade = (df1.loc[:, 'Delivery_person_Age'].min())
        col2.metric('Menor Idade', menor_idade)

    with col3:
        # Exibir a melhor condição dos veículos
        melhor_condicao = (df1.loc[:, 'Vehicle_condition'].max())
        col3.metric('Melhor Condição', melhor_condicao)

    with col4:
        # Exibit a pior condição dos veículos
        pior_condicao = (df1.loc[:, 'Vehicle_condition'].min())
        col4.metric('Pior Condição', pior_condicao)

with st.container():
    st.markdown("""---""")
    st.title('Avaliações')

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('##### Avaliações Médias por Entregador')
        col = ['Delivery_person_Ratings', 'Delivery_person_ID']
        df_avg_ratings_per_deliver = df1.loc[:, col].groupby('Delivery_person_ID').mean().reset_index()
        st.dataframe(df_avg_ratings_per_deliver)
        
    with col2:
        st.markdown('##### Avaliação Média por Trânsito')
        col = ['Delivery_person_Ratings', 'Road_traffic_density']
        df_avg_std_rating_by_traffic = ( df1.loc[:, col].groupby('Road_traffic_density').agg({'Delivery_person_Ratings': ['mean','std']}))
        df_avg_std_rating_by_traffic.columns = ['delivery_mean', 'delivery_std']
        df_avg_std_rating_by_traffic.reset_index()
        st.dataframe(df_avg_std_rating_by_traffic)
        
        st.markdown('##### Avaliação Média por Clima')
        col = ['Delivery_person_Ratings', 'Weatherconditions']
        df_avg_std_rating_by_weather = ( df1.loc[:, col].groupby('Weatherconditions').agg({'Delivery_person_Ratings': ['mean','std']}))
        df_avg_std_rating_by_weather.columns = ['delivery_mean', 'delivery_std']
        df_avg_std_rating_by_weather.reset_index()
        st.dataframe(df_avg_std_rating_by_weather)

with st.container():
    st.markdown("""---""")
    st.title('Velocidade de Entrega')

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('##### Entregadores Mais Rapidos')
        df3 = top_delivers (df1, top_asc = True)
        st.dataframe(df3)
        
    with col2:
        st.markdown('##### Entregadores Mais Lentos')
        df3 = top_delivers(df1, top_asc = False)
        st.dataframe(df3)