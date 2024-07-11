import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import time
import base64
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Huna AI",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.hunaai.com/help',
        'Report a bug': "https://www.hunaai.com/bug",
        'About': "Essa é a plataforma de rastreamento do câncer de mama"})

topo = Image.open("topo.png")
st.image(topo, width=1500, use_column_width=False)

image = Image.open("tagline.png")
st.image(image, width=150, use_column_width=False)

st.title("Plataforma de rastreamento de câncer da Huna")
st.markdown("A Huna fornece soluções acessíveis baseadas em IA para detecção precoce do câncer.")

def download_file(file_path, name):
    with open(file_path, "rb") as file:
        data = file.read()
        base64_encoded = base64.b64encode(data).decode()
        href = f'<a href="data:file/{file_path};base64,{base64_encoded}" download="{file_path}">{name}</a>'
        st.markdown(href, unsafe_allow_html=True)

def fake_load(message, seconds=5):
    with st.spinner(message):
        time.sleep(seconds)

def read_file(file):
    if file.name.endswith('.csv'):
        return pd.read_csv(file)
    elif file.name.endswith('.xlsx'):
        return pd.read_excel(file)
    else:
        st.error("Formato de arquivo não suportado!")
        return None

def discarded_data():
    st.write("Existem dados que foram descartados porque não passaram pelo filtro do algoritmo. "
             "O gráfico a seguir mostra as etapas de filtragem pelos quais os dados foram submetidos.")
    data = {
        'Etapa': [
            'Dataset Inicial',
            'Após filtro de idade',
            'Após remover valores ausentes em NEUTRÓFILOS',
            'Após remover valores ausentes em ERITRÓCITOS',
            'Após remover valores ausentes em LINFÓCITOS',
            'Após remover duplicados'
        ],
        'Tamanho': [1955, 1900, 1500, 1400, 1000, 900]
    }

    df1 = pd.DataFrame(data)

    color_map = {
        'Dataset Inicial': '#f2e3a7',
        'Após filtro de idade': '#ebc77c',
        'Após remover valores ausentes em NEUTRÓFILOS': '#e7a25c',
        'Após remover valores ausentes em ERITRÓCITOS': '#e3744b',
        'Após remover valores ausentes em LINFÓCITOS': '#d14039',
        'Após remover duplicados': '#aa1b34'
    }

    fig = go.Figure()

    fig.add_trace(go.Funnel(
        y=df1['Etapa'],
        x=df1['Tamanho'],
        marker=dict(
            color=[color_map[etapa] for etapa in df1['Etapa']],
            line=dict(width=1, color='#f2e3a7')
        )
    ))

    fig.update_layout(
        title="Tamanho do Dataset Após Cada Etapa de Limpeza de Dados",
        height=500,
        width=1000,
        yaxis_title="Etapas de Limpeza de Dados",
        xaxis_title="Tamanho do Dataset",
        funnelmode="stack"
    )
    fig.update_traces(marker_line_color='#f2e3a7', marker_line_width=1)
    st.plotly_chart(fig)


def distr_data():
    st.subheader('Ranking final')
    st.write("Estratificação por risco das pacientes. "
             "O gráfico a seguir mostra a distribuição dos dados pelo grupo de risco.")

    data = {
        'Risco': ['ALTO', 'MODERADO', 'TÍPICO', 'BAIXO'],
        'Tamanho': [216, 630, 970, 136]
    }

    color_map = {
        'ALTO': '#ea4335',
        'MODERADO': '#fbbc04',
        'TÍPICO': '#3c78d8',
        'BAIXO': '#a4c2f4'
    }
    df2 = pd.DataFrame(data)
    fig = px.bar(
        df2,
        x='Risco',
        y='Tamanho',
        color='Risco',
        color_discrete_map=color_map,
        labels={'Tamanho': 'Número de Pacientes'},
        title="Distribuição de Pacientes por Grupo de Risco"
    )

    fig.update_layout(height=500, width=1000)
    fig.update_traces(textposition='outside')

    st.plotly_chart(fig)

def perc_data():
    data = {
        'Risco': ['ALTO', 'MODERADO', 'TIPICO', 'BAIXO'],
        '% da população': [11.1, 32.3, 49.7, 7.0],
    }

    df3 = pd.DataFrame(data)

    color_map = {
        'ALTO': '#ea4335',
        'MODERADO': '#fbbc04',
        'TIPICO': '#3c78d8',
        'BAIXO': '#a4c2f4'
    }

    fig = go.Figure()

    fig.add_trace(go.Bar(
        y=['% da população'],
        x=[df3.loc[df3['Risco'] == 'ALTO', '% da população'].values[0]],
        name='ALTO',
        orientation='h',
        marker=dict(color=color_map['ALTO']),
        text=f"{df3.loc[df3['Risco'] == 'ALTO', '% da população'].values[0]}%"
    ))
    fig.add_trace(go.Bar(
        y=['% da população'],
        x=[df3.loc[df3['Risco'] == 'MODERADO', '% da população'].values[0]],
        name='MODERADO',
        orientation='h',
        marker=dict(color=color_map['MODERADO']),
        text=f"{df3.loc[df3['Risco'] == 'MODERADO', '% da população'].values[0]}%"
    ))
    fig.add_trace(go.Bar(
        y=['% da população'],
        x=[df3.loc[df3['Risco'] == 'TIPICO', '% da população'].values[0]],
        name='TIPICO',
        orientation='h',
        marker=dict(color=color_map['TIPICO']),
        text=f"{df3.loc[df3['Risco'] == 'TIPICO', '% da população'].values[0]}%"
    ))
    fig.add_trace(go.Bar(
        y=['% da população'],
        x=[df3.loc[df3['Risco'] == 'BAIXO', '% da população'].values[0]],
        name='BAIXO',
        orientation='h',
        marker=dict(color=color_map['BAIXO']),
        text=f"{df3.loc[df3['Risco'] == 'BAIXO', '% da população'].values[0]}%"
    ))
    fig.update_layout(
        barmode='stack',
        showlegend=True,
        height=300,
        width=1000,
        xaxis_title='Valor',
        yaxis_title='Categoria',
        title='Distribuição de Pacientes por Grupo de Risco',
    )

    fig.update_traces(textposition='inside')

    st.plotly_chart(fig)


def login():
    # Centralizando o formulário de login
    col1, col2, col3 = st.columns([3, 3, 3])

    with col2:
        st.subheader("Login")
        username = st.text_input("Usuário")
        password = st.text_input("Senha", type="password")
        if st.button("Login"):
            if username == "admin" and password == "admin":
                st.session_state["authenticated"] = True
                st.success("Login bem-sucedido!")
            else:
                st.error("Usuário ou senha incorretos")

def main():
    st.subheader("Upload de Dataset")
    st.markdown("Faça o upload dos dados de acordo com esse template:")
    st.page_link("https://docs.google.com/spreadsheets/d/1ibIFINcDmMcy4H-68_9WzWkFbY1-8mcqiLQmotre-B0/edit?usp=sharing",
                 label="Template", icon="1️⃣")
    st.markdown("Consulte o Guia de Dados para obter mais detalhes:")
    st.page_link("https://docs.google.com/document/d/1MzKQbJtei3azss6x3hppbS4jwN8PwK-PFTs6Cf_6ZsA/edit?usp=sharing",
                 label="Guia de Dados", icon="2️⃣")

    uploaded_file = st.file_uploader("Escolha um arquivo CSV ou XLSX", type=["csv", "xlsx"])

    if uploaded_file is not None:
        fake_load("Carregando arquivo...", seconds=3)
        st.session_state.uploaded_data = read_file(uploaded_file)

        if st.session_state.uploaded_data is not None:
            st.success("Arquivo carregado com sucesso!")
            fake_load("Processando dados...", seconds=3)
            st.write("Resultado:")
            st.dataframe(st.session_state.uploaded_data)

            confirm_inference = st.selectbox("Deseja fazer a inferência com estes dados?", ("Selecione", "Sim", "Não"))

            if confirm_inference == "Sim":
                fake_load("Transformando dados...", seconds=5)
                st.header("Filtro aplicado nos dados:")
                discarded_data()
                st.write("Caso deseje baixar os dados descartados:")
                download_file("medsenior_discarded.xlsx", "Baixar dados descartados")

                # Resultado final da inferência
                fake_load("Fazendo a inferência dos dados...", seconds=5)
                st.header("Dados rankeados:")
                final_data = pd.read_excel("final_medsenior_rankeado_cliente_final.xlsx")
                st.write("Filtrar por resultado de risco:")
                filtro = st.selectbox("Selecione o resultado de risco", final_data['RISCO'].unique())
                filtered_data = final_data[final_data['RISCO'] == filtro]
                st.write("Resultado final da inferência:")
                st.dataframe(filtered_data)
                st.write("Caso deseje baixar os dados rankeados:")
                download_file("final_medsenior_rankeado_cliente_final.xlsx", "Baixar dados rankeados")
                distr_data()
                perc_data()

            elif confirm_inference == "Não":
                st.session_state.uploaded_data = None
                st.write("Faça o upload do arquivo no qual você deseja realizar a inferência clicando em 'Browse files' acima.")

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if st.session_state["authenticated"]:
    main()
else:
    login()
