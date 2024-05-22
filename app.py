import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import time
import base64
from PIL import Image

st.set_page_config(
    page_title="Huna ai",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.hunaai.com/help',
        'Report a bug': "https://www.hunaai.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"})

image = Image.open("huna.png")

st.image(image, use_column_width=True)
st.title("Plataforma de rastreamento de câncer da Huna")
st.text("A Huna fornece soluções acessíveis baseadas em IA para detecção precoce do câncer.")

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
        'Tamanho': [1955, 1954, 1952, 1952, 1952, 1952]
    }

    df1 = pd.DataFrame(data)
    df1 = df1[::-1].reset_index(drop=True)
    colors = sns.color_palette("YlOrRd", len(df1))
    bar_colors = [colors[i] for i in range(len(df1))]
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.barh(df1['Etapa'], df1['Tamanho'], color=bar_colors)
    for i, v in enumerate(df1['Tamanho']):
        ax.text(v + 5, i, str(v), color='black', va='center')

    ax.set_xlabel('Tamanho do Dataset')
    ax.set_ylabel('Etapas de Limpeza de Dados')
    #ax.set_title('Tamanho do Dataset Após Cada Etapa de Limpeza de Dados')

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.tick_params(left=False, bottom=False)

    st.pyplot(fig)


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
    st.text("Faça o upload dos dados de acordo com esse template:")
    st.page_link("https://docs.google.com/spreadsheets/d/1ibIFINcDmMcy4H-68_9WzWkFbY1-8mcqiLQmotre-B0/edit?usp=sharing",
                 label="Template", icon="1️⃣")
    st.text("Consulte o Guia de Dados para obter mais detalhes:")
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

            elif confirm_inference == "Não":
                st.session_state.uploaded_data = None
                st.write("Faça o upload do arquivo no qual você deseja realizar a inferência clicando em 'Browse files' acima.")

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if st.session_state["authenticated"]:
    main()
else:
    login()
