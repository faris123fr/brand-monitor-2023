import streamlit as st
import pandas as pd
import json
from transformers import pipeline
import plotly.express as px

# Load the AI Model
@st.cache_resource
def get_classifier():
    return pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

classifier = get_classifier()

# Load Scraped Data
with open('data.json', 'r') as f:
    data = json.load(f)

st.title("🛡️ 2023 Brand Reputation Monitor")

# Sidebar Navigation
choice = st.sidebar.selectbox("Select Page", ["Products", "Testimonials", "Reviews Analysis"])

if choice == "Products":
    st.header("Available Products")
    st.table(pd.DataFrame(data['products']))

elif choice == "Testimonials":
    st.header("What Customers Say")
    for t in data['testimonials']:
        st.chat_message("user").write(f"{t['user']}: {t['content']}")

elif choice == "Reviews Analysis":
    st.header("Deep Learning Sentiment Analysis")
    
    # Month Filter
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    selected_month = st.select_slider("Select Month (2023)", options=months)
    
    # Filtering Logic
    month_num = str(months.index(selected_month) + 1).zfill(2)
    df = pd.DataFrame(data['reviews'])
    filtered_df = df[df['date'].str.contains(f"2023-{month_num}")].copy()

    if not filtered_df.empty:
        # AI Classification
        results = classifier(filtered_df['text'].tolist())
        filtered_df['Sentiment'] = [r['label'] for r in results]
        filtered_df['Confidence'] = [round(r['score'], 3) for r in results]

        # Bar Chart
        fig = px.bar(filtered_df['Sentiment'].value_counts(), title="Positive vs Negative Counts")
        st.plotly_chart(fig)
        
        # Display Table
        st.dataframe(filtered_df)
    else:
        st.warning(f"No reviews found for {selected_month} 2023.")