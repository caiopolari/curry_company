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
import numpy as np

st.set_page_config(page_title = 'Visão Restaurantes', layout = 'wide')

# =======================================
# Funções
# =======================================

def avg_std_time_graph(df1):

    """ Esta função tem a responsabilidade de plotar o gráfico de barras que possui a distribuição da distância por cidade
    
    Input: Dataframe
    Output: Gráfico de barras """
    
    col = ['Time_taken(min)', 'City']
    df_aux = df1.loc[:, col].groupby(['City']).agg({'Time_taken(min)': ['mean', 'std']})
    df_aux.columns = ['avg_time', 'std_time']
    df_aux = df_aux.reset_index()
    fig = go.Figure()
    fig.add_trace(go.Bar(name = 'Control', x = df_aux['City'], y = df_aux['avg_time'], error_y = dict(type = 'data', array = df_aux['std_time'])))
    fig.update_layout(barmode = 'group')
    return (fig)

def avg_std_time_festival_delivery(df1, op, festival):
    
    """ Esta função tem a responsabilidade de calcular o tempo médio e o desvio padrão do tempo de entrega
        Parâmetros:
            Input:
                - df: Dataframe
                - op: Tipo de operação
                    'avg_time' = Calcula o tempo médio
                    'std_time' = Calcula o desvio padrão
                - festival: Com ou sem festival
                    'Yes' = Calcula com festival
                    'No' = Calcula sem festival
            Output:
                - df: Dataframe """
            
    col = ['Time_taken(min)', 'Festival']
    df_aux = df1.loc[:, col].groupby('Festival').agg({'Time_taken(min)': ['mean', 'std']})
    df_aux.columns = ['avg_time', 'std_time']
    df_aux = df_aux.reset_index()
    df_aux = np.round(df_aux.loc[df_aux['Festival'] == festival, op], 2)
    return (df_aux)

def distance(df1):
    
    """ Esta função tem a responsabilidade de calcular a distância média entre os restaurantes.
    
    Input: Dataframe
    Output: Dataframe"""
    
    col = ['Restaurant_latitude', 'Restaurant_longitude', 'Delivery_location_latitude', 'Delivery_location_longitude']
    df1['distance'] = df1.loc[:, col].apply( lambda x: haversine ((x['Restaurant_latitude'], x['Restaurant_longitude']), (x['Delivery_location_latitude'], x['Delivery_location_longitude'])), axis = 1)
    avg_distance = np.round(df1.loc[:, 'distance'].mean(),2)
    return avg_distance

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
    
    df1 = df1.loc[df1['Road_traffic_density'] != 'NaN ', :].copy()
    df1 = df1.loc[df1['City'] != 'NaN ', :].copy()
    df1 = df1.loc[df1['Weatherconditions'] != 'NaN ', :].copy()
    
    # Conversão de colunas
    
    df1['Delivery_person_Ratings'] = (df1['Delivery_person_Ratings'].astype(float))
    
    linhas_selecionadas = (df1['Delivery_person_Age'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas, :].copy()
    df1['Delivery_person_Age'] = (df1['Delivery_person_Age'].astype(int)).copy()
    
    linhas_selecionadas = (df1['Weatherconditions'] != 'conditions NaN')
    df1 = df1.loc[linhas_selecionadas, :].copy()
    
    linhas_selecionadas = (df1['Festival'] != 'NaN ')
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

st.header('Marketplace - Visão Restaurantes', divider='rainbow')

#image_path = r"C:\Users\User\Documents\repos\ftc_programacao_python\logo.jpg"
image = Image.open('logo.png')
st.sidebar.image(image, width=120)

st.sidebar.markdown ('# Curry Company')
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
    st.title("Overall Metrics")
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1:
        delivery_unique = len(df1['Delivery_person_ID'].unique())
        st.metric('Entregadores', delivery_unique)
    with col2:
        avg_distance = distance(df1)
        col2.metric('Avg dist', avg_distance)
    with col3:
        df_aux = avg_std_time_festival_delivery(df1, 'avg_time', 'Yes')
        col3.metric('Tempo médio c/ festival', df_aux)
    with col4:
        df_aux = avg_std_time_festival_delivery(df1, 'std_time', 'Yes')
        col4.metric('Std s/ festival', df_aux)
    with col5:
        df_aux = avg_std_time_festival_delivery(df1, 'avg_time', 'No')
        col5.metric('Tempo médio s/ festival', df_aux)
    with col6:
        df_aux = avg_std_time_festival_delivery(df1, 'std_time', 'No')
        col6.metric('Std s/ festival', df_aux)
with st.container():
    st.markdown("""---""")
    st.title("Distribuição da distância")
    col1, col2 = st.columns(2)
    with col1:
        fig = avg_std_time_graph(df1)
        st.plotly_chart(fig)
    with col2:
        st.markdown("""---""")
        col = ['Time_taken(min)', 'City', 'Type_of_order']
        df_aux = df1.loc[:, col].groupby(['City', 'Type_of_order']).agg({'Time_taken(min)': ['mean', 'std']})
        df_aux.columns = ['avg_time', 'std_time']
        df_aux = df_aux.reset_index()
        st.dataframe(df_aux)
with st.container():
    st.markdown("""---""")
    st.title("Distribuição do tempo")
    col1, col2 = st.columns(2)
    with col1:
        col = ['Restaurant_latitude', 'Restaurant_longitude', 'Delivery_location_latitude', 'Delivery_location_longitude']
        df1['distance'] = df1.loc[:, col].apply( lambda x: haversine ((x['Restaurant_latitude'], x['Restaurant_longitude']), (x['Delivery_location_latitude'], x['Delivery_location_longitude'])), axis = 1)
        avg_distance = np.round(df1.loc[:, ['City','distance']].groupby('City').mean().reset_index(),2)
        fig = go.Figure(data = [go.Pie(labels = avg_distance['City'], values = avg_distance['distance'], pull = [0, 0.1, 0])])
        st.plotly_chart(fig)
    with col2:
        col = ['Time_taken(min)', 'City', 'Road_traffic_density']
        df_aux = df1.loc[:, col].groupby(['City', 'Road_traffic_density']).agg({'Time_taken(min)': ['mean', 'std']})
        df_aux.columns = ['avg_time', 'std_time']
        df_aux = df_aux.reset_index()
        fig = px.sunburst(df_aux, path = ['City', 'Road_traffic_density'], values = 'avg_time', color = 'std_time', color_continuous_scale = 'RdBu', color_continuous_midpoint = np.average(df_aux['std_time']))
        st.plotly_chart(fig)
