import streamlit as st
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components
import pandas as pd
import altair as alt

st.set_page_config(layout="centered")

columns = ["gene", "variant", "disease", "drugs"]


@st.cache_data
def load_df():
    df_ = pd.read_csv("data/civic_data.tsv")
    df_ = df_[df_["evidence_direction"] == "Supports"]
    df_[columns] = df_[columns].astype(str)
    df_["gene-variant"] = df_["gene"] + "-" + df_["variant"]
    df_ = df_.dropna(subset=columns)
    return df_

@st.cache_data
def load_unique_civic_data():
    df_ = pd.read_csv("data/civic_data_unique.tsv").drop_duplicates(
        subset=columns)
    df_ = df_[df_["evidence_direction"] == "Supports"]
    df_ = df_[df_["clinical_significance"].isin(["Positive", "Sensitivity",
                                                 "Better Outcome"])]
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
    return df_[df_["disease"].notna()]


df = load_df()
df_unique = load_unique_civic_data()

disease = st.text_input("Search a disease here:")

if len(disease) == 0:
    url_params = st.experimental_get_query_params()
    if "disease" in url_params.keys():
        disease = url_params["disease"][0]

if len(disease) > 0 and disease in df_unique["disease"].unique():
    st.experimental_set_query_params(disease=disease)
    disease_url = "/disease"
    st.markdown(f'''
    <a href={disease_url} target="_self">Back</a>
    ''', unsafe_allow_html=True)
    st.title(disease)
    disease_networks_tab, disease_variants_tab = \
        st.tabs(["Disease Networks", "Disease Variants"])
    df_unique_disease = df_unique[df_unique["disease"] == disease]
    df_disease = df[df["disease"] == disease]

    with disease_networks_tab:
        st.header("Disease Gene Variant Network")
        df_unique_disease_variant = df_unique_disease.drop_duplicates(
            subset=["gene-variant"])
        G0 = nx.Graph()
        G0.add_node(0, size=20, title=disease, group=0, label=disease)
        node = 1
        gene_node_index = {}
        for index, row in df_unique_disease_variant.iterrows():
            if row["gene"] not in gene_node_index.keys():
                G0.add_node(node, size=20, title=row["gene"], group=1,
                            label=row["gene"])
                gene_node = node
                gene_node_index[row["gene"]] = gene_node
                G0.add_edge(0, gene_node)
                node += 1
            else:
                gene_node = gene_node_index[row["gene"]]
            G0.add_node(node, size=20, title=row['variant'], group=2,
                        label=row["gene"] + "-" + row["variant"])
            G0.add_edge(gene_node, node)
            node += 1

        # Create legend nodes
        step = 80
        x = -1200
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
        G.add_node(node, size=20, title=disease, group=0, label=disease)
        node += 1
        variant_nodes = {}
        therapy_nodes = {}

        for index, row in df_unique_disease_therapy.iterrows():
            gene_variant_name = row["gene-variant"]
            if gene_variant_name in variant_nodes.keys():
                variant_node = variant_nodes[gene_variant_name]
            else:
                variant_node = node
                variant_nodes[gene_variant_name] = variant_node
                G.add_node(variant_node, size=20, title=gene_variant_name,
                           group=1,
                           label=gene_variant_name)
                G.add_edge(0, variant_node)
                node += 1
            if row["drugs"] in therapy_nodes.keys():
                therapy_node = therapy_nodes[row["drugs"]]
            else:
                therapy_node = node
                therapy_nodes[row["drugs"]] = therapy_node
                G.add_node(therapy_node, size=20, title=row["drugs"], group=2,
                           label=row["drugs"])
                node += 1
            G.add_edge(variant_node, therapy_node)

        df_unique_all_therapy = df_unique[df_unique["gene-variant"].isin(
            df_unique_disease_therapy["gene-variant"].values)]
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
        x = -1000
        y = -100
        G.add_node(node, size=10, group=0, label="Disease", x=x, y=y,
                   physics=False, fixed=True)
        G.add_node(node + 1, size=10, group=1, label="Gene-Variant", x=x,
                   y=y + step,
                   physics=False, fixed=True)
        G.add_node(node + 2, size=10, group=2, label="Known Therapy", x=x,
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

        # heatmap multi-selector
        default = df_unique_disease['disease'].unique()
        dieases_selector = st.multiselect('Diseases',
                                          df_unique["disease"].unique(),
                                          default)
        subset = df_unique[df_unique["disease"].isin(dieases_selector)]
        subset2 = df[df["disease"].isin(dieases_selector)]

        # add interaction
        selector = alt.selection_single(
            fields=["disease"],
            # init={"disease": default[0]}
        )

        # Disease Gene Variant Heatmap
        heatmap = alt.Chart(subset).mark_rect().encode(
            x=alt.X("gene:N", title="Genes"),
            y=alt.Y("disease:N", title="Diseases"),
            color=alt.Color('count():Q'),
            tooltip=["disease", "gene",
                     alt.Tooltip('count():Q', title='Number of Variants')]
        ).properties(
            width=500,
            title="Disease Gene Variant Heatmap"
        ).add_selection(
            selector
        )

        # Disease Gene Variant Bar
        bar_g_v = alt.Chart(subset).mark_bar().encode(
            x=alt.X('gene:N', title="Gene Names"),
            y=alt.Y('count():Q', title="Number of Variants",
                    axis=alt.Axis(tickMinStep=1)),
            color="disease:N",
            tooltip=["gene",
                     alt.Tooltip('count():Q', title='Number of Variants')]
        ).properties(
            width=500,
            title="Disease Gene Variant Bar"
        ).transform_filter(
            selector
        )
        # with time_series_tab:
        time_series = alt.Chart(subset2).mark_line().encode(
            x=alt.X("year:N"),
            y=alt.Y("count(disease):Q", title="Number of Disease Records",
                    axis=alt.Axis(tickMinStep=1)),
            color='disease:N',
            tooltip=["year:N",
                     alt.Tooltip("count(disease):Q", title="Number of Records")]
        ).properties(
            width=500,
            title="Number of Records over Time"
        ).transform_filter(
            selector
        )

        st.altair_chart(heatmap & bar_g_v & time_series,
                        use_container_width=True)

else:
    st.experimental_set_query_params(disease=disease)
    if len(disease) > 0:
        st.markdown(
            ":red[The disease you are looking for does not exist in the CIVic" +
            " database. Please try again with a disease in the following table]"
        )
    st.title("Disease")
    df = df[df["disease"].isin(df_unique["disease"])]
    Year = st.slider("Year", min(df["year"]), max(df["year"]), value=2018)
    subset = df[df["year"] == Year]
    subset = subset[subset["disease"].notna()]
    subset["url"] = "/disease?disease=" + subset["disease"]

    plot1 = alt.Chart(subset).mark_bar(height=20).encode(
        x=alt.X(aggregate="count", type='quantitative',
                title="Number of Records"),
        y=alt.Y('disease:N', title="Diseases", sort="-x"),
        href="url",
        tooltip=["disease",
                 alt.Tooltip(aggregate="count", title="Number of Records")]
    ).properties(
        title=f"Number of Records of All Diseases Reported in {Year}",
        width=650,
        height=alt.Step(30)
    )

    st.altair_chart(plot1, use_container_width=True)
