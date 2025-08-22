# dashboard.py
import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
import os

# Load cleaned data
df = pd.read_csv("../data/processed/YouTubeData_Cleaned.csv")

# Title
st.title("📊 YouTube Analytics Dashboard")

# ========== Section 1: Data Overview ==========
st.subheader("📌 Data Overview")
st.write(df.head())

# ========== Section 2: Visualizations ==========
st.subheader("📈 Views Trend Over Time")
fig1 = px.line(df, x="PublishedDate", y="Views", title="Views Over Time")
st.plotly_chart(fig1)

st.subheader("🔥 Top 10 Videos by Views")
top_videos = df.sort_values(by="Views", ascending=False).head(10)
fig2 = px.bar(top_videos, x="Title", y="Views", title="Top 10 Videos")
st.plotly_chart(fig2)

st.subheader("💬 Engagement Breakdown")
fig3 = px.pie(df, names="Category", values="Views", title="Category-wise Views")
st.plotly_chart(fig3)

# ========== Section 3: ML Predictions ==========
st.subheader("🤖 ML Model – Predicting Video Views")
if os.path.exists("../models/youtube_regression.pkl"):
    model = joblib.load("../models/youtube_regression.pkl")

    likes = st.number_input("Enter Likes", min_value=0)
    comments = st.number_input("Enter Comments", min_value=0)
    shares = st.number_input("Enter Shares", min_value=0)

    if st.button("Predict Views"):
        prediction = model.predict([[likes, comments, shares]])[0]
        st.success(f"🔮 Predicted Views: {int(prediction)}")

# Show evaluation metrics
st.subheader("📊 Model Evaluation Metrics")
st.write("R² Score: 0.85 (example)")  # replace with actual values printed in ml_model.py
st.write("MAE: 1200.50")
st.write("RMSE: 3000.75")

# ========== Section 4: Geospatial Mapping ==========
if "Country" in df.columns:
    st.subheader("🌍 Views by Country")
    country_data = df.groupby("Country")["Views"].sum().reset_index()
    fig4 = px.choropleth(country_data, locations="Country", locationmode="country names",
                         color="Views", title="Views Distribution by Country")
    st.plotly_chart(fig4)

# ========== Section 5: Insights ==========
st.subheader("💡 Business Insights")
top_category = df.groupby("Category")["Views"].sum().idxmax()
st.write(f"✅ The best-performing category is **{top_category}**.")
st.write("📌 Strategy: Focus more on creating content in this category for maximum reach.")
