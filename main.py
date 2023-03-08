import streamlit as st
import altair as alt
import pandas as pd
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components


st.set_page_config(layout="wide")
st.title("CIVic Visualization Tool")

# load data 
df = pd.read_csv("data/civic_data.tsv")
df_unique = pd.read_csv("data/civic_data_unique.tsv")
df_unique = df_unique[["gene", "variant", "drugs","disease"]]
df_unique = df_unique.drop_duplicates()
df_unique = df_unique.dropna()
df_unique["gene-variant"] = df_unique["gene"] + "-" + df_unique["variant"]
path = "html_files"
### Number of Records of All Diseases Reported in a Year ###
@st.cache_data
def creat_graph():
    G = nx.Graph()
    nodes = {}
    node = 0
    for index, row in df_unique.iterrows():
        if row["disease"] not in nodes.keys():
            disease = row["disease"]
            nodes[disease] = node
            G.add_node(node, title=f"disease:{disease}", label=row["disease"], group=1)
            node += 1
        if row["gene"] not in nodes.keys():
            nodes[row["gene"]] = node
            G.add_node(node, title="gene:"+row["gene"], label=row["gene"], group=2)
            node += 1
        if row["gene-variant"] not in nodes.keys():
            nodes[row["gene-variant"]] = node
            G.add_node(node, title="variant:"+row["gene-variant"],label=row["gene-variant"], group=3)
            node += 1
        if row["drugs"] not in nodes.keys():
            nodes[row["drugs"]] = node
            G.add_node(node, title="therapy:"+row["drugs"],label=row["gene-variant"], group=4)
            node += 1
        disease_node = nodes[row["disease"]]
        gene_node = nodes[row["gene"]]
        variant_node = nodes[row["gene-variant"]]
        therapy_node = nodes[row["drugs"]]
        G.add_edge(disease_node,variant_node)
        G.add_edge(gene_node,variant_node)
        G.add_edge(therapy_node,variant_node)
    nt = Network(width='100%', height="100vh")
    nt.from_nx(G)
    nt.repulsion(
        node_distance=420,
        central_gravity=0.33,
        spring_length=110,
        spring_strength=0.10,
        damping=0.95
    )
    nt.save_graph(f'{path}/all_network.html')
    return



creat_graph()
HtmlFile = open(f'{path}/all_network.html', 'r', encoding='utf-8')
components.html(HtmlFile.read(), height=900)






