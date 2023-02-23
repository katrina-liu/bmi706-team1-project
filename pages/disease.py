import streamlit as st

disease = st.text_input("Search a disease here:")

if len(disease) > 0:  # TODO: Change this to if disease is valid
    st.title(disease)
    gene_variant_tab, variant_therapy_tab, time_series_tab = \
        st.tabs(["Gene-Variant", "Variant-Therapy", "Time Series"])
    with gene_variant_tab:
        st.header("Disease Gene Variant Network")
        # TODO: insert network
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
    st.title("Disease")
    # TODO: maybe show some overview charts about disease
