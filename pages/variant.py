import streamlit as st
import altair as alt
import pandas as pd

st.set_page_config(layout="centered")

columns = ["gene", "variant", "disease", "drugs", "year"]


@st.cache_data
def load_df():
    df_ = pd.read_csv("data/civic_data.tsv")
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
    return df_[df_["gene-variant"].notna()]


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
    return df_[df_["gene-variant"].notna()]


df = load_df()
df_unique = load_unique_civic_data()

variant = st.text_input("Search a variant here:")
if len(variant) == 0:
    url_params = st.experimental_get_query_params()
    if "variant" in url_params.keys():
        variant = url_params["variant"][0]

print(variant, variant in df_unique["gene-variant"].unique())

if len(variant) > 0 and variant in df_unique["gene-variant"].unique():
    variant_url = "/variant"
    st.markdown(f'''
            <a href={variant_url} target="_self">Back</a>
            ''', unsafe_allow_html=True)
    disease_tab, therapy_tab = st.tabs(["Disease", "Therapy"])
    df_variant = df[df["gene-variant"] == variant]

    with disease_tab:
        df_variant_disease = df_variant[df_variant["disease"].notna()]
        st.header("Number of Evidences Showing Connection between " + variant +
                  " and Diseases")
        donut_v_d = alt.Chart(df_variant_disease).mark_arc(innerRadius=50,
                                                           outerRadius=90).encode(
            theta=alt.Theta("num_ev:Q"),
            color=alt.Color("disease:N", title="Diseases"),
            tooltip=["num_ev:Q", "disease:N", "variant:N"]
        ).transform_aggregate(
            num_ev='count(evidence_id)',
            groupby=["disease", "variant"]
        )

        st.altair_chart(donut_v_d, use_container_width=True)

    with therapy_tab:
        df_variant_therapy = df_variant[df_variant["drugs"].notna()]
        st.header("Number of Evidences Showing Connection between " + variant +
                  " and Therapies")
        donut_v_t = alt.Chart(df_variant_therapy).mark_arc(innerRadius=50,
                                                           outerRadius=90).encode(
            theta=alt.Theta("num_ev:Q"),
            color=alt.Color("drugs:N", title="Therapies"),
            tooltip=["num_ev:Q", "variant:N", "drugs:N"]
        ).transform_aggregate(
            num_ev='count(evidence_id)',
            groupby=["variant", "drugs"]
        )

        st.altair_chart(donut_v_t, use_container_width=True)
else:
    if len(variant) > 0:
        st.markdown(
            ":red[The variant you are looking for does not exist in the CIVic " +
            "database. Please try again with a variant in the following chart]")

    st.title("Variant")
    df = df[df["gene-variant"].isin(df_unique["gene-variant"])]
    Year = st.slider("Year", min(df["year"]), max(df["year"]), value=2018)
    subset = df[df["year"] == Year]
    subset = subset[subset["gene-variant"].notna()]
    subset["url"] = "/variant?variant=" + subset["gene-variant"]

    plot1 = alt.Chart(subset).mark_bar(height=20).encode(
        x=alt.X(aggregate="count", type='quantitative',
                title="Number of Records"),
        y=alt.Y('gene-variant:N', title="Variants", sort="-x"),
        href="url",
        tooltip=["gene-variant",
                 alt.Tooltip(aggregate="count", title="Number of Records")]
    ).properties(
        title=f"Number of Records of All Variants Reported in {Year}",
        width=1000,
        height=alt.Step(30)
    )

    st.altair_chart(plot1, use_container_width=True)
