import streamlit as st
import ollama

st.set_page_config(
    page_title="Random Seed Experiment",
    page_icon="🌱"
)

st.title("🌱 Experiment 2: Random Seeds")

st.write(
    """
    This experiment tests whether using the same random seed produces
    similar or identical AI responses.

    First, the model runs three times using the same seed.
    Then, it runs three times using different seeds.
    """
)

prompt = st.text_area(
    "Enter a prompt:",
    "Write a short paragraph about a robot learning how to cook."
)

temperature = st.slider(
    "Temperature",
    min_value=0.0,
    max_value=2.0,
    value=0.7,
    step=0.1
)

fixed_seed = st.number_input(
    "Fixed seed",
    min_value=0,
    max_value=100000,
    value=42,
    step=1
)

number_of_runs = st.slider(
    "Number of runs",
    min_value=2,
    max_value=5,
    value=3
)


def generate_response(user_prompt, selected_temperature, selected_seed):
    """Send a prompt and randomness settings to Ollama."""

    response = ollama.chat(
        model="qwen3.5:latest",
        messages=[
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        options={
            "temperature": selected_temperature,
            "seed": selected_seed
        }
    )

    return response["message"]["content"]


def calculate_word_similarity(first_text, second_text):
    """
    Calculate a simple similarity score based on shared unique words.
    The score ranges from 0% to 100%.
    """

    first_words = set(first_text.lower().split())
    second_words = set(second_text.lower().split())

    all_words = first_words.union(second_words)

    if len(all_words) == 0:
        return 0.0

    shared_words = first_words.intersection(second_words)

    return len(shared_words) / len(all_words) * 100


if st.button("Run Seed Experiment"):

    if not prompt.strip():
        st.warning("Please enter a prompt.")

    else:
        st.header("Part 1: Same Seed")

        st.write(
            f"All runs below use seed **{fixed_seed}** and "
            f"temperature **{temperature}**."
        )

        same_seed_responses = []

        for run_number in range(1, number_of_runs + 1):

            with st.spinner(
                f"Generating same-seed response {run_number}..."
            ):
                generated_text = generate_response(
                    prompt,
                    temperature,
                    fixed_seed
                )

            same_seed_responses.append(generated_text)

            with st.expander(
                f"Same Seed — Run {run_number}",
                expanded=True
            ):
                st.write(generated_text)

        st.subheader("Same-Seed Comparison")

        first_same_seed_response = same_seed_responses[0]

        for index, response in enumerate(
            same_seed_responses[1:],
            start=2
        ):
            exact_match = response == first_same_seed_response

            similarity = calculate_word_similarity(
                first_same_seed_response,
                response
            )

            st.write(
                f"Run 1 compared with Run {index}:"
            )

            st.write(
                f"- Exact match: **{'Yes' if exact_match else 'No'}**"
            )

            st.write(
                f"- Shared-word similarity: **{similarity:.1f}%**"
            )

        st.divider()

        st.header("Part 2: Different Seeds")

        different_seed_responses = []

        for run_number in range(1, number_of_runs + 1):

            current_seed = fixed_seed + run_number

            with st.spinner(
                f"Generating response with seed {current_seed}..."
            ):
                generated_text = generate_response(
                    prompt,
                    temperature,
                    current_seed
                )

            different_seed_responses.append(
                {
                    "seed": current_seed,
                    "text": generated_text
                }
            )

            with st.expander(
                f"Different Seed — Seed {current_seed}",
                expanded=True
            ):
                st.write(generated_text)

        st.subheader("Different-Seed Comparison")

        first_different_response = different_seed_responses[0]["text"]
        first_different_seed = different_seed_responses[0]["seed"]

        for result in different_seed_responses[1:]:

            exact_match = (
                result["text"] == first_different_response
            )

            similarity = calculate_word_similarity(
                first_different_response,
                result["text"]
            )

            st.write(
                f"Seed {first_different_seed} compared with "
                f"seed {result['seed']}:"
            )

            st.write(
                f"- Exact match: **{'Yes' if exact_match else 'No'}**"
            )

            st.write(
                f"- Shared-word similarity: **{similarity:.1f}%**"
            )

        st.success("Seed experiment completed!")