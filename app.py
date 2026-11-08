import streamlit as st
import pandas as pd
import os

# App Title & Header
st.title("Rate my recipe")
st.write("Welcome! Search for your favourite recipe.")

# Load Data Safely
@st.cache_data
def load_data():
    for path in ['data/processed_recipes.csv', '../data/processed_recipes.csv', 'processed_recipes.csv']:
        if os.path.exists(path):
            return pd.read_csv(path)
    return None

df = load_data()

if df is not None:
    st.success("recipe dataset loaded successfully")
    
    # Search Box
    search_query = st.text_input(
        "Search for a recipe:",
        placeholder="try chicken or chocolate"
    )

    if search_query:
        matches = df[df['name'].astype(str).str.contains(search_query, case=False, na=False)]
        best_matches = matches.sort_values(by='bayesian_rating', ascending=False).head(10)
        
        if not best_matches.empty:
            st.subheader("Your recipe recommendations")
            
            for idx, row in best_matches.iterrows():
                st.subheader(row['name'])
                
                col1, col2, col3 = st.columns(3)
                col1.metric("bayesian score", f"{row['bayesian_rating']:.2f}")
                col2.metric("average rating", f"{row['avg_rating']:.2f}")
                col3.metric("review count", int(row['review_count']))
                
                st.write(f"preparation time: {row['minutes']} minutes")
                st.write(f"number of steps: {row['n_steps']}")
                st.markdown("---")
        else:
            st.warning("oppss, no recipes found matching that keyword. try another one, thank you!")
else:
    st.error("Dataset file 'processed_recipes.csv' not found! Please check your data folder.")