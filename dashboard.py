import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# 1. PAGE LAYOUT CONFIGURATION
st.set_page_config(
    page_title="HORIZON ADDIS TYRE — Store Satisfaction Hub",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. INJECT ARTISTIC INDUSTRIAL THEME CSS
st.markdown("""
    <style>
    /* Main App Background */
    .stApp {
        background: linear-gradient(135deg, #12181f 0%, #1a232e 100%);
        color: #e2e8f0;
    }
    
    /* Header Custom Typography styling */
    .main-title {
        font-family: 'Helvetica Neue', Arial, sans-serif;
        font-size: 42px;
        font-weight: 800;
        letter-spacing: 2px;
        color: #ffffff;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.6);
        margin-bottom: 5px;
    }
    
    .sub-title {
        font-family: 'Segoe UI', sans-serif;
        font-size: 20px;
        font-weight: 400;
        color: #00ffd0; 
        margin-bottom: 25px;
    }
    
    .section-header {
        font-family: 'Arial Black', Gadget, sans-serif;
        font-size: 24px;
        color: #ffc107; /* Industrial Gold */
        border-left: 5px solid #ffc107;
        padding-left: 10px;
        margin-top: 20px;
        margin-bottom: 15px;
    }

    /* --- YELLOW AND BOLD LIVE ANALYTICS TEXT METRICS --- */
    div[data-testid="stMetricValue"] {
        color: #ffc107 !important;
        font-weight: 900 !important;
        font-size: 36px !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.8);
    }
    div[data-testid="stMetricLabel"] {
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 16px !important;
    }

    /* --- TAB NAVIGATION VISIBILITY --- */
    button[data-baseweb="tab"] {
        color: #ffffff !important;         
        font-size: 22px !important;        
        font-weight: 700 !important;        
        font-family: 'Segoe UI', sans-serif;
        padding: 12px 24px !important;
    }
    
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #ffc107 !important;         
        border-bottom-color: #ffc107 !important;
    }

    /* --- DROPDOWN SELECTION BAR CUSTOMIZATION (Light Rose Theme) --- */
    div[data-basename="selectbox"] > div, 
    div[data-testid="stSelectbox"] > div {
        background-color: #ffe4e1 !important; 
        border-radius: 8px !important;
        border: 2px solid #ffb6c1 !important; 
    }
    
    div[data-testid="stSelectbox"] div[data-baseweb="select"] span,
    div[data-testid="stSelectbox"] div[aria-selected="true"] {
        color: #12181f !important;           
        font-weight: 600 !important;
        font-size: 16px !important;
    }

    /* Elegant Glass Container styling for Cards & Question Blocks */
    div[data-testid="stForm"], .stMetric, div[data-testid="stMarkdownContainer"] hr {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 12px !important;
        padding: 20px !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37) !important;
    }

    div[data-testid="stRadio"] label {
        color: #ffffff !important;
        font-size: 16px !important;
        font-weight: bold !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. DATA ARCHITECTURE RECONSTRUCTION
DEPARTMENTAL_CRITERIA = {
    "PIQA": ["Inventory procedures", "Expired monitoring", "Work order validation", "Damage prevention", "Speed & clarity", "Raw material decisions", "Reception hospitality"],
    "Production": ["Timely mixing delivery", "Green tags compliance", "Leakage containment", "Metallic pallets usage", "Cord roll handling", "Worker hospitality"],
    "S&M": ["Inventory visibility", "External customer satisfaction", "Conflict resolution", "Information quality", "Waiting time reduction", "Hospitality index"],
    "Purchase": ["Order update tracking", "Timely query response", "Specifications adequacy", "Report delivery speed", "Efficient unloading", "Driver coordination", "Cooperation index"],
    "PMITS": ["System deployment speed", "Reporting quality", "Feedback optimization", "Supply provisions", "Cooperation metrics"],
    "Finance": ["ERP processing schedules", "Audit execution", "Data speed delivery", "Supply lines dispatch", "Recommendation response", "Staff sincerity"],
    "PE": ["Urgent follow-ups", "Technical updates", "Standards verification", "Inter-department support", "Reception processing"],
    "HR": ["Performance evaluations", "Manpower deployments", "Discipline monitoring", "Training operations", "Leave administration", "Supply chain speeds", "Common areas maintenance", "Cooperation index"],
    "Safety Section": ["Guidelines obedience", "Signs infrastructure", "Risk reduction advice", "Material lookup accuracy", "Customer handling"],
    "Security": ["Shipment protocols", "Theft counter-measures", "Risk instruction orders", "Consultation transparency", "Lookups processing", "Service delivery"]
}

if "survey_db" not in st.session_state:
    historical_logs = []
    np.random.seed(42)
    # Generate numerical indices for the 3D axis coordinates
    for d_idx, (d_name, q_list) in enumerate(DEPARTMENTAL_CRITERIA.items()):
        for r_id in range(4):
            scores = [np.random.randint(3, 6) for _ in q_list]
            mean_val = round(float(np.mean(scores)), 2)
            historical_logs.append({
                "Timestamp": f"2026-06-20 10:{12 * r_id}:00",
                "Timeline_Hour": 10 + r_id, 
                "Department": d_name,
                "Dept_Index": d_idx,
                "Average Score": mean_val,
                "Feedback Comments": "Automatic plant verification log."
            })
    st.session_state["survey_db"] = historical_logs

# 4. BRANDING HEADER
st.markdown('<div class="main-title">🏭 HORIZON ADDIS TYRE</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Store Management Department — Internal Quality & Satisfaction Engine</div>', unsafe_allow_html=True)

form_tab, dashboard_tab = st.tabs(["📋 Fill Department Evaluation", "📈 Live Performance Dashboard"])

# ==========================================
# TAB 1: SURVEY LOGIC FORM
# ==========================================
with form_tab:
    st.markdown('<div class="section-header">Active Evaluation Form Entry</div>', unsafe_allow_html=True)
    target_dept = st.selectbox("Select Your Submitting Department:", options=list(DEPARTMENTAL_CRITERIA.keys()), key="form_dept_selector")
    
    questions = DEPARTMENTAL_CRITERIA[target_dept]
    form_scores = []
    
    with st.form(key=f"survey_form_container_{target_dept}", clear_on_submit=True):
        for idx, text in enumerate(questions):
            st.markdown(f"<div style='font-size:16px; font-weight:600; color:#ffffff; margin-top:10px;'>Q{idx+1}: {text}</div>", unsafe_allow_html=True)
            val = st.radio("Rating:", options=[1, 2, 3, 4, 5], index=3, horizontal=True, key=f"score_input_{target_dept}_{idx}", label_visibility="collapsed")
            form_scores.append(val)
            st.markdown("<hr style='border:1px dashed rgba(255,255,255,0.15); margin: 15px 0;'>", unsafe_allow_html=True)
            
        text_remarks = st.text_area("Provide any additional industrial remarks or operations feedback:", key=f"notes_{target_dept}")
        submit_form = st.form_submit_button("Submit Evaluation Entry", width="content")
        
        if submit_form:
            final_mean = round(float(np.mean(form_scores)), 2)
            d_idx = list(DEPARTMENTAL_CRITERIA.keys()).index(target_dept)
            payload = {
                "Timestamp": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Timeline_Hour": 14,
                "Department": target_dept,
                "Dept_Index": d_idx,
                "Average Score": final_mean,
                "Feedback Comments": text_remarks if text_remarks else "No remarks filed."
            }
            st.session_state["survey_db"].append(payload)
            st.success(f"🎉 Logs filed! Matrix Score: {final_mean} / 5.0")
            st.rerun()

# ==========================================
# TAB 2: LIVE METRICS REPORTING DASHBOARD
# ==========================================
with dashboard_tab:
    st.markdown('<div class="section-header">Live Analytics Reporting Engine</div>', unsafe_allow_html=True)
    df_current = pd.DataFrame(st.session_state["survey_db"])
    
    filter_dept = st.selectbox("Isolate Dashboard View Scope:", options=["All Departments"] + list(DEPARTMENTAL_CRITERIA.keys()), key="dashboard_dept_selector")
    df_view = df_current if filter_dept == "All Departments" else df_current[df_current["Department"] == filter_dept]

    # Display Metrics (styled in bold yellow via the CSS injection above)
    m_col1, m_col2, m_col3 = st.columns(3)
    with m_col1:
        st.metric("Total Surveys Processed", value=len(df_view))
    with m_col2:
        global_index = round(df_view["Average Score"].mean(), 2) if not df_view.empty else 0.0
        st.metric("Mean Satisfaction Index", value=f"{global_index} / 5.0")
    with m_col3:
        top_unit = df_current.groupby("Department")["Average Score"].mean().idxmax() if not df_current.empty else "None"
        st.metric("Top Plant Partner", value=top_unit)
        
    st.markdown("<br>", unsafe_allow_html=True)
    fig_col1, fig_col2 = st.columns(2)
    
    with fig_col1:
        st.markdown("<h5 style='color:white;text-align:center;'>Proportional Venn Diagram (Sunburst Distribution)</h5>", unsafe_allow_html=True)
        if not df_current.empty:
            # Create categorical ranges to serve as Venn intersection zones
            df_current["Rating_Group"] = pd.cut(df_current["Average Score"], bins=[0, 3.5, 4.5, 5.0], labels=["Standard (0-3.5)", "Target (3.5-4.5)", "Optimal (4.5-5.0)"])
            fig_venn = px.sunburst(
                df_current,
                path=["Rating_Group", "Department"],
                values="Average Score",
                template="plotly_dark",
                color_continuous_scale=px.colors.sequential.Sunsetdark
            )
            fig_venn.update_layout(margin=dict(l=10, r=10, t=10, b=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_venn, width="stretch", key="venn_sunburst_chart")
            
    with fig_col2:
        st.markdown("<h5 style='color:white;text-align:center;'>3D Rotatable Line & Scatter Matrix Mesh</h5>", unsafe_allow_html=True)
        if not df_view.empty:
            # Interactive 3D plotting matrix space
            fig_3d = px.scatter_3d(
                df_view,
                x="Timeline_Hour",
                y="Dept_Index",
                z="Average Score",
                color="Average Score",
                hover_name="Department",
                template="plotly_dark",
                color_continuous_scale=px.colors.sequential.Goldred
            )
            # Render a 3D line connectors mesh
            fig_3d.update_traces(marker=dict(size=6, opacity=0.9), line=dict(width=4, color="#ffc107"))
            fig_3d.update_layout(
                scene=dict(
                    xaxis_title='Timeline Tracker (Hr)',
                    yaxis_title='Dept Cluster Key',
                    zaxis_title='Score Metrics',
                    backgroundcolor="rgba(0,0,0,0)"
                ),
                margin=dict(l=0, r=0, t=10, b=0),
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_3d, width="stretch", key="3d_timeline_mesh_chart")

    st.markdown("---")
    st.markdown('<div class="section-header">Detailed Records Registry View</div>', unsafe_allow_html=True)
    st.dataframe(df_view.sort_values(by="Timestamp", ascending=False), width="stretch", hide_index=True)
