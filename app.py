import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

COR_AZUL = "#1976D2"
COR_VERDE = "#2E7D32"
COR_VERMELHO = "#C62828"
COR_ROXO = "#6A1B9A"



# ==================================================
# CONFIGURAÇÃO DA PÁGINA
# ==================================================

st.set_page_config(
    page_title="Indicadores de Saúde Pública no Brasil",
    page_icon="🏥",
    layout="wide"
)



# ==================================================
# ESTILO VISUAL
# ==================================================

st.markdown("""
<style>

/* FUNDO */
.stApp {
    background-color: #F4F8F5;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background-color: #2E7D32;
}

section[data-testid="stSidebar"] * {
    color: white;
}

/* TÍTULOS */
h1, h2, h3 {
    color: #1B5E20 !important;
}

/* KPI */
[data-testid="stMetric"] {
    background: white;
    border-radius: 15px;
    padding: 18px;
    border-left: 8px solid #43A047;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

/* DATAFRAME */
[data-testid="stDataFrame"] {
    background: white;
    border-radius: 12px;
}

/* LINHAS DIVISÓRIAS */
hr {
    border: none;
    border-top: 1px solid #D6EAD8;
}

/* CONTAINER */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>

/* Chips dos multiselects */
.stMultiSelect [data-baseweb="tag"] {
    background-color: #2E7D32 !important;
    color: white !important;
    border: none !important;
}

/* Texto dentro do chip */
.stMultiSelect [data-baseweb="tag"] span {
    color: white !important;
}

/* X de remover */
.stMultiSelect [data-baseweb="tag"] svg {
    fill: white !important;
}

/* Campo do multiselect */
.stMultiSelect div[data-baseweb="select"] > div {
    background-color: white !important;
    color: black !important;
}
            
            /* Títulos da sidebar */

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] p {
    color: white !important;
}

            

</style>
""", unsafe_allow_html=True)



# ==================================================
# LEITURA DOS DADOS
# ==================================================

@st.cache_data
def carregar_dados():

    df = pd.read_csv(
        "dados/simulacao_saude_publica_brasil.csv"
    )

    df["data"] = pd.to_datetime(df["data"])

    return df


df = carregar_dados()

# ==================================================
# SIDEBAR
# ==================================================

st.sidebar.title("🏥 Saúde Pública")

pagina = st.sidebar.radio(
    "Navegação",
    [
        "🏠 Visão Geral",
        "❤️ Expectativa de Vida",
        "📉 Mortalidade",
        "💉 Vacinação",
        "🏥 Infraestrutura",
        "🔍 Correlações",
        "📋 Tabela Dinâmica",
        "📝 Conclusão Executiva"
    ]
)

st.sidebar.divider()

st.sidebar.subheader("Filtros")

regioes = st.sidebar.multiselect(
    "Região",
    options=sorted(df["regiao"].unique()),
    default=sorted(df["regiao"].unique())
)

ufs = st.sidebar.multiselect(
    "UF",
    options=sorted(df["uf"].unique()),
    default=sorted(df["uf"].unique())
)

anos = st.sidebar.multiselect(
    "Ano",
    options=sorted(df["ano"].unique()),
    default=sorted(df["ano"].unique())
)

# ==================================================
# FILTRO PRINCIPAL
# ==================================================

df_filtrado = df[
    (df["regiao"].isin(regioes))
    &
    (df["uf"].isin(ufs))
    &
    (df["ano"].isin(anos))
]

# ==================================================
# PÁGINA INICIAL
# ==================================================

if pagina == "🏠 Visão Geral":

    st.markdown("""
# 🏥 Saúde Pública no Brasil

### Dashboard de Indicadores (2015–2024)
""")


    st.divider()

    st.subheader("📈 Indicadores-Chave (KPIs)")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Expectativa Média de Vida",
            f"{df_filtrado['expectativa_vida'].mean():.2f}"
        )

    with col2:
        st.metric(
            "Taxa Média de Mortalidade",
            f"{df_filtrado['taxa_mortalidade'].mean():.2f}"
        )

    with col3:
        st.metric(
            "Cobertura Vacinal Média",
            f"{df_filtrado['cobertura_vacinal'].mean():.2f}%"
        )

    col4, col5, col6 = st.columns(3)

    with col4:
        st.metric(
            "Média de Leitos",
            f"{df_filtrado['leitos_hospitalares'].mean():.0f}"
        )

    with col5:
        st.metric(
            "Taxa Média de Internação",
            f"{df_filtrado['taxa_internacao'].mean():.2f}"
        )

    with col6:

        estado_critico = (
            df_filtrado
            .groupby("uf")["taxa_mortalidade"]
            .mean()
            .sort_values(ascending=False)
            .index[0]
        )

        st.metric(
            "UF Mais Vulnerável",
            estado_critico
        )

    st.divider()

    st.subheader("📋 Base de Dados")

    st.dataframe(
        df_filtrado.head(20),
        use_container_width=True
    )

    st.divider()

    st.subheader("📌 Resumo Executivo")

    st.info("""
    Utilize os filtros laterais para explorar os indicadores por região, estado e período.

    As páginas seguintes apresentam análises detalhadas de expectativa de vida, mortalidade, vacinação, infraestrutura hospitalar, correlações estatísticas e uma conclusão executiva baseada nos resultados obtidos.
    """)

    # ==================================================
# EXPECTATIVA DE VIDA
# ==================================================

elif pagina == "❤️ Expectativa de Vida":

    st.title("❤️ Expectativa de Vida")

    media_ano = (
        df_filtrado
        .groupby("ano")["expectativa_vida"]
        .mean()
        .reset_index()
    )

    fig, ax = plt.subplots(figsize=(12,6))

    sns.lineplot(
        data=media_ano,
        x="ano",
        y="expectativa_vida",
        marker="o",
        linewidth=3,
        color=COR_AZUL,
        ax=ax
    )

    ax.set_title(
        "Evolução da Expectativa de Vida no Brasil",
        fontsize=16,
        fontweight="bold"
    )

    ax.set_xlabel("Ano")
    ax.set_ylabel("Expectativa de Vida")

    ax.grid(
        True,
        linestyle="--",
        alpha=0.5
    )

    ax.set_ylim(72,75)

    st.pyplot(fig)

    st.markdown("""
    ### Interpretação

    O gráfico demonstra que a expectativa de vida no Brasil apresentou oscilações ao longo do período entre 2015 e 2024.

    Observa-se crescimento até 2018, ano em que foi registrado o maior valor médio.

    Após esse período ocorre uma redução do indicador, especialmente entre 2020 e 2022.

    Esse comportamento pode estar relacionado aos impactos da pandemia da COVID-19 sobre os indicadores de saúde da população.
    """)

# ==================================================
# MORTALIDADE
# ==================================================

elif pagina == "📉 Mortalidade":

    st.title("📉 Mortalidade")

    # --------------------------------------------
    # Mortalidade por Região
    # --------------------------------------------

    st.subheader("Taxa Média de Mortalidade por Região")

    mortalidade_regiao = (
        df_filtrado
        .groupby("regiao")["taxa_mortalidade"]
        .mean()
        .sort_values(ascending=False)
        .reset_index()
    )

    fig, ax = plt.subplots(figsize=(10,6))

    sns.barplot(
        data=mortalidade_regiao,
        x="regiao",
        y="taxa_mortalidade",
        hue="regiao",
        palette="Blues",
        legend=False,
        ax=ax
    )

    for i, v in enumerate(
        mortalidade_regiao["taxa_mortalidade"]
    ):
        ax.text(
            i,
            v + 0.02,
            f"{v:.2f}",
            ha="center",
            fontsize=10
        )

    ax.set_title(
        "Taxa Média de Mortalidade por Região",
        fontsize=16,
        fontweight="bold"
    )

    ax.set_xlabel("Região")
    ax.set_ylabel("Taxa Média de Mortalidade")

    ax.set_ylim(0,10)

    ax.grid(
        axis="y",
        linestyle="--",
        alpha=0.3
    )

    st.pyplot(fig)

    st.markdown("""
    ### Interpretação

    As regiões Centro-Oeste e Sudeste apresentam os maiores índices médios de mortalidade.

    O Nordeste apresenta o menor valor médio observado.

    Apesar das diferenças, os valores permanecem relativamente próximos, indicando certa uniformidade nacional no indicador.
    """)

    st.divider()

    # --------------------------------------------
    # Evolução Temporal da Mortalidade
    # --------------------------------------------

    st.subheader("Evolução Temporal da Mortalidade")

    temporal_mortalidade = (
        df_filtrado
        .groupby("ano")["taxa_mortalidade"]
        .mean()
        .reset_index()
    )

    fig, ax = plt.subplots(figsize=(12,6))

    sns.lineplot(
        data=temporal_mortalidade,
        x="ano",
        y="taxa_mortalidade",
        marker="o",
        linewidth=3,
        color=COR_VERMELHO,
        ax=ax
    )

    for _, row in temporal_mortalidade.iterrows():

        ax.text(
            row["ano"],
            row["taxa_mortalidade"] + 0.02,
            f"{row['taxa_mortalidade']:.2f}",
            ha="center",
            fontsize=9
        )

    ax.set_title(
        "Evolução Temporal da Taxa de Mortalidade",
        fontsize=16,
        fontweight="bold"
    )

    ax.set_xlabel("Ano")
    ax.set_ylabel("Taxa Média de Mortalidade")

    ax.set_ylim(
        temporal_mortalidade["taxa_mortalidade"].min() - 0.2,
        temporal_mortalidade["taxa_mortalidade"].max() + 0.2
    )

    ax.grid(
        True,
        linestyle="--",
        alpha=0.4
    )

    st.pyplot(fig)

    st.markdown("""
    ### Interpretação

    O gráfico apresenta oscilações da mortalidade ao longo da série histórica.

    O principal pico ocorre em 2018.

    Também são observadas elevações próximas ao período da pandemia da COVID-19.

    O comportamento demonstra como eventos epidemiológicos podem impactar diretamente os indicadores de saúde pública.
    """)

    st.divider()

    st.subheader("📋 Tabela de Mortalidade por Região")

    tabela_mortalidade = (
        df_filtrado
        .groupby("regiao")["taxa_mortalidade"]
        .mean()
        .reset_index()
        .sort_values(
            by="taxa_mortalidade",
            ascending=False
        )
    )

    st.dataframe(
        tabela_mortalidade,
        use_container_width=True
    )

    # ==================================================
# VACINAÇÃO
# ==================================================

elif pagina == "💉 Vacinação":

    st.title("💉 Cobertura Vacinal")

    # --------------------------------------------
    # Cobertura Vacinal por Região
    # --------------------------------------------

    st.subheader("Cobertura Vacinal Média por Região")

    vacina_regiao = (
        df_filtrado
        .groupby("regiao")["cobertura_vacinal"]
        .mean()
        .sort_values(ascending=False)
        .reset_index()
    )

    fig, ax = plt.subplots(figsize=(10,6))

    sns.barplot(
        data=vacina_regiao,
        x="regiao",
        y="cobertura_vacinal",
        hue="regiao",
        palette="Greens",
        legend=False,
        ax=ax
    )

    for i, v in enumerate(
        vacina_regiao["cobertura_vacinal"]
    ):
        ax.text(
            i,
            v + 0.05,
            f"{v:.2f}",
            ha="center",
            fontsize=10
        )

    ax.set_title(
        "Cobertura Vacinal Média por Região",
        fontsize=16,
        fontweight="bold"
    )

    ax.set_xlabel("Região")
    ax.set_ylabel("Cobertura Vacinal (%)")

    ax.set_ylim(72,75)

    ax.grid(
        axis="y",
        linestyle="--",
        alpha=0.3
    )

    st.pyplot(fig)

    st.markdown("""
    ### Interpretação

    A região Norte apresenta a maior cobertura vacinal média.

    Sul e Sudeste apresentam os menores valores médios.

    Apesar disso, a diferença entre regiões é relativamente pequena,
    demonstrando estabilidade nacional da vacinação.
    """)

    st.divider()

    # --------------------------------------------
    # Vacinação x Mortalidade
    # --------------------------------------------

    st.subheader("Relação entre Vacinação e Mortalidade")

    vacina_mortalidade = (
        df_filtrado
        .groupby("regiao")[
            ["cobertura_vacinal", "taxa_mortalidade"]
        ]
        .mean()
        .reset_index()
    )

    fig, ax = plt.subplots(figsize=(10,6))

    sns.scatterplot(
        data=vacina_mortalidade,
        x="cobertura_vacinal",
        y="taxa_mortalidade",
        hue="regiao",
        s=300,
        ax=ax
    )

    for i in range(len(vacina_mortalidade)):

        ax.text(
            vacina_mortalidade["cobertura_vacinal"][i] + 0.02,
            vacina_mortalidade["taxa_mortalidade"][i],
            vacina_mortalidade["regiao"][i],
            fontsize=10
        )

    ax.set_title(
        "Relação entre Cobertura Vacinal e Mortalidade",
        fontsize=16,
        fontweight="bold"
    )

    ax.set_xlabel("Cobertura Vacinal Média (%)")
    ax.set_ylabel("Taxa Média de Mortalidade")

    ax.grid(
        True,
        linestyle="--",
        alpha=0.5
    )

    st.pyplot(fig)

    st.markdown("""
    ### Interpretação

    Os dados sugerem que regiões com menores índices de vacinação
    tendem a apresentar mortalidade mais elevada.

    Entretanto, a vacinação não é o único fator que influencia
    os indicadores de mortalidade.

    Infraestrutura hospitalar, acesso à saúde e fatores
    socioeconômicos também possuem impacto relevante.
    """)

    st.divider()

    # --------------------------------------------
    # Top 10 Estados
    # --------------------------------------------

    st.subheader(
        "Top 10 Estados com Maior Cobertura Vacinal"
    )

    vacinacao_estado = (
        df_filtrado
        .groupby("uf")["cobertura_vacinal"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig, ax = plt.subplots(figsize=(12,6))

    sns.barplot(
        data=vacinacao_estado,
        x="uf",
        y="cobertura_vacinal",
        hue="uf",
        palette="Greens_r",
        legend=False,
        ax=ax
    )

    for i, v in enumerate(
        vacinacao_estado["cobertura_vacinal"]
    ):
        ax.text(
            i,
            v + 0.03,
            f"{v:.2f}",
            ha="center",
            fontsize=10
        )

    ax.set_title(
        "Top 10 Estados com Maior Cobertura Vacinal",
        fontsize=16,
        fontweight="bold"
    )

    ax.set_xlabel("Estado")
    ax.set_ylabel("Cobertura Vacinal Média (%)")

    ax.set_ylim(
        vacinacao_estado["cobertura_vacinal"].min() - 0.3,
        vacinacao_estado["cobertura_vacinal"].max() + 0.3
    )

    ax.grid(
        axis="y",
        linestyle="--",
        alpha=0.4
    )

    st.pyplot(fig)

    st.markdown("""
    ### Interpretação

    Os estados apresentados registram os maiores índices
    médios de vacinação do período analisado.

    As diferenças são pequenas, demonstrando elevado nível
    de cobertura vacinal entre os líderes do ranking.
    """)

# ==================================================
# INFRAESTRUTURA
# ==================================================

elif pagina == "🏥 Infraestrutura":

    st.title("🏥 Infraestrutura Hospitalar")

    infraestrutura = (
        df_filtrado
        .groupby("regiao")["leitos_hospitalares"]
        .mean()
        .sort_values(ascending=False)
        .reset_index()
    )

    fig, ax = plt.subplots(figsize=(10,6))

    sns.barplot(
        data=infraestrutura,
        x="regiao",
        y="leitos_hospitalares",
        hue="regiao",
        palette="Purples",
        legend=False,
        ax=ax
    )

    for i, v in enumerate(
        infraestrutura["leitos_hospitalares"]
    ):
        ax.text(
            i,
            v + 20,
            f"{v:.0f}",
            ha="center",
            fontsize=10
        )

    ax.set_title(
        "Média de Leitos Hospitalares por Região",
        fontsize=16,
        fontweight="bold"
    )

    ax.set_xlabel("Região")
    ax.set_ylabel("Quantidade Média de Leitos")

    ax.set_ylim(5700,6200)

    ax.grid(
        axis="y",
        linestyle="--",
        alpha=0.4
    )

    st.pyplot(fig)

    st.markdown("""
    ### Interpretação

    A distribuição dos leitos hospitalares não ocorre de forma
    completamente uniforme entre as regiões brasileiras.

    Regiões com maior disponibilidade de leitos possuem
    maior capacidade potencial de atendimento hospitalar.

    A infraestrutura é um dos fatores fundamentais para
    resposta a crises sanitárias e aumento da qualidade
    dos serviços de saúde.
    """)

    st.divider()

    st.subheader("Resumo da Infraestrutura")

    st.dataframe(
        infraestrutura,
        use_container_width=True
    )

    # ==================================================
# CORRELAÇÕES
# ==================================================

elif pagina == "🔍 Correlações":

    st.title("🔍 Correlações entre Indicadores")

    corr = (
        df_filtrado
        .select_dtypes(include=np.number)
        .corr()
    )

    fig, ax = plt.subplots(figsize=(14,8))

    sns.heatmap(
        corr,
        annot=True,
        cmap="RdBu_r",
        fmt=".2f",
        linewidths=0.5,
        square=True,
        cbar_kws={"label":"Correlação"},
        ax=ax
    )

    ax.set_title(
        "Correlação entre Indicadores de Saúde Pública",
        fontsize=16,
        fontweight="bold",
        pad=20
    )

    plt.xticks(rotation=45, ha="right")
    plt.yticks(rotation=0)

    st.pyplot(fig)

    st.markdown("""
    ### Interpretação

    O heatmap demonstra que a expectativa de vida apresenta correlação negativa com a taxa de mortalidade.

    Também é possível observar uma relação negativa entre cobertura vacinal e mortalidade.

    Esses resultados sugerem que melhores indicadores preventivos tendem a estar associados a melhores condições gerais de saúde da população.

    Algumas variáveis apresentam correlação fraca, indicando influência de fatores adicionais não presentes no dataset.
    """)

# ==================================================
# TABELA DINÂMICA
# ==================================================

elif pagina == "📋 Tabela Dinâmica":

    st.title("📋 Tabela Dinâmica")

    tabela_dinamica = (
        df_filtrado.pivot_table(
            values="taxa_mortalidade",
            index="regiao",
            columns="ano",
            aggfunc="mean"
        )
        .round(2)
    )

    st.subheader(
        "Taxa Média de Mortalidade por Região e Ano"
    )

    st.dataframe(
        tabela_dinamica,
        use_container_width=True
    )

    st.markdown("""
    ### Interpretação

    O Centro-Oeste e o Sudeste apresentam alguns dos maiores índices médios de mortalidade ao longo da série histórica.

    Também é possível observar aumentos em períodos específicos, especialmente próximos a eventos epidemiológicos relevantes.

    Norte e Nordeste frequentemente apresentam valores inferiores quando comparados às demais regiões.

    Os resultados reforçam a importância de análises regionais para o planejamento de políticas públicas de saúde.
    """)

# ==================================================
# CONCLUSÃO EXECUTIVA
# ==================================================

elif pagina == "📝 Conclusão Executiva":

    st.title("📝 Conclusão Executiva")

    st.success("""
    A análise dos indicadores de saúde pública no Brasil permitiu identificar padrões importantes relacionados à mortalidade, vacinação, expectativa de vida e infraestrutura hospitalar entre 2015 e 2024.
    """)

    st.subheader("Principais Achados")

    st.markdown("""
    ✅ Centro-Oeste e Sudeste apresentaram os maiores índices médios de mortalidade.

    ✅ Norte apresentou a maior cobertura vacinal média.

    ✅ Expectativa de vida apresentou oscilações ao longo da série histórica.

    ✅ Os indicadores sofreram impactos relevantes próximos ao período da pandemia da COVID-19.

    ✅ A infraestrutura hospitalar apresenta diferenças regionais que podem impactar a capacidade de atendimento.

    ✅ Existe relação negativa entre vacinação e mortalidade, embora outros fatores também influenciem os resultados.
    """)

    st.subheader("Conclusão")

    st.markdown("""
    Os resultados demonstram que a saúde pública brasileira apresenta diferenças regionais relevantes que devem ser consideradas no planejamento de políticas públicas.

    A vacinação mostrou-se um importante indicador preventivo, enquanto a infraestrutura hospitalar permanece como elemento fundamental para suporte ao sistema de saúde.

    A análise temporal evidenciou como eventos epidemiológicos podem impactar diretamente indicadores populacionais como mortalidade e expectativa de vida.

    O projeto permitiu aplicar técnicas de tratamento, análise e visualização de dados utilizando Python, Pandas, Matplotlib, Seaborn e Streamlit, transformando dados em informações úteis para apoio à tomada de decisão.
    """)

    st.divider()

    st.info(
        "Projeto G2 — Análise de Indicadores de Saúde Pública no Brasil"
    )