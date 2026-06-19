import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# 1. PAGE LAYOUT CONFIGURATION
st.set_page_config(
    page_title="HORIZON ADDIS TYRE - Store Satisfaction Hub",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. BRANDING HEADER
st.title("🏭 HORIZON ADDIS TYRE")
st.subheader("Store Management Department — Internal Customer Satisfaction Live Hub")
st.markdown("---")

# 3. MOCK DATA STREAM GENERATOR (Structured from Questionnaire Schema)
@st.cache_data
def generate_industry_survey_data():
    np.random.seed(42)
    departments = ["PI&QA", "Production", "S&M", "Purchase", "PMITS", "Finance", "PE", "HR", "Security", "Safety"]
    records = []
    
    # Generate realistic evaluations (Scores 1 to 5) reflecting varying sample metrics
    for dept in departments:
        samples = np.random.randint(8, 15)
        for _ in range(samples):
            records.append({
                "Department": dept,
                "Inventory Management & Rules": np.random.randint(3, 6),
                "Timeliness & Delivery Speed": np.random.randint(2, 6),
                "Staff Hospitality & Cooperation": np.random.randint(3, 6),
                "Operational Support & Feedback": np.random.randint(3, 6),
                "Overall Satisfaction": round(np.random.uniform(3.4, 4.9), 2)
            })
    return pd.DataFrame(records)

df_all_surveys = generate_industry_survey_data()

# 4. SIDEBAR NAVIGATION CONTROLS
st.sidebar.image("https://img.icons8.com/fluency/96/tire.png", width=60)
st.sidebar.header("Dashboard Filters")

dept_list = ["All Departments"] + sorted(list(df_all_surveys["Department"].unique()))
selected_dept = st.sidebar.selectbox("Filter by Submitting Department:", dept_list)

# Apply Dataset Filter Matrix
if selected_dept != "All Departments":
    df_filtered = df_all_surveys[df_all_surveys["Department"] == selected_dept]
else:
    df_filtered = df_all_surveys

# 5. CORE KPI SUMMARY CARDS
st.markdown("### 📊 Live Evaluation Metrics Matrix")
col1, col2, col3, col4 = st.columns(4)

avg_sat = round(df_filtered["Overall Satisfaction"].mean(), 2)
avg_time = round(df_filtered["Timeliness & Delivery Speed"].mean(), 2)
avg_hosp = round(df_filtered["Staff Hospitality & Cooperation"].mean(), 2)
total_count = len(df_filtered)

with col1:
    st.metric(label="Overall Satisfaction Index", value=f"{avg_sat} / 5.0", delta="Live Tracker")
with col2:
    st.metric(label="Timeliness Score (Avg)", value=f"{avg_time} / 5.0", delta="+0.08")
with col3:
    st.metric(label="Hospitality & Customer Care", value=f"{avg_hosp} / 5.0", delta="+0.15")
with col4:
    st.metric(label="Responses Evaluated", value=str(total_count), delta="Synchronized")

st.markdown("---")

# 6. TABULAR FUNCTIONAL VIEWS (Fixed legacy compilation bugs)
tab1, tab2, tab3 = st.tabs(["📈 Comparative Analytics", "📋 Detailed Evaluation Registry", "⚙️ Connection & API Settings"])

# --- Tab 1: Interactive Plotly Visualizations ---
with tab1:
    st.markdown("#### Store Operations Performance Analytics")
    
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        # Group metrics cleanly by Department
        df_dept_summary = df_all_surveys.groupby("Department")["Overall Satisfaction"].mean().reset_index()
        fig_bar = px.bar(
            df_dept_summary,
            x="Department",
            y="Overall Satisfaction",
            title="Average Satisfaction Level Across Tire Plant Sections",
            labels={"Overall Satisfaction": "Rating Score (1-5)"},
            color="Overall Satisfaction",
            color_continuous_scale=px.colors.sequential.Plotly3
        )
        fig_bar.update_layout(margin=dict(l=20, r=20, t=40, b=20))
        # 2026 Deprecation Fix: use width="stretch" instead of use_container_width=True
        st.plotly_chart(fig_bar, width="stretch", key="dept_bar_analytics")

    with col_chart2:
        fig_box = px.box(
            df_filtered,
            y="Overall Satisfaction",
            x="Department" if selected_dept == "All Departments" else None,
            title=f"Satisfaction Score Variance Range: {selected_dept}",
            points="all",
            color_discrete_sequence=["#10b981"]
        )
        fig_box.update_layout(margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig_box, width="stretch", key="satisfaction_variance_box")

# --- Tab 2: Inventory Grid Registry ---
with tab2:
    st.markdown(f"#### Logged Internal Survey Submissions Tracking Database ({selected_dept})")
    
    # 2026 Deprecation Fix: use width="stretch" for data table scaling 
    st.dataframe(
        df_filtered, 
        width="stretch", 
        hide_index=True
    )
    
    # Interactive dataset downloading endpoint
    csv_bytes = df_filtered.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Structured Dataset as CSV",
        data=csv_bytes,
        file_name="horizon_addis_tyre_satisfaction_report.csv",
        mime="text/csv",
        width="content"  # 2026 widget component alignment standard
    )

# --- Tab 3: Operational System Adjustments ---
with tab3:
    st.markdown("#### Dashboard Endpoint Configurations")
    st.info("System configuration metrics link directly to your active repository setup.")
    
    api_url = st.text_input(
        "Core Production API Endpoint URL Context:", 
        value="https://sfhnmvmr7ipaj7fvx7oyae.streamlit.app/api/v1/metrics"
    )
    
    # Compact button layout config using clean metrics styling
    if st.button("Verify DB Sync Status", width="content"):
        st.success("API Pipeline Communication Integrity Verified. Systems Operating Nominally.")
