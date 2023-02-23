import streamlit as st

therapy = st.text_input("Search a therapy here:")

if len(therapy) > 0: # TODO: Change this to if therapy is valid
    variant_tab, disease_tab = st.tabs(["Variant", "Disease"])
    with variant_tab:
        st.header("Number of Evidences Showing Connection between "+ therapy+
                 " and Variants")
        # TODO: add donut
    with disease_tab:
        st.header("Number of Evidences Showing Connection between "+ therapy+
                 " and Diseases")
        # TODO: add donut
else:
    st.title("Therapy")
    # TODO: maybe show some overview charts about therapy
