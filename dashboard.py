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

# 2. COMPLETE EVALUATION QUESTIONS DIRECTLY LOADED FROM YOUR INTERNAL CODES
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

# 3. ROBUST SESSION STATE INIT (Prevents components from wiping values on selection changes)
if "survey_db" not in st.session_state:
    historical_logs = []
    np.random.seed(24)
    # Generate initial fallback dataset for real-time graphs representation
    for index, (d_name, q_list) in enumerate(DEPARTMENTAL_CRITERIA.items()):
        for r_id in range(3):
            scores = [np.random.randint(3, 6) for _ in q_list]
            historical_logs.append({
                "Timestamp": f"2026-06-19 09:{10 * r_id}:00",
                "Department": d_name,
                "Average Score": round(float(np.mean(scores)), 2),
                "Feedback Comments": "Initial plant pre-load audit log check."
            })
    st.session_state["survey_db"] = historical_logs

# 4. BRANDING TOP VIEW
st.title("🏭 HORIZON ADDIS TYRE")
st.subheader("Store Management Department — Internal Customer Evaluation System")
st.markdown("---")

# 5. NAVIGATION LAYOUT (SPLIT INTO TABS TO AVOID SELECTION SHIFT BUGS)
form_tab, dashboard_tab = st.tabs(["📋 Fill Department Evaluation", "📈 Live Performance Dashboard"])

# ==========================================
# TAB 1: FORM RENDERING ENGINE & DROPDOWN HANDLING
# ==========================================
with form_tab:
    st.markdown("### 📋 Active Evaluation Form Entry")
    st.caption("Please pick your department branch, evaluate the operational targets, and press submit.")
    
    # Active safe selector
    target_dept = st.selectbox(
        "Select Your Submitting Department:",
        options=list(DEPARTMENTAL_CRITERIA.keys()),
        key="form_dept_selector"
    )
    
    st.markdown(f"**Current Section Metric Sheet:** `{target_dept} Department Questionnaire`")
    st.markdown("---")
    
    # Render criteria inputs
    questions = DEPARTMENTAL_CRITERIA[target_dept]
    form_scores = []
    
    # Form containment block ensuring all answers are passed reliably upon interaction
    with st.form(key=f"survey_form_{target_dept}", clear_on_submit=True):
        for idx, text in enumerate(questions):
            st.markdown(f"**Q{idx+1}:** {text}")
            val = st.radio(
                "Assign Rating Score:",
                options=[1, 2, 3, 4, 5],
                index=3, # Default selection is '4' (Agree)
                horizontal=True,
                key=f"score_input_{target_dept}_{idx}"
            )
            form_scores.append(val)
            st.markdown("<hr style='border:1px gray dotted;'>", unsafe_allowed_html=True)
            
        text_remarks = st.text_area("Provide additional remarks or suggestions:", key=f"notes_{target_dept}")
        
        # Action execution button
        submit_form = st.form_submit_button("Submit Evaluation Entry", width="content")
        
        if submit_form:
            final_mean = round(float(np.mean(form_scores)), 2)
            payload = {
                "Timestamp": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Department": target_dept,
                "Average Score": final_mean,
                "Feedback Comments": text_remarks if text_remarks else "No remarks filed."
            }
            # Append log directly into running memory
            st.session_state["survey_db"].append(payload)
            st.success(f"🎉 Filed successfully! Average Score evaluated: {final_mean} / 5.0")
            st.balloons()
            
            # Instantly rerun context to prompt calculations to display in Tab 2
            st.rerun()

# ==========================================
# TAB 2: LIVE PERFORMANCE ANALYTICS & REGISTRY
# ==========================================
with dashboard_tab:
    st.markdown("### 📈 Live Analytics Reporting Engine")
    
    # Read session dataset safely
    df_current = pd.DataFrame(st.session_state["survey_db"])
    
    # Dropdown to isolate specific analytics branches
    filter_dept = st.selectbox(
        "Isolate Dashboard View Scope:",
        options=["All Departments"] + list(DEPARTMENTAL_CRITERIA.keys()),
        key="dashboard_dept_selector"
    )
    
    # Filter matrix evaluation mapping
    if filter_dept != "All Departments":
        df_view = df_current[df_current["Department"] == filter_dept]
    else:
        df_view = df_current

    # Key Indicator Widgets
    m_col1, m_col2, m_col3 = st.columns(3)
    with m_col1:
        st.metric("Total Evaluation Surveys Processed", value=len(df_view), delta="Live Feed")
    with m_col2:
        global_index = round(df_view["Average Score"].mean(), 2) if not df_view.empty else 0.0
        st.metric("Mean Satisfaction Index Score", value=f"{global_index} / 5.0")
    with m_col3:
        top_unit = df_current.groupby("Department")["Average Score"].mean().idxmax() if not df_current.empty else "None"
        st.metric("Highest Rating Partner Section", value=top_unit)
        
    st.markdown("---")
    
    # Data visualization splits
    fig_col1, fig_col2 = st.columns(2)
    
    with fig_col1:
        if not df_current.empty:
            df_grp = df_current.groupby("Department")["Average Score"].mean().reset_index()
            fig_bar = px.bar(
                df_grp,
                x="Department",
                y="Average Score",
                title="Aggregated Satisfaction Rating Matrix",
                color="Average Score",
                color_continuous_scale=px.colors.sequential.Darkmint
            )
            fig_bar.update_layout(yaxis_range=[1,5], margin=dict(l=10, r=10, t=35, b=10))
            st.plotly_chart(fig_bar, width="stretch", key="live_metrics_bar_chart")
        else:
            st.info("No visualization metrics data loaded yet.")
            
    with fig_col2:
        if not df_view.empty:
            fig_scat = px.scatter(
                df_view,
                x="Timestamp",
                y="Average Score",
                color="Department",
                title="Timeline Spread of Submissions",
                hover_data=["Feedback Comments"]
            )
            fig_scat.update_layout(yaxis_range=[1,5], margin=dict(l=10, r=10, t=35, b=10))
            st.plotly_chart(fig_scat, width="stretch", key="live_timeline_chart")
            
    st.markdown("---")
    
    # Main log datagrid overview
    st.markdown("#### Detailed Records Registry View")
    st.dataframe(
        df_view.sort_values(by="Timestamp", ascending=False),
        width="stretch",
        hide_index=True
    )
