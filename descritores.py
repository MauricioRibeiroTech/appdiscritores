import streamlit as st
import pandas as pd
import numpy as np


def per_aluno(A, B):
    p = (A / B) * 100
    return p


st.set_page_config(
    page_title="SIMULADOS SAEB HD",
    page_icon=":book:",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/MauricioRibeiroTech',
        'Report a bug': "https://github.com/MauricioRibeiroTech",
        'About': "# Aplicativo para os Indices dos Simulados do SAEB-HD "
    }
)

with st.sidebar:
    st.markdown('# Relatório de notas parcial')
    st.title('Simulados SAEB 2025  \n Escola Estadual Helena Dionysio')

    df = pd.read_csv("Dados_Planilha_9A/descritores.csv", sep=",")

    with st.sidebar:
        salas_distintas = df["Simulados"].unique().tolist()
        salas_selecionadas = st.selectbox("Simulados", salas_distintas)

        componente_selecionada = st.radio("Componentes", ["Matematica", "Portugues"])
        if componente_selecionada:
            df = df[df["Simulados"] == salas_selecionadas]

        if componente_selecionada:
            df = df[df["Componentes"] == componente_selecionada]

st.header("Relatório de notas de " + str(componente_selecionada))
        # dataframe desconsiderando as tres primeiras colunas
df1 = df.iloc[:, 3:38]
num_NaN = df1.iloc[1].isna().sum()
Num_descritores_contemplados = len(df1.columns) - num_NaN

df_alunos = df.iloc[:, 0]
Num_descritores = len(df1.columns) - num_NaN
Num_alunos = len(df_alunos)
df_analise_alunos = pd.DataFrame()
df_descritores = pd.DataFrame()

# soma das linhas do dataframe (analise por aluno)
df2 = df1.sum(axis=1)
df_analise_alunos['Nomes'] = df_alunos
df_analise_alunos['Porcentagem'] = (df2 / Num_descritores_contemplados) * 100

# df_descritores['Descritores']

df_acima_de_60 = df_analise_alunos[df_analise_alunos['Porcentagem'] >= 60]

df_descritores['Descritor'] = df1.columns.tolist()
df_descritores['Porcentagem'] = df1.sum(axis=0).tolist()
# st.table(df_descritores['Porcentagem'])

df_descritores['Porcentagem'] = (df_descritores['Porcentagem'] / Num_alunos) * 100
# df_porcentagem_descritor = df1.sum(axis=0)

df_descritores_mean = df_descritores[df_descritores['Porcentagem'] != 0.0]

# Gráfico Notas em Porcentagem dos alunos
st.markdown("## Nota em porcentagem dos alunos")
st.bar_chart(df_analise_alunos, x="Nomes", y="Porcentagem", stack=False)

# Gráfico de porcentagem dos descritores
st.markdown("## Porcentagem de acerto dos descritores trabalhados no " + str(salas_selecionadas))
st.bar_chart(df_descritores, x="Descritor", y="Porcentagem", stack=False)

a, b = st.columns(2)
dif1 = df_descritores_mean['Porcentagem'].mean().round(2) - 60
dif2 = df_analise_alunos['Porcentagem'].mean().round(2) - 60

a.metric("Porcentagem Média Descritores", df_descritores_mean['Porcentagem'].mean().round(2), dif1.round(2),
         border=True)
b.metric("Porcentagem Média Alunos", df_analise_alunos['Porcentagem'].mean().round(2), dif2.round(2), border=True)

st.markdown("# 10 Primeiros alunos com maiores notas no " + str(salas_selecionadas))
st.table(df_acima_de_60.round(2))

st.markdown("# Lista porcentagem dos descritores trabalhados no " + str(salas_selecionadas))
st.table(df_descritores_mean.sort_values('Porcentagem', ascending=False).round(2))

with st.sidebar:
    st.markdown("Links importantes:")
    st.page_link(
        "https://download.inep.gov.br/educacao_basica/prova_brasil_saeb/menu_do_professor/o_que_cai_nas_provas/Matriz_de_Referencia_de_Matematica.pdf",
        label="Descritores Matemática", icon="🌎")
    st.page_link(
        "https://download.inep.gov.br/educacao_basica/prova_brasil_saeb/menu_do_professor/o_que_cai_nas_provas/Matriz_de_Referencia_de_Lingua_Portuguesa.pdf",
        label="Descritores Português", icon="🌎")

    st.text("Desenvolvido por Mauricio A. Ribeiro")
    st.text("EMAIL: mau.ap.ribeiro@gmail.com")
