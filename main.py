import streamlit as st
import pandas as pd
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components

path = "html_files"

st.set_page_config(layout="wide")
st.title("CIVic Visualization Tool")
st.markdown("It would take about 20s to load...")


@st.cache_data
def load_unique_civic_data():
    columns = ["gene", "variant", "disease", "drugs"]
    df_ = pd.read_csv("data/civic_data_unique.tsv").drop_duplicates(
        subset=columns)
    df_ = df_[df_["evidence_direction"] == "Supports"]
    df_ = df_[df_["clinical_significance"].isin(["Positive", "Sensitivity"])]
    df_ = df_[~df_["variant"].isin(["MUTATION", "FRAMESHIFT TRUNCATION",
                                    'LOSS-OF-FUNCTION', "PROMOTER METHYLATION",
                                    'OVEREXPRESSION', 'LOSS', 'EXPRESSION',
                                    'INTERNAL DUPLICATION', 'AMPLIFICATION',
                                    'UNDEREXPRESSION', 'REARRANGEMENT',
                                    'POLYMORPHISM', 'PROMOTER HYPERMETHYLATION',
                                    'ISOFORM EXPRESSION', 'NUCLEAR EXPRESSION',
                                    'WILD TYPE', 'PHOSPHORYLATION',
                                    'FRAMESHIFT MUTATION',
                                    'DELETERIOUS MUTATION',
                                    'BIALLELIC INACTIVATION',
                                    'TRUNCATING FUSION',
                                    'FUSION', 'ALTERNATIVE TRANSCRIPT (ATI)',
                                    'WILDTYPE',
                                    'COPY NUMBER VARIATION', 'RARE MUTATION'
                                    ])]
    df_ = df_[columns].dropna().astype(str)
    df_["gene-variant"] = df_["gene"] + "-" + df_["variant"]
    df_ = df_[df_.groupby('disease')['disease'].transform('size') > 10]
    df_ = df_[df_.groupby('gene')['gene'].transform('size') > 10]

    return df_.head(n=200)


df_unique = load_unique_civic_data()

@st.cache_data
def creat_graph():
    G = nx.Graph()
    nodes = {}
    node = 0
    for index, row in df_unique.iterrows():
        if row["disease"] not in nodes.keys():
            disease = row["disease"]
            nodes[disease] = node
            G.add_node(node, title=f"disease:{disease}", label=row["disease"],
                       group=1)
            node += 1
        if row["gene"] not in nodes.keys():
            nodes[row["gene"]] = node
            G.add_node(node, title="gene:" + row["gene"],
                       label=row["gene"], group=2)
            node += 1
        if row["gene-variant"] not in nodes.keys():
            nodes[row["gene-variant"]] = node
            G.add_node(node, title="variant:" + row["gene-variant"],
                       label=row["gene-variant"], group=3)
            node += 1
        if row["drugs"] not in nodes.keys():
            nodes[row["drugs"]] = node
            G.add_node(node, title="therapy:" + row["drugs"],
                       label=row["gene-variant"], group=4)
            node += 1
        disease_node = nodes[row["disease"]]
        gene_node = nodes[row["gene"]]
        variant_node = nodes[row["gene-variant"]]
        therapy_node = nodes[row["drugs"]]
        G.add_edge(disease_node, variant_node)
        G.add_edge(gene_node, variant_node)
        G.add_edge(therapy_node, variant_node)
    nt = Network(width='100%', height="100vh")
    nt.from_nx(G)
    nt.save_graph(f'{path}/all_network.html')
    return


creat_graph()
HtmlFile = open(f'{path}/all_network.html', 'r', encoding='utf-8')
components.html(HtmlFile.read(), height=800)
