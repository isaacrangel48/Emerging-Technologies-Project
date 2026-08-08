import random

import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="Random Number Generator",
    page_icon="🎲"
)

st.title("🎲 Experiment 1: Random Number Generator")

st.write(
    """
    This experiment demonstrates how a computer generates random numbers.

    A random seed controls the starting point of the random-number generator.
    Using the same seed and settings should produce the same sequence of numbers.
    """
)

minimum_value = st.number_input(
    "Minimum number",
    value=1,
    step=1
)

maximum_value = st.number_input(
    "Maximum number",
    value=100,
    step=1
)

number_of_values = st.slider(
    "How many numbers should be generated?",
    min_value=1,
    max_value=1000,
    value=100
)

seed = st.number_input(
    "Random seed",
    min_value=0,
    max_value=100000,
    value=42,
    step=1
)

use_fixed_seed = st.checkbox(
    "Use the selected seed",
    value=True
)

if st.button("Generate Random Numbers"):

    if minimum_value >= maximum_value:
        st.error(
            "The minimum number must be smaller than the maximum number."
        )

    else:
        if use_fixed_seed:
            random.seed(seed)
        else:
            random.seed()

        random_numbers = [
            random.randint(
                int(minimum_value),
                int(maximum_value)
            )
            for _ in range(number_of_values)
        ]

        results = pd.DataFrame(
            {
                "Random Number": random_numbers
            }
        )

        st.success("Random numbers generated!")

        st.subheader("Generated Numbers")

        st.dataframe(
            results,
            use_container_width=True,
            hide_index=True
        )

        average_value = results["Random Number"].mean()
        minimum_generated = results["Random Number"].min()
        maximum_generated = results["Random Number"].max()
        unique_values = results["Random Number"].nunique()

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Average",
            f"{average_value:.2f}"
        )

        col2.metric(
            "Smallest",
            int(minimum_generated)
        )

        col3.metric(
            "Largest",
            int(maximum_generated)
        )

        col4.metric(
            "Unique Values",
            unique_values
        )

        st.subheader("Distribution of Random Numbers")

        frequency_table = (
            results["Random Number"]
            .value_counts()
            .sort_index()
        )

        st.bar_chart(frequency_table)

        st.subheader("Reproducibility Test")

        if use_fixed_seed:
            random.seed(seed)

            second_sequence = [
                random.randint(
                    int(minimum_value),
                    int(maximum_value)
                )
                for _ in range(number_of_values)
            ]

            sequences_match = (
                random_numbers == second_sequence
            )

            if sequences_match:
                st.success(
                    "The same seed produced the same sequence."
                )
            else:
                st.warning(
                    "The sequences did not match."
                )

        else:
            st.info(
                """
                No fixed seed was used, so a new sequence should normally
                appear each time the button is pressed.
                """
            )