import streamlit as st
import ollama

st.set_page_config(
    page_title="Temperature Experiment",
    page_icon="🌡️"
)

st.title("🌡️ Experiment 1: Temperature and Text Generation")

st.write(
    "This experiment sends the same prompt to the same AI model "
    "using different temperature settings."
)

prompt = st.text_area(
    "Enter a prompt:",
    "Write a 5-10 sentence summary of the book Moneyball starring Brad Pitt."
)

temperatures = [0.0, 0.5, 1.0, 1.5]

if st.button("Run Experiment"):

    for temp in temperatures:

        st.subheader(f"Temperature: {temp}")

        with st.spinner(f"Generating at temperature {temp}..."):

            response = ollama.chat(
                model="qwen3.5:latest",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                options={
                    "temperature": temp
                }
            )

        text = response["message"]["content"]

        st.write(text)

        # Simple measurements
        words = text.split()
        total_words = len(words)
        unique_words = len(set(word.lower() for word in words))

        st.write(f"Total words: {total_words}")
        st.write(f"Unique words: {unique_words}")

        st.divider()