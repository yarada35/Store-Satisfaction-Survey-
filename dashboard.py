import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# 1. PAGE SETUP & THEME CONTEXT
st.set_page_config(
    page_title="HORIZON ADDIS TYRE — Internal Satisfaction Hub",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. DICTIONARY CONTAINING RAW CRITERIA DIRECTLY EXTRACTED FROM YOUR JSON FILES
DEPARTMENTAL_CRITERIA = {
    "PIQA": [
        "Maintaining inventory of products and raw materials in accordance with established procedures and standards.",
        "Regarding the handling and monitoring of expired products.",
        "Receive and implement work orders and expert opinions on product and raw material management.",
        "Work according to the operating system to prevent products and raw materials from being damaged.",
        "Providing the goods and information you need quickly and clearly.",
        "Providing timely information regarding the decision to pass incoming raw materials and implementing the decision accordingly.",
        "Employee reception and information reception."
    ],
    "Production": [
        "Requested raw materials are delivered on time to mixing area.",
        "Delivered items are labeled with Green tag always.",
        "Delivered items are free from Foreign material & leakage.",
        "Natural rubber is delivered with proper metallic pallet requirement.",
        "Cord roll handling & storing condition.",
        "Customer handling ability and hospitality of store workers."
    ],
    "S&M": [
        "Provide quality inventory reports on time.",
        "Store operating system ensures the satisfaction of External customers.",
        "Willingness and commitment to jointly resolve workplace problems and disagreements.",
        "Get the goods and information you need in a timely and quality manner.",
        "Regarding store implementation of the Waiting time for external customers.",
        "Staff hospitality and timely customer service."
    ],
    "Purchase": [
        "Providing updated information regarding all purchase requests.",
        "Responding requests from the purchasing department in a timely manner.",
        "Providing the necessary information/ specifications in adequate manner for goods/ services to be purchased.",
        "Provide timely and quality raw material inventory reports.",
        "When a purchased item arrives, it must be handled and received efficiently.",
        "Handling drivers carrying goods purchased from domestic and foreign countries in a timely and quality manner.",
        "Employee hospitality and cooperation."
    ],
    "PMITS": [
        "Implementing deployed systems efficiently and as required.",
        "Providing required reports in a timely and quality manner.",
        "Accept and implement feedback.",
        "Delivering the goods you need quickly and with quality.",
        "Good hospitality and cooperation of employees."
    ],
    "Finance": [
        "ERP and inventory data processing And delivering in a timely and quality Manner.",
        "Work efficiently and effectively during planned product inventory, as well as preparation and work.",
        "Getting the information you need in quality and on time.",
        "Delivering the goods you want with quality and speed.",
        "Accept and implement the recommendations given.",
        "The sincerity and hospitality of the staff."
    ],
    "PE": [
        "Follow up on urgent purchase orders, place orders and provide information when received.",
        "Providing the property and information you need in a Clear and concise Manner.",
        "Verify with the relevant body that the purchased items are in accordance with the standards.",
        "Collaboration for any support Request from your department.",
        "Staff orientation and customer service and Reception."
    ],
    "HR": [
        "Timely report employees performance evaluation result.",
        "Timely request the department's manpower recruitment.",
        "Proper Handling of employees with a discipline case or Handling of low performers.",
        "Appropriate and timely planning and execution of trainings for employees.",
        "Proper employee leave management.",
        "Delivering the goods you need quickly and with quality.",
        "Responsible for cleaning and other related tasks in the common areas.",
        "Good hospitality and cooperation of employees."
    ],
    "Safety Section": [
        "Carrying out work in accordance with established safety guidelines.",
        "Supervision and work in the use and maintenance of safety signs.",
        "Accepting and implementing expert advice to protect assets in warehouses from hazards.",
        "Find the item you want quickly and with quality.",
        "Staff hospitality and customer reception and handling."
    ],
    "Security": [
        "Working according to a jointly agreed procedure during the shipment.",
        "Work with security personnel to protect products from damage and theft.",
        "Accepting and carrying out work orders from professionals to protect property from danger.",
        "Solving problems during shipment by consulting together.",
        "Find the items and information you need quickly and efficiently.",
        "Good staff and customer service."
    ]
}

# 3. INITIALIZE STATE ENGINE (Stores feedback in runtime memory)
if "survey_database" not in st.session_state:
    # Build historical template entries to populate charts beautifully on startup
    pre_populated_data = []
    np.random.seed(10)
    for dept_key, questions in DEPARTMENTAL_CRITERIA.items():
        for i in range(5):  # Inject 5 historical submission forms for each department
            random_scores = [np.random.randint(3, 6) for _ in questions]
            pre_populated_data.append({
                "Timestamp": f"2026-06-19 10:{15 + i}:00",
                "Department": dept_key,
                "Average Score": round(float(np.mean(random_scores)), 2),
                "Feedback Comments": "System generated verification audit trail."
            })
    st.session_state["survey_database"] = pre_populated_data

# 4. BRANDING HEADERS
st.title("🏭 HORIZON ADDIS TYRE")
st.subheader("Store Management Department — Internal Satisfaction System")
st.markdown("---")

# 5. SIDEBAR MODE CONTROLLER
st.sidebar.image("https://img.icons8.com/fluency/96/tire.png", width=55)
st.sidebar.header("Navigation Hub")
app_mode = st.sidebar.radio("Go To Area:", ["📋 Active Survey Form Entry", "📈 Real-Time Data Dashboard"])

# ======================================================================================
# MODE A: ACTIVE QUESTIONNAIRE FILLING ENGINE
# ======================================================================================
if app_mode == "📋 Active Survey Form Entry":
    st.markdown("### 📋 Store Performance Evaluation Form")
    st.info("Your evaluations directly optimize stockroom workflow, logistics accuracy, and delivery times. Please score objectively.")
    
    # Active Dynamic Dropdown Select
    target_dept = st.selectbox(
        "Select Your Submitting Department Context:",
        list(DEPARTMENTAL_CRITERIA.keys())
    )
    
    st.markdown(f"#### 🔍 Satisfaction Evaluation Questionnaire: **{target_dept} Department**")
    st.caption("Grading Scale Matrix: 1 = Strongly Disagree | 2 = Disagree | 3 = Neutral | 4 = Agree | 5 = Strongly Agree")
    
    # Render active criteria matching selection dynamically
    questions_list = DEPARTMENTAL_CRITERIA[target_dept]
    user_scores = []
    
    # Generating targeted radio selections per question
    with st.form(key="active_evaluation_form", clear_on_submit=True):
        for index, criterion in enumerate(questions_list):
            st.markdown(f"**Question {index + 1}:** {criterion}")
            score = st.select_slider(
                "Assign Rating Score:",
                options=[1, 2, 3, 4, 5],
                value=4,
                key=f"q_{target_dept}_{index}"
            )
            user_scores.append(score)
            st.markdown("<br>", unsafe_allowed_html=True)
            
        additional_comments = st.text_area("If you have additional validation points please specify here:")
        
        # Submission Handling
        submit_btn = st.form_submit_button("Submit Department Evaluation", width="content")
        if submit_btn:
            calc_avg = round(float(np.mean(user_scores)), 2)
            
            # Construct submission dataset payload record
            new_record = {
                "Timestamp": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Department": target_dept,
                "Average Score": calc_avg,
                "Feedback Comments": additional_comments if additional_comments else "None provided."
            }
            
            # Commit to Active Session Memory State
            st.session_state["survey_database"].append(new_record)
            st.success(f"🎉 Success! Feedback for '{target_dept}' computed with an Average Index of {calc_avg}/5.0 and securely filed.")
            st.balloons()

# ======================================================================================
# MODE B: DATA ANALYTICS HUB
# ======================================================================================
else:
    st.markdown("### 📈 Live Analytics & Evaluation Registry")
    
    # Parse running operational database cache 
    df_live = pd.DataFrame(st.session_state["survey_database"])
    
    # Filter selection logic
    st.markdown("#### Live Filters")
    dashboard_filter = st.selectbox(
        "Filter Dashboard View Scope:",
        ["All Departments"] + list(DEPARTMENTAL_CRITERIA.keys())
    )
    
    if dashboard_filter != "All Departments":
        df_display = df_live[df_live["Department"] == dashboard_filter]
    else:
        df_display = df_live

    # High-Value Card KPI Rows
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            label="Total Evaluation Records Captured", 
            value=str(len(df_display)), 
            delta="Live Dynamic Sink"
        )
    with col2:
        global_avg = round(df_display["Average Score"].mean(), 2) if not df_display.empty else 0.0
        st.metric(
            label="Aggregated Department Satisfaction Index", 
            value=f"{global_avg} / 5.0", 
            delta=None
        )
    with col3:
        highest_dept = df_live.groupby("Department")["Average Score"].mean().idxmax() if not df_live.empty else "N/A"
        st.metric(
            label="Top Performing Partner Relationship", 
            value=highest_dept, 
            delta="Highest Service Level"
        )
        
    st.markdown("---")
    
    # Graphical Visual Splits
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        if not df_live.empty:
            df_chart = df_live.groupby("Department")["Average Score"].mean().reset_index()
            fig_bar = px.bar(
                df_chart,
                x="Department",
                y="Average Score",
                title="Mean Satisfaction Matrix Across Plant Branches",
                labels={"Average Score": "Rating Score (Scale 1-5)"},
                color="Average Score",
                color_continuous_scale=px.colors.sequential.Tealgrn
            )
            fig_bar.update_layout(yaxis_range=[1, 5], margin=dict(l=15, r=15, t=35, b=15))
            # 2026 Conforming Parameter: width="stretch"
            st.plotly_chart(fig_bar, width="stretch", key="dash_bar_analytics")
        else:
            st.warning("Awaiting initial metrics logs.")
            
    with chart_col2:
        if not df_display.empty:
            fig_trend = px.scatter(
                df_display,
                x="Timestamp",
                y="Average Score",
                color="Department",
                title="Timeline Variance of Logged Department Submissions",
                size=[10] * len(df_display),
                hover_data=["Feedback Comments"]
            )
            fig_trend.update_layout(yaxis_range=[1, 5], margin=dict(l=15, r=15, t=35, b=15))
            st.plotly_chart(fig_trend, width="stretch", key="dash_trend_scatter")
            
    st.markdown("---")
    
    # 6. CENTRAL EXCEL/CSV INVENTORY DATAGRID
    st.markdown("#### 📋 Consolidated Historical Database Grid View")
    
    # Conforming Parameter: width="stretch" replaces the old warning-heavy parameter
    st.dataframe(
        df_display.sort_values(by="Timestamp", ascending=False),
        width="stretch",
        hide_index=True
    )
    
    # Export Module
    csv_stream = df_display.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Current Query Output View as CSV",
        data=csv_stream,
        file_name="horizon_addis_live_store_metrics.csv",
        mime="text/csv",
        width="content"
    )
