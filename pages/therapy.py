import streamlit as st
import altair as alt
import pandas as pd

st.set_page_config(layout="centered")
columns = ["gene", "variant", "disease", "drugs"]

@st.cache_data
def load_df():
    df_ = pd.read_csv("data/civic_data.tsv")
    df_ = df_[df_["evidence_direction"] == "Supports"]
    df_ = df_.dropna(subset=columns)
    df_[columns] = df_[columns].astype(str)
    df_["gene-variant"] = df_["gene"] + "-" + df_["variant"]
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
    return df_[df_["drugs"].notna()]


df = load_df()
df_unique = load_unique_civic_data()

therapy = st.text_input("Search a therapy here:")

if len(therapy) == 0:
    url_params = st.experimental_get_query_params()
    if "therapy" in url_params.keys():
        therapy = url_params["therapy"][0]

if len(therapy) > 0 and therapy in df_unique["drugs"].unique():
    therapy_url = "/therapy"
    st.markdown(f'''
        <a href={therapy_url} target="_self">Back</a>
        ''', unsafe_allow_html=True)
    variant_tab, disease_tab = st.tabs(["Variant", "Disease"])
    df_therapy = df[df["drugs"] == therapy]

    with variant_tab:
        st.header("Number of Evidences Showing Connection between " + therapy +
                  " and Variants")
        df_therapy_variant = df_therapy[df_therapy["gene-variant"].notna()]
        donut_t_v = alt.Chart(df_therapy_variant).mark_arc(
            innerRadius=50,
            outerRadius=90).encode(
            theta=alt.Theta("num_ev:Q"),
            color=alt.Color("gene-variant:N", title="Variants"),
            tooltip=["num_ev:Q", "gene-variant:N", "drugs:N"]
        ).transform_aggregate(
            num_ev='count(evidence_id)',
            groupby=["gene-variant", "drugs"]
        )

        st.altair_chart(donut_t_v, use_container_width=True)

    with disease_tab:
        st.header("Number of Evidences Showing Connection between " + therapy +
                  " and Diseases")
        df_therapy_disease = df_therapy[df_therapy["disease"].notna()]
        donut_t_d = alt.Chart(df_therapy_disease).mark_arc(
            innerRadius=50,
            outerRadius=90).encode(
            theta=alt.Theta("num_ev:Q"),
            color=alt.Color("disease:N", title="Diseases"),
            tooltip=["num_ev:Q", "disease:N", "drugs:N"]
        ).transform_aggregate(
            num_ev='count(evidence_id)',
            groupby=["disease", "drugs"]
        )

        st.altair_chart(donut_t_d, use_container_width=True)
else:
    if len(therapy) > 0:
        st.markdown(
            ":red[The therapy you are looking for does not exist in the CIVic" +
            " database. Please try again with a therapy in the following chart]"
        )
    st.title("Therapy")
    df = df[df["drugs"].isin(df_unique["drugs"])]
    Year = st.slider("Year", min(df["year"]), max(df["year"]), value=2018)
    subset = df[df["year"] == Year]
    subset["url"] = "/therapy?therapy=" + subset["drugs"]

    plot1 = alt.Chart(subset).mark_bar(height=20).encode(
        x=alt.X(aggregate="count", type='quantitative',
                title="Number of Records"),
        y=alt.Y('drugs:N', title="Drugs", sort="-x"),
        href="url",
        tooltip=["drugs",
                 alt.Tooltip(aggregate="count", title="Number of Records")]
    ).properties(
        title=f"Number of Records of All Therapies Reported in {Year}",
        width=650,
        height=alt.Step(30)
    )

    st.altair_chart(plot1, use_container_width=True)
