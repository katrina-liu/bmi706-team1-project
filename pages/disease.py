import streamlit as st
import networkx as nx
import nx_altair as nxa
from pyvis.network import Network
import streamlit.components.v1 as components
import pandas as pd

def load_unique_civic_data():
    columns = ["gene","variant","disease","drugs"]
    df = pd.read_csv("data/civic_data_unique.tsv")[columns].drop_duplicates()
    return df[df["disease"].notna()]


df_unique = load_unique_civic_data()
disease = st.text_input("Search a disease here:")

if len(disease) > 0 and disease in df_unique["disease"].unique():
    print(disease)
    st.title(disease)
    gene_variant_tab, variant_therapy_tab, time_series_tab = \
        st.tabs(["Gene-Variant", "Variant-Therapy", "Time Series"])
    with gene_variant_tab:
        st.header("Disease Gene Variant Network")
        # TODO: insert network
        # Generate a random graph
        df_dgv_network = df_unique[df_unique["disease"]==disease]
        print(df_dgv_network)
        G = nx.Graph()
        G.add_node(0, size=20, title='disease', group=0, label=disease)
        node = 1
        gene_node_index = {}
        for index,row in df_dgv_network.iterrows():
            if row["gene"] not in gene_node_index.keys():
                G.add_node(node,size=20, title='gene', group=1, label=row["gene"])
                gene_node = node
                gene_node_index[row["gene"]] = gene_node
                G.add_edge(0,gene_node)
                node += 1
            else:
                gene_node = gene_node_index[row["gene"]]
            G.add_node(node,size=20, title='variant', group=2, label=row["gene"]+"-"+row["variant"])
            G.add_edge(gene_node,node)
            node += 1

        step = 80
        x = -600
        y = 0
        G.add_node(node, size=10, group=0, label="Disease", x=x, y=y,
                   physics=False, fixed=True)
        G.add_node(node+1, size=10, group=1, label="Gene", x=x, y=y+step,
                   physics=False, fixed=True)
        G.add_node(node+2, size=10, group=2, label="Variant", x=x,
                   y=y+2*step, physics=False, fixed=True)

        nt = Network(height = '500px', width= '100%')
        # populates the nodes and edges data structures
        nt.from_nx(G)

        path = 'html_files'
        nt.save_graph(f'{path}/dgv_network.html')
        HtmlFile = open(f'{path}/dgv_network.html', 'r', encoding='utf-8')
        components.html(HtmlFile.read(), height=500)

        st.header("Disease Gene Variant Bar")
        # TODO: insert bar
        st.header("Disease Gene Variant Heatmap")
        # TODO: insert selector and heatmap
    with variant_therapy_tab:
        st.header("Disease Variant Therapy Network")
        # TODO: insert network
    with time_series_tab:
        st.header("Number of Incidence of Disease over Time")
        # TODO: insert line
else:
    if len(disease) > 0:
        st.markdown(":red[The disease you are looking does not exist in the CIVic database. Please try again with a disease in the following table]")
    st.title("Disease")
    st.table(df_unique)
    # TODO: maybe show some overview charts about disease
