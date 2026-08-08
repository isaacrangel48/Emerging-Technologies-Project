import streamlit as st
st.set_page_config(
    page_title="How Randomness Affects AI",
    page_icon="🎲"
)

st.title("🎲 How Randomness Affects AI")

st.write(
    """
    Welcome to our Project!

    This website demonstrates how randomness affects artificial intelligence
    and deep-learning systems.

    Use the page menu on the left to select an experiment.
    """
)

st.subheader("Experiments")

st.write(
    """
    **Experiment 1:** Random Number Generator

    **Experiment 2:** Temperature and text generation

    **Experiment 3:** Random seeds and reproducibility

    **Experiment 4:** Random weight initialization in neural networks
    """
)