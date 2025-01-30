import streamlit as st
from tabs.ingress_tab import render_ingress_tab
from tabs.analysis_tab import render_analysis_tab
from src.config import Config

def main():
    # Load configuration
    config = Config()

    # Set up Streamlit interface
    st.title("ICMC/USP Infrastructure AI Agent")

    # Create tabs
    tab_ingress, tab_analysis = st.tabs(["Ingress Details", "AI Metrics Analysis"])

    # Render tabs
    with tab_ingress:
        render_ingress_tab(config)

    with tab_analysis:
        render_analysis_tab(config)

if __name__ == "__main__":
    main() 