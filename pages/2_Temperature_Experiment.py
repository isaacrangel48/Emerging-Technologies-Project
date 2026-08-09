import streamlit as st
import ollama

st.set_page_config(
    page_title="Temperature Experiment",
    page_icon="🌡️"
)

st.title("🌡️ Experiment 2: Temperature and Text Generation")

st.write(
    """
    This experiment shows how temperature changes the randomness
    of an AI model's response.

    Lower temperatures usually produce more predictable responses.
    Higher temperatures usually produce more varied responses.
    """
)

prompt = st.text_area(
    "Enter a prompt:",
    "Write a 5-10 sentence summary of the book Moneyball starring Brad Pitt."
)

temperature = st.slider(
    "Choose a temperature",
    min_value=0.0,
    max_value=1.5,
    value=0.7,
    step=0.1
)

seed = st.number_input(
    "Random seed",
    min_value=0,
    max_value=100000,
    value=42,
    step=1
)

if "temperature_results" not in st.session_state:
    st.session_state.temperature_results = []

if st.button("Generate Response"):

    if not prompt.strip():
        st.warning("Please enter a prompt.")

    else:

        with st.spinner(
            f"Generating response at temperature {temperature}..."
        ):

            try:
                response = ollama.chat(
    model="qwen3.5:latest",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ],
    think=False,
    options={
        "temperature": temperature,
        "seed": int(seed),
        "num_predict": 300
    }
)

                text = response["message"]["content"]

                words = text.split()

                total_words = len(words)

                unique_words = len(
                    set(word.lower() for word in words)
                )

                if total_words > 0:
                    unique_ratio = (
                        unique_words / total_words
                    ) * 100
                else:
                    unique_ratio = 0

                st.session_state.temperature_results.append(
                    {
                        "temperature": temperature,
                        "seed": int(seed),
                        "response": text,
                        "words": total_words,
                        "unique_words": unique_words,
                        "unique_ratio": unique_ratio
                    }
                )

                st.subheader(
                    f"Response — Temperature {temperature}"
                )

                st.write(text)

                col1, col2, col3 = st.columns(3)

                col1.metric(
                    "Total Words",
                    total_words
                )

                col2.metric(
                    "Unique Words",
                    unique_words
                )

                col3.metric(
                    "Unique-Word Ratio",
                    f"{unique_ratio:.1f}%"
                )

            except Exception as error:

                st.error(
                    "The model could not generate a response."
                )

                st.code(str(error))


st.divider()

st.header("Saved Comparisons")

if len(st.session_state.temperature_results) == 0:

    st.info(
        "Generate responses at different temperatures to compare them."
    )

else:

    for result in st.session_state.temperature_results:

        with st.expander(
            f"Temperature {result['temperature']} "
            f"| Seed {result['seed']}"
        ):

            st.write(result["response"])

            st.write(
                f"Total words: {result['words']}"
            )

            st.write(
                f"Unique words: {result['unique_words']}"
            )

            st.write(
                f"Unique-word ratio: "
                f"{result['unique_ratio']:.1f}%"
            )


if st.button("Clear Saved Results"):

    st.session_state.temperature_results = []

    st.rerun()