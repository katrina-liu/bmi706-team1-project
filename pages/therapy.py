import streamlit as st
import altair as alt
import pandas as pd

df = pd.read_csv("data/civic_data.tsv")
df_unique = pd.read_csv("data/civic_data_unique.tsv")
df_unique.dropna(subset=['drugs','variant','disease'])

therapy = st.text_input("Search a therapy here:")

if len(therapy) > 0 and therapy in df_unique["drugs"].unique(): # TODO: Change this to if therapy is valid
    variant_tab, disease_tab = st.tabs(["Variant", "Disease"])
    with variant_tab:
        st.header("Number of Evidences Showing Connection between "+ therapy+
                 " and Variants")
        donut_t_v = alt.Chart(df_unique).mark_arc(innerRadius=50, outerRadius=90).encode(
            theta = alt.Theta("num_ev:Q"),
            color = alt.Color("variant:N", title = "Variants"),
            tooltip=["num_ev:Q", "variant:N","therapy:N"]
            ).transform_aggregate(
                num_ev='count(evidence_id)',
                groupby=["variant","therapy"]
                ).properties(
                    width=250
                    )
        st.altair_chart(donut_t_v)

    with disease_tab:
        st.header("Number of Evidences Showing Connection between "+ therapy+
                 " and Diseases")
        donut_t_d = alt.Chart(df_unique).mark_arc(innerRadius=50, outerRadius=90).encode(
            theta = alt.Theta("num_ev:Q"),
            color = alt.Color("disease:N", title = "Diseases"),
            tooltip=["num_ev:Q", "disease:N","therapy:N"]
            ).transform_aggregate(
                num_ev='count(evidence_id)',
                groupby=["disease","therapy"]
                ).properties(
                    width=250
                    )
        st.altair_chart(donut_t_d)
else:
    st.title("Therapy")
    # TODO: maybe show some overview charts about therapy
