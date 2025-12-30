import streamlit as st
import pandas as pd
import json
from transformers import pipeline
import plotly.express as px

# --- 1. CONFIGURATION & LIGHTWEIGHT MODEL LOADING ---
st.set_page_config(page_title="2023 Brand Monitor", layout="wide")

@st.cache_resource
def get_classifier():
    """
    Loads TinyBERT: The smallest possible transformer model to avoid 503 errors.
    device=-1 ensures CPU usage for stability.
    """
    return pipeline(
        "sentiment-analysis", 
        model="prajjwal1/bert-tiny",
        device=-1
    )

# Initialize the model
classifier = get_classifier()

# --- 2. DATA LOADING ---
@st.cache_data
def load_data():
    try:
        with open('data.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("data.json not found. Please run scraper.py first.")
        return None

data = load_data()

# --- 3. UI - SIDEBAR NAVIGATION ---
st.title("🛡️ 2023 Brand Reputation Monitor")
st.sidebar.header("Navigation")
choice = st.sidebar.selectbox("Select Page", ["Products", "Testimonials", "Reviews Analysis"])

if data:
    # --- 4. PAGE: PRODUCTS ---
    if choice == "Products":
        st.header("📦 Scraped Products")
        st.table(pd.DataFrame(data['products']))

    # --- 5. PAGE: TESTIMONIALS ---
    elif choice == "Testimonials":
        st.header("💬 Customer Testimonials")
        for t in data['testimonials']:
            with st.chat_message("user"):
                st.write(f"**{t['user']}**")
                st.write(t['content'])

    # --- 6. PAGE: REVIEWS ANALYSIS (CORE FEATURE) ---
    elif choice == "Reviews Analysis":
        st.header("🧠 Sentiment Analysis (TinyBERT)")
        
        # Month Selection Slider
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        selected_month = st.select_slider("Select Month in 2023", options=months)
        
        # Filtering Logic
        month_num = str(months.index(selected_month) + 1).zfill(2)
        df = pd.DataFrame(data['reviews'])
        filtered_df = df[df['date'].str.contains(f"2023-{month_num}")].copy()

        if not filtered_df.empty:
            # AI Classification
            with st.spinner("Analyzing..."):
                results = classifier(filtered_df['text'].tolist())
                filtered_df['Sentiment'] = [r['label'] for r in results]
                filtered_df['Confidence'] = [round(r['score'], 4) for r in results]

            # --- VISUALIZATION ---
            chart_data = filtered_df.groupby('Sentiment').agg(
                Count=('Sentiment', 'count'),
                Avg_Confidence=('Confidence', 'mean')
            ).reset_index()

            fig = px.bar(
                chart_data, x='Sentiment', y='Count', color='Sentiment',
                hover_data={'Avg_Confidence': ':.4f'},
                title=f"Sentiment Distribution: {selected_month} 2023"
            )
            st.plotly_chart(fig, use_container_width=True)
            st.dataframe(filtered_df, use_container_width=True)
        else:
            st.warning(f"No reviews found for {selected_month} 2023.")
