import streamlit as st
import networkx as nx
import nx_altair as nxa
from pyvis.network import Network
import streamlit.components.v1 as components
import pandas as pd


@st.cache_data
def load_unique_civic_data():
    columns = ["gene", "variant", "disease", "drugs"]
    df = pd.read_csv("data/civic_data_unique.tsv")[columns].drop_duplicates()
    df["gene-variant"] = df["gene"] + "-" + df["variant"]
    return df[df["disease"].notna()]


df_unique = load_unique_civic_data()
disease = st.text_input("Search a disease here:")

if len(disease) > 0 and disease in df_unique["disease"].unique():
    st.title(disease)
    disease_networks_tab, disease_variants_tab, time_series_tab = \
        st.tabs(["Disease Networks", "Disease Variants", "Time Series"])
    df_unique_disease = df_unique[df_unique["disease"] == disease]

    with disease_networks_tab:
        # TODO: change tooltip title
        st.header("Disease Gene Variant Network")
        # Generate a random graph
        G0 = nx.Graph()
        G0.add_node(0, size=20, title='disease', group=0, label=disease)
        node = 1
        gene_node_index = {}
        for index, row in df_unique_disease.iterrows():
            if row["gene"] not in gene_node_index.keys():
                G0.add_node(node, size=20, title='gene', group=1,
                            label=row["gene"])
                gene_node = node
                gene_node_index[row["gene"]] = gene_node
                G0.add_edge(0, gene_node)
                node += 1
            else:
                gene_node = gene_node_index[row["gene"]]
            G0.add_node(node, size=20, title='variant', group=2,
                        label=row["gene"] + "-" + row["variant"])
            G0.add_edge(gene_node, node)
            node += 1

        # Create legend nodes
        step = 80
        x = -600
        y = 0
        G0.add_node(node, size=10, group=0, label="Disease", x=x, y=y,
                    physics=False, fixed=True)
        G0.add_node(node + 1, size=10, group=1, label="Gene", x=x, y=y + step,
                    physics=False, fixed=True)
        G0.add_node(node + 2, size=10, group=2, label="Variant", x=x,
                    y=y + 2 * step, physics=False, fixed=True)

        nt = Network(height='500px', width='100%')
        # populates the nodes and edges data structures
        nt.from_nx(G0)

        path = 'html_files'
        nt.save_graph(f'{path}/dgv_network.html')
        HtmlFile = open(f'{path}/dgv_network.html', 'r', encoding='utf-8')
        components.html(HtmlFile.read(), height=500)

        st.header("Disease Variant Therapy Network")
        df_unique_disease_therapy = df_unique_disease[
            df_unique_disease["drugs"].notna()]
        G = nx.Graph()
        node = 0
        G.add_node(node, size=20, title='disease', group=0, label=disease)
        node += 1
        variant_nodes = {}
        therapy_nodes = {}
        for index, row in df_unique_disease_therapy.iterrows():
            gene_variant_name = row["gene"] + "-" + row["variant"]
            if gene_variant_name in variant_nodes.keys():
                variant_node = variant_nodes[gene_variant_name]
            else:
                variant_node = node
                variant_nodes[gene_variant_name] = variant_node
                G.add_node(variant_node, size=20, title='variant', group=1,
                           label=gene_variant_name)
                G.add_edge(0, variant_node)
                node += 1
            if row["drugs"] in therapy_nodes.keys():
                therapy_node = therapy_nodes[row["drugs"]]
            else:
                therapy_node = node
                therapy_nodes[row["drugs"]] = therapy_node
                G.add_node(therapy_node, size=20, title='drugs', group=2,
                           label=row["drugs"])
                node += 1
            G.add_edge(variant_node, therapy_node)

        df_unique_all_therapy = df_unique[df_unique["gene-variant"].isin(
            df_unique_disease["gene-variant"].values)]
        df_unique_other_therapy = df_unique_all_therapy[
            df_unique_all_therapy["disease"] != disease]
        df_unique_other_therapy = df_unique_other_therapy[
            ~df_unique_other_therapy["drugs"].isin(
                df_unique_disease["drugs"].values)]
        df_unique_other_therapy = df_unique_other_therapy[
            ["gene-variant", "drugs"]].drop_duplicates()
        for index, row in df_unique_other_therapy.iterrows():
            gene_variant_node = variant_nodes[row["gene-variant"]]
            if row["drugs"] in therapy_nodes.keys():
                therapy_node = therapy_nodes[row["drugs"]]
            else:
                therapy_node = node
                G.add_node(therapy_node, size=20, title='drugs', group=3,
                           label=row["drugs"])
                node += 1
            G.add_edge(gene_variant_node, therapy_node)

        # Create legend nodes
        step = 80
        x = -600
        y = -100
        G.add_node(node, size=10, group=0, label="Disease", x=x, y=y,
                   physics=False, fixed=True)
        G.add_node(node + 1, size=10, group=1, label="Gene-Variant", x=x,
                   y=y + step,
                   physics=False, fixed=True)
        G.add_node(node + 2, size=10, group=2, label="Known Variant", x=x,
                   y=y + 2 * step, physics=False, fixed=True)
        G.add_node(node + 3, size=10, group=3, label="Unknown Therapy", x=x,
                   y=y + 3 * step, physics=False, fixed=True)
        nt1 = Network(height='500px', width='100%')
        # populates the nodes and edges data structures
        nt1.from_nx(G)
        path = 'html_files'
        nt1.save_graph(f'{path}/dvt_network.html')
        HtmlFile = open(f'{path}/dvt_network.html', 'r', encoding='utf-8')
        components.html(HtmlFile.read(), height=500)

    with disease_variants_tab:
        st.header("Disease Gene Variant Bar")
        # TODO: insert bar
        st.header("Disease Gene Variant Heatmap")
        # TODO: insert selector and heatmap

    with time_series_tab:
        st.header("Number of Incidence of Disease over Time")
        # TODO: insert line
else:
    if len(disease) > 0:
        st.markdown(
            ":red[The disease you are looking does not exist in the CIVic " +
            "database. Please try again with a disease in the following table]")
    st.title("Disease")
    st.table(df_unique)
    # TODO: maybe show some overview charts about disease
