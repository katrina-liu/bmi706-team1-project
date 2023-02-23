import streamlit as st

variant = st.text_input("Search a variant here:")

if len(variant) > 0:  # TODO: Change this to if variant is valid
    disease_tab, therapy_tab = st.tabs(["Disease", "Therapy"])
    with disease_tab:
        st.header("Number of Evidences Showing Connection between " + variant +
                  " and Diseases")
        # TODO: add donut
    with therapy_tab:
        st.header("Number of Evidences Showing Connection between " + variant +
                  " and Therapies")
        # TODO: add donut
else:
    st.title("Variant")
    # TODO: maybe show some overview charts about Variants
