import streamlit as st
st.set_page_config(
    page_title="Randomness Lab",
    page_icon="🎲"
)

st.title("🎲 Randomness Lab")

st.write(
    """
    Welcome to Randomness Lab!

    This website demonstrates how randomness affects artificial intelligence
    and deep-learning systems.

    Use the page menu on the left to select an experiment.
    """
)

st.subheader("Experiments")

st.write(
    """
    **Experiment 1:** Temperature and text generation

    **Experiment 2:** Random seeds and reproducibility

    **Experiment 3:** Random weight initialization in neural networks
    """
)