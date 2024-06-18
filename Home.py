import streamlit as st
from PIL import Image

st.set_page_config(
    page_title = "Home",
    page_icon = ""
    )

### Os comandos abaixo são os mesmos que constam nos arquivos de visão separadamente

#image_path = r"C:\Users\User\Documents\repos\ftc_programacao_python\logo.jpg"
image = Image.open('logo.jpg')
st.sidebar.image(image, width=120)

st.sidebar.markdown ('# Pluto Company')
st.sidebar.markdown ('## Fastest Delivery in Town')
st.sidebar.markdown ("""---""")

st.write("# Pluto Company Growth Dashboard")

st.sidebar.markdown ('### Powered by Comunidade DS')

st.markdown(
    """
    Growth Dashboard foi construído para acompanhar as métricas de crescimento dos Entregadores e Restaurantes.
    ### Como utilizar esse Growth Darshboard?
    - Visão Empresa:
        - Visão Gerencial: Métricas gerais de comportamento.
        - Visão Tática: Indicadores semanais de crescimento.
        - Visão Geográfica: Insights de geolocalização.
    - Visão Entregador:
        - Acompanhamento dos indicadores semanais de crescimento
    - Visão Restaurante:
        - Indicadores semanais de crescimento dos restaurantes
    ### Ask for Help
    - Time de Data Science no Discord
        - @caiopolari
""")