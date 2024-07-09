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

st.set_page_config(page_title = 'Visão Empresa', layout = 'wide')

# =======================================
# Funções
# =======================================

def country_maps(df1):
    """ Esta função tem a responsabilidade de retornar um mapa com a localização central de cada cidade por tipo de tráfego
    
    Input: Dataframe
    Output: Mapa """

    # A localização central de cada cidade por tipo de tráfego.
    colunas = ['Road_traffic_density', 'City', 'Delivery_location_latitude', 'Delivery_location_longitude']
    df_aux = df1.loc[:, colunas].groupby(['City', 'Road_traffic_density']).median().reset_index() # Utiliza-se mediana para obter o ponto central do banco de dados -> a média altera os dados
    map = folium.Map()
    for index, location_info in df_aux.iterrows():
        folium.Marker( [location_info['Delivery_location_latitude'],
                          location_info['Delivery_location_longitude']],
                          popup=location_info[['City', 'Road_traffic_density']] ).add_to( map )
    folium_static(map, width = 1024, height = 600)

def order_by_deliver_by_week (df1):
    """ Esta função tem a responsabilidade de retornar um gráfico de linhas em que reporta a quantidade de pedidos por entregador por semana
    
    Input: Dataframe
    Output: Figura """

    # A quantidade de pedidos por entregador por semana.
    coluna1 = ['ID', 'week_of_year']
    df_aux1 = df1.loc[:, coluna1].groupby(['week_of_year']).count().reset_index()
    coluna2 = ['Delivery_person_ID', 'week_of_year']
    df_aux2 = df1.loc[:, coluna2].groupby(['week_of_year']).nunique().reset_index()
    df_aux = pd.merge(df_aux1, df_aux2, how = 'inner')
    df_aux['order_by_deliver'] = df_aux['ID'] / df_aux['Delivery_person_ID']
    fig = px.line(df_aux, x = 'week_of_year', y = 'order_by_deliver')
    return (fig)
            
def order_by_week(df1):
    """ Esta função tem a responsabilidade de retornar um gráfico de linhas em que reporta a quantidade de pedidos por semana
    
    Input: Dataframe
    Output: Figura """
    
    # Quantidade de pedidos por semana
    df1['week_of_year'] = df1['Order_Date'].dt.strftime('%U') # .dt transforma a sequência de dados em data (se fosse string, seria str)
    df_aux = df1.loc[:, ['ID','week_of_year']].groupby(['week_of_year']).count().reset_index()
    fig = px.line(df_aux, x = 'week_of_year', y = 'ID')
    return(fig)

def traffic_order_city(df1):
    """ Esta função tem a responsabilidade de retornar um gráfico scatter baseado na comparação de volume de pedidos por cidade e tipo de tráfego 
    
    Input: Dataframe
    Output: Figura """
    
    # Comparação do volume de pedidos por cidade e tipo de tráfego.
    colunas = ['ID','City','Road_traffic_density']
    df_aux = df1.loc[:, colunas].groupby(['City','Road_traffic_density']).count().reset_index()
    fig = px.scatter(df_aux, x = 'City', y = 'Road_traffic_density', size = 'ID', color = 'City')
    return (fig)

def traffic_order_share(df1):
    """ Esta função tem a responsabilidade de retornar um gráfico de pizza baseado na distribuição de pedidos por tipo de tráfego
    
    Input: Dataframe
    Output: Figura """        
    # Distribuição dos pedidos por tipo de tráfego
    
    df_aux = df1.loc[:,['ID','Road_traffic_density']].groupby('Road_traffic_density').count().reset_index()
    df_aux['entregas_perc'] = df_aux['ID'] / df_aux['ID'].sum()
    fig = px.pie(df_aux, values = 'entregas_perc', names = 'Road_traffic_density')
    return (fig)

def order_metric(df1):
    """ Esta função tem a responsabilidade de retornar uma figura baseado na quantidade de pedidos por dia
    
    Input: Dataframe
    Output: Figura """        
    colunas = ['ID', 'Order_Date']
    df_aux = df1.loc[:, colunas].groupby(['Order_Date']).count().reset_index()
        
    # Gráfico de barras
        
    fig = px.bar(df_aux, x = 'Order_Date', y = 'ID')
    return (fig)

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
    
    linhas_selecionadas = (df1['Weatherconditions'] != 'conditions NaN ')
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

## Visão - Empresa

# =======================================
# Barra lateral
# =======================================

st.header('Marketplace - Visão Empresa', divider='rainbow')

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

st.sidebar.markdown ("""---""")
st.sidebar.markdown ('### Powered by Comunidade DS')

# Filtro de data

linhas_selecionadas = df1['Order_Date'] < date_slider
df1 = df1.loc[linhas_selecionadas, :]

# Filtro de trânsito

linhas_selecionadas = df1['Road_traffic_density'].isin(traffic_options)
df1 = df1.loc[linhas_selecionadas, :]

# =======================================
# Layout no Streamlit
# =======================================

tab1, tab2, tab3 =  st.tabs(['Visão Gerencial', 'Visão Tática', 'Visão Geográfica'])

with tab1:
    with st.container():
        st.markdown('# Orders by Day')
        fig = order_metric(df1)
        st.plotly_chart( fig, use_container_width=True)
        
    # Criando duas colunas no Streamlit
    
    with st. container():
        col1, col2 = st.columns (2)
        with col1:
            st.markdown('# Traffic Order Share')
            fig = traffic_order_share(df1)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown('# Traffic Order City')
            fig = traffic_order_city(df1)
            st.plotly_chart(fig, use_container_width=True)
                
with tab2:
    with st.container():
        
        st.markdown("# Order by Week")
        fig = order_by_week(df1)
        st.plotly_chart(fig, use_container_width=True)
        
    with st.container():
        
        st.markdown("# Order by Week by Deliver")
        fig = order_by_deliver_by_week (df1)
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    
    st.markdown("# Country Maps")
    country_maps (df1)
    
