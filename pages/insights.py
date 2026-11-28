import streamlit as st
import pandas as pd
import altair as alt

st.title("Recipe Insights & Analytics")

@st.cache_data
def load_data():
    return pd.read_csv("processed_recipes.csv")

df = load_data()

# Summary Metrics
col1, col2, col3 = st.columns(3)

col1.metric("Total Recipes", len(df))
if "average_rating" in df.columns:
    col2.metric("Average Rating", f"{df['average_rating'].mean():.2f}")
if "review_count" in df.columns:
    col3.metric("Total Reviews", f"{int(df['review_count'].sum()):,}")

st.divider()

# Chart 1: Top Rated Recipes
st.subheader("Top 10 Recipes by Bayesian rating")
if "bayesian_rating" in df.columns and "name" in df.columns:
    top_recipes = df.sort_values(by="bayesian_rating", ascending=False).head(10)
    chart = (
        alt.Chart(top_recipes)
        .mark_bar()
        .encode(
            x=alt.X("name:N", sort="-y", title="Recipe"),
            y=alt.Y("bayesian_rating:Q", title="Bayesian Rating"),
            tooltip=["name", "bayesian_rating", "review_count"],
        )
    )
    st.altair_chart(chart, use_container_width=True)
else:
    st.info("Bayesian rating data available in search view.")
    
