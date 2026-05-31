import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# -------------------------
# CONFIGURAÇÃO DA PÁGINA
# -------------------------

st.set_page_config(
    page_title='Indicadores de Saúde Pública no Brasil',
    layout='wide'
)

# -------------------------
# TÍTULO
# -------------------------

st.title('📊 Indicadores de Saúde Pública no Brasil')

st.markdown("""
Este dashboard apresenta uma análise dos principais indicadores de saúde pública no Brasil entre os anos de 2015 e 2024.

Foram analisados indicadores relacionados à:
- mortalidade;
- expectativa de vida;
- cobertura vacinal;
- infraestrutura hospitalar;
- internações.

O objetivo do projeto é identificar padrões, tendências e relações entre os indicadores de saúde pública nas regiões brasileiras.
""")

# -------------------------
# LEITURA DOS DADOS
# -------------------------

df = pd.read_csv('dados/simulacao_saude_publica_brasil.csv')

# -------------------------
# SIDEBAR
# -------------------------

st.sidebar.title('🏥 Saúde Pública')

pagina = st.sidebar.radio(
    'Navegação',
    [
        '🏠 Visão Geral',
        '❤️ Expectativa de Vida',
        '📉 Mortalidade',
        '💉 Vacinação',
        '🏥 Infraestrutura',
        '🔍 Correlações',
        '📋 Tabela Dinâmica',
        '📝 Conclusão'
    ]
)

st.sidebar.divider()

st.sidebar.subheader('Filtros')

regioes = st.sidebar.multiselect(
    'Região',
    options=sorted(df['regiao'].unique()),
    default=sorted(df['regiao'].unique())
)

anos = st.sidebar.multiselect(
    'Ano',
    options=sorted(df['ano'].unique()),
    default=sorted(df['ano'].unique())
)

ufs = st.sidebar.multiselect(
    'UF',
    options=sorted(df['uf'].unique()),
    default=sorted(df['uf'].unique())
)

# -------------------------
# FILTROS
# -------------------------

df_filtrado = df[
    (df['regiao'].isin(regioes)) &
    (df['ano'].isin(anos)) &
    (df['uf'].isin(ufs))
]

# -------------------------
# VISÃO GERAL
# -------------------------

if pagina == '🏠 Visão Geral':

    st.header('📊 Visão Geral')

    st.markdown("""
    Este dashboard apresenta uma análise dos principais indicadores de saúde pública
    no Brasil entre 2015 e 2024.

    A análise contempla expectativa de vida, mortalidade, vacinação,
    infraestrutura hospitalar e internações, permitindo identificar padrões
    regionais e tendências ao longo do tempo.
    """)

    st.divider()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            'Expectativa de Vida Média',
            f"{df_filtrado['expectativa_vida'].mean():.2f}"
        )

    with col2:
        st.metric(
            'Cobertura Vacinal Média',
            f"{df_filtrado['cobertura_vacinal'].mean():.2f}%"
        )

    with col3:
        st.metric(
            'Média de Leitos',
            f"{df_filtrado['leitos_hospitalares'].mean():.2f}"
        )

    with col4:
        st.metric(
            'Taxa Média de Internação',
            f"{df_filtrado['taxa_internacao'].mean():.2f}"
        )

    st.divider()

    st.subheader('Resumo Executivo')

    st.info("""
    Utilize os filtros laterais para explorar os indicadores de saúde pública
    por região, estado e período. As demais seções apresentam análises
    específicas sobre expectativa de vida, mortalidade, vacinação,
    infraestrutura hospitalar e correlações entre os indicadores.
    """)

# -------------------------
# PÁGINAS FUTURAS
# -------------------------

elif pagina == '❤️ Expectativa de Vida':

    st.header('❤️ Expectativa de Vida')

    exp_vida = (
        df_filtrado
        .groupby('ano')['expectativa_vida']
        .mean()
        .reset_index()
    )

    fig, ax = plt.subplots(figsize=(10, 5))

    sns.lineplot(
        data=exp_vida,
        x='ano',
        y='expectativa_vida',
        marker='o',
        linewidth=3,
        color='#1E88E5',
        ax=ax
    )

    ax.set_title('Evolução da Expectativa de Vida')
    ax.set_xlabel('Ano')
    ax.set_ylabel('Expectativa de Vida')

    st.pyplot(fig)

    st.markdown("""
    ### Interpretação

    O gráfico demonstra que a expectativa de vida no Brasil apresentou oscilações ao longo do período analisado, sem uma tendência contínua de crescimento.

    O maior valor médio foi observado em 2018. A partir desse período ocorre uma redução do indicador, com queda mais perceptível entre 2020 e 2022.

    Essa diminuição pode estar relacionada aos impactos da pandemia da COVID-19, que elevou os índices de mortalidade e afetou diretamente a expectativa de vida da população.

    Embora haja uma leve recuperação em alguns momentos posteriores, o indicador encerra o período analisado abaixo do pico registrado em 2018.
    """)

elif pagina == '📉 Mortalidade':

    st.header('📉 Mortalidade')

    # -------------------------
    # Mortalidade por Região
    # -------------------------

    st.subheader('Taxa Média de Mortalidade por Região')

    mortalidade_regiao = (
        df_filtrado
        .groupby('regiao')['taxa_mortalidade']
        .mean()
        .reset_index()
        .sort_values('taxa_mortalidade', ascending=False)
    )

    fig, ax = plt.subplots(figsize=(10, 5))

    sns.barplot(
        data=mortalidade_regiao,
        x='regiao',
        y='taxa_mortalidade',
        color='#E53935',
        ax=ax
    )

    ax.set_xlabel('Região')
    ax.set_ylabel('Taxa de Mortalidade')
    ax.set_title('Taxa Média de Mortalidade por Região')

    st.pyplot(fig)

    st.markdown("""
    **Interpretação**

    O gráfico evidencia diferenças regionais nos níveis médios de mortalidade. As regiões com valores mais elevados apresentam maior impacto dos fatores associados à saúde pública, enquanto regiões com taxas menores demonstram indicadores relativamente mais favoráveis.

    Essas diferenças reforçam a importância da análise regional para compreender desigualdades na oferta de serviços de saúde e nas condições de vida da população.
    """)

    st.divider()

    # -------------------------
    # Evolução Temporal
    # -------------------------

    st.subheader('Evolução Temporal da Mortalidade')

    mortalidade_ano = (
        df_filtrado
        .groupby('ano')['taxa_mortalidade']
        .mean()
        .reset_index()
    )

    fig, ax = plt.subplots(figsize=(10, 5))

    sns.lineplot(
        data=mortalidade_ano,
        x='ano',
        y='taxa_mortalidade',
        marker='o',
        linewidth=3,
        color='#E53935',
        ax=ax
    )

    ax.set_xlabel('Ano')
    ax.set_ylabel('Taxa de Mortalidade')
    ax.set_title('Evolução da Taxa Média de Mortalidade')

    st.pyplot(fig)

    st.markdown("""
    **Interpretação**

    Observa-se uma variação da mortalidade ao longo do período analisado, incluindo um pico em 2018. Após esse período, os valores apresentam oscilações sem tendência contínua de crescimento.

    O comportamento do indicador demonstra que fatores epidemiológicos, socioeconômicos e estruturais podem influenciar a mortalidade de forma diferente em cada período analisado.
    """)

elif pagina == '💉 Vacinação':

    st.header('💉 Cobertura Vacinal')

    # -------------------------
    # Cobertura por Região
    # -------------------------

    st.subheader('Cobertura Vacinal Média por Região')

    vac_regiao = (
        df_filtrado
        .groupby('regiao')['cobertura_vacinal']
        .mean()
        .reset_index()
        .sort_values('cobertura_vacinal', ascending=False)
    )

    fig, ax = plt.subplots(figsize=(10, 5))

    sns.barplot(
        data=vac_regiao,
        x='regiao',
        y='cobertura_vacinal',
        color='#43A047',
        ax=ax
    )

    ax.set_xlabel('Região')
    ax.set_ylabel('Cobertura Vacinal (%)')
    ax.set_title('Cobertura Vacinal Média por Região')

    st.pyplot(fig)

    st.markdown("""
    **Interpretação**

    Observam-se diferenças relativamente pequenas entre as regiões, indicando uma distribuição relativamente equilibrada da cobertura vacinal no país.

    Ainda assim, algumas regiões apresentam desempenho superior, demonstrando maior alcance das campanhas de imunização.
    """)

    st.divider()

    # -------------------------
    # Vacinação x Mortalidade
    # -------------------------

    st.subheader('Relação entre Vacinação e Mortalidade')

    relacao = (
        df_filtrado
        .groupby('regiao')[['cobertura_vacinal', 'taxa_mortalidade']]
        .mean()
        .reset_index()
    )

    fig, ax = plt.subplots(figsize=(10, 5))

    sns.scatterplot(
        data=relacao,
        x='cobertura_vacinal',
        y='taxa_mortalidade',
        s=150,
        color='#43A047',
        ax=ax
    )

    for _, row in relacao.iterrows():
        ax.text(
            row['cobertura_vacinal'],
            row['taxa_mortalidade'],
            row['regiao']
        )

    ax.set_xlabel('Cobertura Vacinal (%)')
    ax.set_ylabel('Taxa de Mortalidade')
    ax.set_title('Vacinação x Mortalidade')

    st.pyplot(fig)

    st.markdown("""
    **Interpretação**

    A comparação entre vacinação e mortalidade evidencia que regiões com maior cobertura vacinal nem sempre apresentam as maiores taxas de mortalidade.

    O resultado sugere que a mortalidade é influenciada por diversos fatores além da vacinação, como infraestrutura de saúde, condições socioeconômicas e perfil demográfico da população.
    """)

    st.divider()

    # -------------------------
    # Top Estados
    # -------------------------

    st.subheader('Top 10 Estados com Maior Cobertura Vacinal')

    top_estados = (
        df_filtrado
        .groupby('uf')['cobertura_vacinal']
        .mean()
        .reset_index()
        .sort_values('cobertura_vacinal', ascending=False)
        .head(10)
    )

    fig, ax = plt.subplots(figsize=(10, 5))

    sns.barplot(
        data=top_estados,
        x='cobertura_vacinal',
        y='uf',
        color='#43A047',
        ax=ax
    )

    ax.set_xlabel('Cobertura Vacinal (%)')
    ax.set_ylabel('UF')
    ax.set_title('Estados com Maior Cobertura Vacinal')

    st.pyplot(fig)

    st.markdown("""
    **Interpretação**

    Os estados presentes no topo do ranking apresentam os maiores níveis médios de cobertura vacinal do período analisado.

    O resultado evidencia diferenças entre unidades federativas e demonstra a importância das estratégias regionais para ampliar o alcance da imunização.
    """)

elif pagina == '🏥 Infraestrutura':
    st.header('🏥 Infraestrutura')
    st.write('Em construção.')

elif pagina == '🔍 Correlações':
    st.header('🔍 Correlações')
    st.write('Em construção.')

elif pagina == '📋 Tabela Dinâmica':
    st.header('📋 Tabela Dinâmica')
    st.write('Em construção.')

elif pagina == '📝 Conclusão':
    st.header('📝 Conclusão')
    st.write('Em construção.')