import streamlit as st
import pandas as pd

st.title("Recipe insights and analytics")

@st.cache_data
def load_data():
   return pd.read_csv("processed_recipes.csv")

def = load_data()

#summary metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total recipes", len(df))
col2.metric("Average rating", f"{df['avg_rating'].mean():.2f}")
col3.metric("Total reviews", f"{int(df['review_count'].sum()):,}")

st.divider()

#chart 1 : Top rated recipes
st.subheader("Top 10 recipes by bayesian ratings")

top_recipes = df.sort_values(
  by ="bayesian_rating", ascending = False
).head(10)

st.bar_chart(top_recipes.set_index("name")["bayesian_rating"])

#chart 2 : Rating distribution
st.subheader("Distribution of recipe ratings")

rating_counts = pd.cut(
  df["avg_rating"],
  bins = [0,1,2,3,4,5],
  labels = ["0-1", "1-2", "2-3", "3-4", "4-5"],
  include_lowest = True
).value_counts().sort_index()

st.bar_chart(rating_counts)

#chart 3: Most reviewed recipes
st.subheader("Top 10 most reviewed recipes")

most_reviewed = df.sort_values(
  by = "review_count", ascending = False
).head(10)

st.bar_chart(most_reviewed.set_index("name")["review_count"])
  
