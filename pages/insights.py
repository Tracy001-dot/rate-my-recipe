import streamlit as st
import pandas as pd
import altair as alt
import os

st.title("Recipe Insights & Analytics")

# Load the processed recipe dataset
@st.cache_data
def load_data():
    data_path = os.path.join("data", "processed_recipes.csv")
    return pd.read_csv(data_path)

df = load_data()

# Summary Metrics
col1, col2, col3 = st.columns(3)

col1.metric("Total Recipes", len(df))

if "avg_rating" in df.columns:
    col2.metric(
        "Average Rating",
        f"{df['avg_rating'].mean():.2f}"
    )

if "review_count" in df.columns:
    col3.metric(
        "Total Reviews",
        f"{int(df['review_count'].sum()):,}"
    )

st.divider()

# Chart 1: Top 10 Recipes by Bayesian Rating
st.subheader("Top 10 Recipes by Bayesian Rating")

if all(column in df.columns for column in [
    "name", "bayesian_rating", "avg_rating", "review_count"
]):
    top_recipes = df.sort_values(
        by="bayesian_rating",
        ascending=False
    ).head(10)

    ordered_names = top_recipes["name"].tolist()

    chart = (
        alt.Chart(top_recipes)
        .mark_bar()
        .encode(
            x=alt.X(
                "name:N",
                sort=ordered_names,
                title="Recipe",
                axis=alt.Axis(labelAngle=-45)
            ),
            y=alt.Y(
                "bayesian_rating:Q",
                title="Bayesian Rating",
                scale=alt.Scale(domain=[0, 5])
            ),
            tooltip=[
                alt.Tooltip("name:N", title="Recipe"),
                alt.Tooltip(
                    "bayesian_rating:Q",
                    title="Bayesian Rating",
                    format=".3f"
                ),
                alt.Tooltip(
                    "avg_rating:Q",
                    title="Average Rating",
                    format=".3f"
                ),
                alt.Tooltip(
                    "review_count:Q",
                    title="Number of Reviews"
                )
            ]
        )
    )

    st.altair_chart(chart, use_container_width=True)

    # Show the exact top 10 results
    st.subheader("Top 10 Recipes – Detailed Results")

    st.dataframe(
        top_recipes[
            ["name", "avg_rating", "review_count", "bayesian_rating"]
        ].reset_index(drop=True),
        hide_index=True,
        use_container_width=True
    )

else:
    st.warning("Some required columns are missing from the dataset.")
