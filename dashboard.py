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

# 3. FULL DATA ARCHITECTURE (RESTORED FULL QUESTIONS)
DEPARTMENTAL_CRITERIA = {
    "PIQA": [
        "How do you rate the inventory procedures and material tracking inside the shop floor?",
        "Are expired or degraded compound elements monitored and flagged efficiently?",
        "How accurately are technical work orders validated before implementation?",
        "Rate the damage prevention measures applied to processed raw tires during storage.",
        "How do you evaluate the speed and clarity of technical communications from PIQA?",
        "Are raw material usage decisions aligned properly with standard operating procedures?",
        "Rate the overall reception hospitality and cooperation experienced with the PIQA team."
    ],
    "Production": [
        "How efficient is the timely delivery of rubber mixing materials to the assembly lines?",
        "Are green compliance tags strictly observed and maintained across all tire batches?",
        "How effectively are material leakages and compound waste contained in your area?",
        "Rate the suitability and condition of metallic pallets used for shipping rubber sheets.",
        "Are cord rolls handled and stored with proper respect to tension and safety standards?",
        "Rate the general hospitality and working relationship with the production floor staff."
    ],
    "S&M": [
        "How transparent and accessible is the real-time finished tire inventory visibility?",
        "How do you rate external customer satisfaction responses routed through sales?",
        "Are inter-departmental conflicts or order modifications resolved fairly and quickly?",
        "Rate the precise quality and correctness of supply dispatch notes and technical info.",
        "How effectively has the sales department worked to reduce order waiting times?",
        "Rate the overall hospitality and customer-centric attitude index of the S&M team."
    ],
    "Purchase": [
        "How closely are raw material purchase orders and tracking updates shared with operations?",
        "Are timely responses provided when technical material queries are sent to purchasing?",
        "How adequate are the final specifications of tools and spare components purchased?",
        "Rate the delivery speed of procurement reports and market assessment audits.",
        "How efficient is the unloading and receiving process at the incoming materials gate?",
        "Rate the coordination and transit transparency provided for regional delivery drivers.",
        "Evaluate the cooperation and communication index experienced with purchasing officers."
    ],
    "PMITS": [
        "How do you rate the deployment and maintenance speed of plant network infrastructure?",
        "Are internal server reporting dashboards updated accurately without missing telemetry?",
        "How effectively is user feedback integrated into software and database optimizations?",
        "Are general IT supplies, workstations, and terminal provisions adequate?",
        "Rate the overall communication and technical cooperation metrics of the PMITS crew."
    ],
    "Finance": [
        "Are ERP invoice processing and clearance schedules completed within timeline targets?",
        "How transparent and collaborative is the internal cost audit execution process?",
        "Rate the delivery speed of accurate financial data sheets requested by management.",
        "Are funding and credit authorizations for urgent supply lines dispatched on time?",
        "How constructively does the finance team respond to procedural recommendations?",
        "Rate the approachability, operational sincerity, and helpfulness of finance personnel."
    ],
    "PE": [
        "How quickly are urgent equipment follow-ups and plant engineering modifications resolved?",
        "Are technical design updates and machine schematics clearly communicated?",
        "How rigorously are equipment calibration standards verified across shift transfers?",
        "Rate the level of inter-department technical support offered during major breakdowns.",
        "How smoothly are engineering intake reports and work requests processed at reception?"
    ],
    "HR": [
        "Are performance evaluations completed fairly and communicated constructively?",
        "How efficiently is floor manpower deployed to clear operational plant bottlenecks?",
        "Are labor discipline monitoring systems balanced, objective, and transparent?",
        "Rate the quality, accessibility, and utility of active plant technical training operations.",
        "How smoothly and quickly is annual or medical leave administration processed?",
        "Are basic logistics and personnel transport lines operating at target transit speeds?",
        "How well maintained are common areas, cafeterias, and change locker infrastructure?",
        "Evaluate the general cooperation index and conflict resolution skills of HR staff."
    ],
    "Safety Section": [
        "Are industrial safety guidelines and PPE obedience monitored strictly on the floor?",
        "Is the warning sign infrastructure visible, updated, and well-placed around risks?",
        "How actionable and proactive is the risk reduction advice provided by safety inspectors?",
        "How accurate is the safety material lookup database during hazard identification?",
        "Rate the hospitality and supportive handling of emergency reporting incidents."
    ],
    "Security": [
        "Are shipment entry and exit inspection protocols executed rigorously at the gates?",
        "How robust are the plant theft counter-measures and perimeter surveillance systems?",
        "Are emergency risk instruction orders conveyed clearly to personnel during alarms?",
        "How transparent and professional are consultation procedures during incident audits?",
        "Are transport gate pass lookups processed without causing logistical delivery delays?",
        "Rate the overall hospitality, fairness, and vigilance shown during service delivery."
    ]
}

if "survey_db" not in st.session_state:
    historical_logs = []
    np.random.seed(42)
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

    # Display Metrics
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
            df_current["Rating_Group"] = pd.cut(df_current["Average Score"], bins=[0, 3.5, 4.5, 5.0], labels=["Standard (0-3.5)", "Target (3.5-4.5)", "Optimal (4.5-5.0)"])
            
            fig_venn = px.sunburst(
                df_current,
                path=["Rating_Group", "Department"],
                values="Average Score",
                color_discrete_sequence=["#ffc107"] 
            )
            fig_venn.update_layout(
                margin=dict(l=10, r=10, t=10, b=10), 
                paper_bgcolor='rgba(0,0,0,0)', 
                plot_bgcolor='rgba(0,0,0,0)'
            )
            fig_venn.update_traces(
                textinfo="label+value",
                insidetextfont=dict(color="#ffffff", size=14, family="Arial Black")
            )
            st.plotly_chart(fig_venn, width="stretch", key="venn_sunburst_chart")
            
    with fig_col2:
        st.markdown("<h5 style='color:white;text-align:center;'>Operational Performance Density Heatmap</h5>", unsafe_allow_html=True)
        
        if not df_view.empty:
            # FIXED: Replaced the troubleshooting 3D layout entirely with a stable 2D Density Heatmap Matrix 
            fig_density = px.density_heatmap(
                df_view,
                x="Timeline_Hour",
                y="Department",
                z="Average Score",
                histfunc="avg",
                template="plotly_dark",
                color_continuous_scale=["#12181f", "#ffc107", "#ff5722", "#d50000"],
                labels={"Timeline_Hour": "Timeline Tracker (Hr)", "Department": "Department Category", "color": "Score Avg"}
            )
            
            # Inject your text message via safe standard layout attributes
            fig_density.update_layout(
                title=dict(
                    text="<b>Perfect, send this message on live analytics result graph.</b>",
                    x=0.5,
                    y=0.98,
                    xanchor="center",
                    yanchor="top",
                    font=dict(color="#ffc107", size=13, family="Arial")
                ),
                xaxis=dict(showgrid=False, tickmode="linear"),
                yaxis=dict(showgrid=False),
                margin=dict(l=20, r=20, t=50, b=20),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig_density, width="stretch", key="heatmap_perf_matrix_chart")
        else:
            st.info("Waiting for target data metrics to render layout configuration...")

    st.markdown("---")
    st.markdown('<div class="section-header">Detailed Records Registry View</div>', unsafe_allow_html=True)
    st.dataframe(df_view.sort_values(by="Timestamp", ascending=False), width="stretch", hide_index=True)
