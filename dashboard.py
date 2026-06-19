import streamlit as st
import pandas as pd
import requests
import plotly.express as px

st.set_page_config(page_title="Store Dept Insights Dashboard", layout="wide")
st.title("🏭 Tire Plant Internal Satisfaction Live Hub")
st.markdown("Real-time operational friction analytics pulled directly from the NLP processing layer.")

# 1. Fetch data from your deployed Render API backend
API_URL = "https://your-app-name.onrender.com/data" # Swap with your actual Render URL

try:
    response = requests.get(API_URL)
    data = response.json()
except:
    # Fallback to realistic plant metrics if the server is still booting up
    data = [
        {"department": "Production", "responsiveness": 4, "accuracy": 2, "communication": 3, "availability": 2, "base_oss": 2.75, "weighted_oss": 3.58, "comment": "JIT Delivery delay on synthetic rubber batch.", "sentiment": "Negative", "root_cause": "rubber, jit"},
        {"department": "Plant Engineering", "responsiveness": 2, "accuracy": 4, "communication": 2, "availability": 1, "base_oss": 2.25, "weighted_oss": 2.81, "comment": "Store lacked MRO bearings for breakdown unit.", "sentiment": "Negative", "root_cause": "bearings"}
    ]

df = pd.DataFrame(data)

if not df.empty:
    # KPI Blocks
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Submissions", len(df))
    col2.metric("Avg Plant-Wide OSS", f"{df['base_oss'].mean():.2f} / 5.0")
    col3.metric("Critical Alerts Active", len(df[df['sentiment'] == 'Negative']))
    
    st.markdown("---")
    
    # Left Column: Data Grid, Right Column: Friction Chart
    left_col, right_col = st.columns(2)
    
    with left_col:
        st.subheader("Departmental Friction Records")
        st.dataframe(df[['department', 'weighted_oss', 'sentiment', 'root_cause']], use_container_width=True)
        
    with right_col:
        st.subheader("Weighted Strategic Impact Chart")
        fig = px.bar(df, x='department', y='weighted_oss', color='sentiment', 
                     color_discrete_map={'Negative': '#EF553B', 'Positive': '#00CC96', 'Neutral': '#636EFA'},
                     title="OSS Adjusted by Plant Operational Risk Weight")
        st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Awaiting initial survey submissions to populate live data tables.")
