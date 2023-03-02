import streamlit as st
import altair as alt
import pandas as pd

df = pd.read_csv("data/civic_data.tsv")
df_unique = pd.read_csv("data/civic_data_unique.tsv")
df_unique.dropna(subset=['drugs','variant','disease'])

variant = st.text_input("Search a variant here:")

if len(variant) > 0 and variant in df_unique["variant"].unique():  # TODO: Change this to if variant is valid
    disease_tab, therapy_tab = st.tabs(["Disease", "Therapy"])
    df_unique_variant = df_unique[df_unique["variant"] == variant]
    
    with disease_tab:
        st.header("Number of Evidences Showing Connection between " + variant +
                  " and Diseases")
        donut_v_d = alt.Chart(df_unique_variant).mark_arc(innerRadius=50, outerRadius=90).encode(
            theta = alt.Theta("num_ev:Q"),
            color = alt.Color("disease:N", title = "Diseases"),
            tooltip=["num_ev:Q", "disease:N","variant:N"]
            ).transform_aggregate(
                num_ev='count(evidence_id)',
                groupby=["disease","variant"]
                )
            
        st.altair_chart(donut_v_d)
        
    with therapy_tab:
        st.header("Number of Evidences Showing Connection between " + variant +
                  " and Therapies")
        donut_v_t = alt.Chart(df_unique_variant).mark_arc(innerRadius=50, outerRadius=90).encode(
            theta = alt.Theta("num_ev:Q"),
            color = alt.Color("drugs:N", title = "Therapies"),
            tooltip=["num_ev:Q", "variant:N","drugs:N"]
            ).transform_aggregate(
                num_ev='count(evidence_id)',
                groupby=["variant","drugs"]
                )
            
        st.altair_chart(donut_v_t)
else:
    st.title("Variant")
    # TODO: maybe show some overview charts about Variants
