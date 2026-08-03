import time

import pandas as pd
import streamlit as st
from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler


st.set_page_config(
    page_title="Weight Initialization",
    page_icon="🧠"
)

st.title("🧠 Experiment 3: Random Weight Initialization")

st.write(
    """
    A neural network does not begin knowing the correct answer.

    It begins with random starting weights. These weights are small numbers
    that control how strongly the neurons are connected.

    This experiment trains the same neural network several times using
    different random seeds. Everything else stays the same.
    """
)

st.info(
    """
    Think of each seed as giving the neural network a different starting point.

    Some starting points may help it learn faster or reach better results.
    """
)

number_of_runs = st.slider(
    "Number of different seeds",
    min_value=3,
    max_value=10,
    value=5
)

hidden_neurons = st.slider(
    "Number of hidden neurons",
    min_value=2,
    max_value=30,
    value=10
)

maximum_iterations = st.slider(
    "Maximum training iterations",
    min_value=100,
    max_value=1000,
    value=500,
    step=100
)

if st.button("Run Weight Initialization Experiment"):

    # Create the same dataset every time.
    X, y = make_moons(
        n_samples=500,
        noise=0.25,
        random_state=100
    )

    # Split the dataset into training and testing portions.
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.30,
        random_state=100,
        stratify=y
    )

    # Scale the input values so the neural network trains more reliably.
    scaler = StandardScaler()

    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    results = []
    loss_history = {}

    progress_bar = st.progress(0)

    for run_number in range(number_of_runs):

        seed = run_number + 1

        model = MLPClassifier(
            hidden_layer_sizes=(hidden_neurons,),
            activation="relu",
            solver="adam",
            max_iter=maximum_iterations,
            random_state=seed
        )

        start_time = time.perf_counter()

        model.fit(
            X_train_scaled,
            y_train
        )

        elapsed_time = time.perf_counter() - start_time

        training_accuracy = model.score(
            X_train_scaled,
            y_train
        )

        testing_accuracy = model.score(
            X_test_scaled,
            y_test
        )

        final_loss = model.loss_

        results.append(
            {
                "Seed": seed,
                "Training Accuracy": training_accuracy,
                "Testing Accuracy": testing_accuracy,
                "Final Loss": final_loss,
                "Iterations": model.n_iter_,
                "Training Time": elapsed_time
            }
        )

        loss_history[f"Seed {seed}"] = pd.Series(
            model.loss_curve_
        )

        progress_bar.progress(
            (run_number + 1) / number_of_runs
        )

    results_dataframe = pd.DataFrame(results)

    st.success("Experiment completed!")

    st.header("Results")

    display_dataframe = results_dataframe.copy()

    display_dataframe["Training Accuracy"] = (
        display_dataframe["Training Accuracy"] * 100
    ).round(2)

    display_dataframe["Testing Accuracy"] = (
        display_dataframe["Testing Accuracy"] * 100
    ).round(2)

    display_dataframe["Final Loss"] = (
        display_dataframe["Final Loss"].round(4)
    )

    display_dataframe["Training Time"] = (
        display_dataframe["Training Time"].round(3)
    )

    st.dataframe(
        display_dataframe,
        use_container_width=True,
        hide_index=True
    )

    best_row = results_dataframe.loc[
        results_dataframe["Testing Accuracy"].idxmax()
    ]

    worst_row = results_dataframe.loc[
        results_dataframe["Testing Accuracy"].idxmin()
    ]

    average_accuracy = (
        results_dataframe["Testing Accuracy"].mean()
    )

    accuracy_standard_deviation = (
        results_dataframe["Testing Accuracy"].std()
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Best Seed",
        int(best_row["Seed"])
    )

    col2.metric(
        "Best Test Accuracy",
        f"{best_row['Testing Accuracy'] * 100:.2f}%"
    )

    col3.metric(
        "Average Accuracy",
        f"{average_accuracy * 100:.2f}%"
    )

    col4.metric(
        "Accuracy Variation",
        f"{accuracy_standard_deviation * 100:.2f}%"
    )

    st.header("Accuracy by Seed")

    accuracy_chart = results_dataframe[
        [
            "Seed",
            "Training Accuracy",
            "Testing Accuracy"
        ]
    ].set_index("Seed")

    st.bar_chart(accuracy_chart)

    st.header("Training Loss Curves")

    loss_dataframe = pd.DataFrame(loss_history)

    loss_dataframe.index.name = "Training Iteration"

    st.line_chart(loss_dataframe)

    st.header("What Does This Show?")

    difference = (
        best_row["Testing Accuracy"]
        - worst_row["Testing Accuracy"]
    )

    st.write(
        f"""
        The best seed was **{int(best_row['Seed'])}**, with a testing
        accuracy of **{best_row['Testing Accuracy'] * 100:.2f}%**.

        The lowest testing accuracy was
        **{worst_row['Testing Accuracy'] * 100:.2f}%**.

        The difference between the best and worst results was
        **{difference * 100:.2f} percentage points**.
        """
    )

    if difference < 0.01:
        st.write(
            """
            In this run, the different starting weights produced similar
            final results. However, the loss curves and number of training
            iterations may still be different.
            """
        )

    else:
        st.write(
            """
            In this run, the random starting weights noticeably affected
            the neural network's final performance.
            """
        )