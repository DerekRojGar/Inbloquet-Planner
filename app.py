import streamlit as st
from controllers.ui_controller import run_app

st.set_page_config(
    page_title="Planificador INBLOQUET",
    page_icon="📅",
    layout="wide"
)

if __name__ == "__main__":
    run_app()
