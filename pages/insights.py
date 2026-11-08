import streamlit as st
import pandas as pd

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
st.subheader("Top 10 Recipes by Bayesian Score")
if "bayesian_score" in df.columns and "name" in df.columns:
    top_recipes = df.sort_values(by="bayesian_score", ascending=False).head(10)
    st.bar_chart(top_recipes.set_index("name")["bayesian_score"])
else:
    st.info("Bayesian score data available in search view.")
