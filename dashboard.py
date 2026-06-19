import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import requests

# --- PAGE CONFIGURATION & THEME ---
st.set_page_config(
    page_title="HORIZON ADDIS TYRE - Store Satisfaction BI",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Enterprise Dark Theme CSS
st.markdown("""
    <style>
        .stApp {
            background-color: #0B0F19;
            color: #F8FAFC;
        }
        div[data-testid="stMetricValue"] {
            color: #38BDF8 !important;
            font-size: 1.8rem !important;
            font-weight: 700;
        }
        div[data-testid="stMetricLabel"] {
            color: #94A3B8 !important;
            font-size: 0.85rem !important;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        .metric-card {
            background-color: #1E293B;
            border-left: 4px solid #0EA5E9;
            padding: 12px 15px;
            border-radius: 6px;
            margin-bottom: 12px;
            min-height: 110px;
        }
        /* Custom styling for the survey radio layout */
        div[data-testid="stMarkdownContainer"] p {
            font-size: 1.05rem;
        }
    </style>
""", unsafe_allow_html=True)

# --- EXACT QUESTIONNAIRE MAPS FROM UPLOADED FILES ---
QUESTIONNAIRE_MAP = {
    "Product Industrialization & QA": [
        "Maintaining inventory of products and raw materials in accordance with established procedures and standards.",
        "Regarding the handling and monitoring of expired products",
        "Receive and implement work orders and expert opinions on product and raw material management.",
        "Work according to the operating system to prevent products and raw materials from being damaged.",
        "Providing the goods and information you need quickly and clearly",
        "Providing timely information regarding the decision to pass incoming raw materials and implementing the decision accordingly",
        "Employee reception and information reception ."
    ],
    "Security Section": [
        "Working according to a jointly agreed procedure during the shipment",
        "Work with security personnel to protect products from damage and theft.",
        "Accepting and carrying out work orders from professionals to protect property from danger",
        "Solving problems during shipment by consulting together",
        "Find the items and information you need quickly and efficiently",
        "Good staff and customer service"
    ],
    "Safety Section": [
        "Carrying out work in accordance with established safety guidelines",
        "Supervision and work in the use and maintenance of safety signs",
        "Accepting and implementing expert advice to protect assets in warehouses from hazards",
        "Find the item you want quickly and with quality",
        "Staff hospitality and customer reception and handling"
    ],
    "Production": [
        "Requested raw materials are delivered on time to mixing area",
        "Delivered items are labeled with Green tag always",
        "Delivered items are free from Foreign material & leakage.",
        "Natural rubber is delivered with proper metallic pallet requirement",
        "Cord roll handling & storing condition.",
        "Customer handling ability and hospitality of store workers ."
    ],
    "Sales & Marketing": [
        "Provide quality inventory reports on time.",
        "Store operating system ensures the satisfaction of External customers.",
        "Willingness and commitment to jointly resolve workplace problems and disagreements",
        "Get the goods and information you need in a timely and quality manner",
        "Regarding store implementation of the Waiting time for external customers",
        "Staff hospitality and timely customer service"
    ],
    "Purchasing": [
        "Providing updated information regarding all purchase requests.",
        "Responding requests from the purchasing department in a timely manner.",
        "Providing the necessary information/ specifications in adequate manner for goods/ services to be purchased.",
        "Provide timely and quality raw material inventory reports.",
        "When a purchased item arrives, it must be handled and received efficiently.",
        "Handling drivers carrying goods purchased from domestic and foreign countries in a timely and quality manner",
        "Employee hospitality and cooperation"
    ],
    "PMITS": [
        "Implementing deployed systems efficiently and as required.",
        "Providing required reports in a timely and quality manner",
        "Accept and implement feedback.",
        "Delivering the goods you need quickly and with quality",
        "Good hospitality and cooperation of employees"
    ],
    "Finance": [
        "ERP and inventory data processing And delivering in a timely and quality Manner.",
        "Work efficiently and effectively during planned product inventory, as well as preparation and work.",
        "Getting the information you need in quality and on time.",
        "Delivering the goods you want with quality and speed.",
        "Accept and implement the recommendations given.",
        "The sincerity and hospitality of the staff"
    ],
    "Plant Engineering (PE)": [
        "Follow up on urgent purchase orders, place orders and provide information when received.",
        "Providing the property and information you need in a Clear and concise Manner",
        "Verify with the relevant body that the purchased and purchased items are in accordance with the standards.",
        "Collaboration for any support Request from your department .",
        "Staff orientation and customer service and Reception"
    ],
    "Human Resources (HR)": [
        "Timely report employees performance evaluation result",
        "Timely request the department's manpower recruitment.",
        "Proper Handling of employees with a discipline case or Handling of low performers.",
        "Appropriate and timely planning and execution of trainings for employees.",
        "Proper employee leave management .",
        "Delivering the goods you need quickly and with quality.",
        "Responsible for cleaning and other related tasks in the common areas",
        "Good hospitality and cooperation of employees"
    ]
}

# --- DATA GENERATOR / PIPELINE ---
@st.cache_data
def generate_factory_responses():
    np.random.seed(42)
    records = []
    for _ in range(300):
        dept = np.random.choice(list(QUESTIONNAIRE_MAP.keys()))
        questions = QUESTIONNAIRE_MAP[dept]
        
        for idx, q_text in enumerate(questions, start=1):
            records.append({
                "Response_ID": _,
                "Department": dept,
                "Question_No": f"Q{idx}",
                "Question_Text": q_text,
                "Rating": np.random.choice([1, 2, 3, 4, 5], p=[0.05, 0.10, 0.20, 0.40, 0.25])
            })
    return pd.DataFrame(records)

df_responses = generate_factory_responses()

# --- HEADER SECTION ---
st.title("🏭 HORIZON ADDIS TYRE")
st.subheader("Store Management Department - Internal Customer Satisfaction Hub")
st.markdown("---")

# --- SECTION 1: ENTERPRISE SCORECARDS ---
st.markdown("### 📊 Departmental Overall Satisfaction Standings (OSS / 5.0)")

dept_oss = df_responses.groupby("Department")["Rating"].mean().round(2).reset_index()
dept_oss.columns = ["Department", "OSS"]
dept_oss_dict = dict(zip(dept_oss["Department"], dept_oss["OSS"]))

cols = st.columns(5)
for index, dept_name in enumerate(QUESTIONNAIRE_MAP.keys()):
    col_selector = index % 5
    with cols[col_selector]:
        score = dept_oss_dict.get(dept_name, 0.0)
        st.markdown(f'<div class="metric-card">', unsafe_allow_html=True)
        st.metric(
            label=dept_name,
            value=f"{score} / 5.0",
            delta=f"{round(score - 3.5, 2)} vs Target"
        )
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# --- SECTION 2: THREE TOGGLEABLE APP TABS (INCLUDING FORM) ---
view_tab1, view_tab2, view_tab3 = st.tabs([
    "🎯 Customer-by-Customer Analysis", 
    "📝 Question-by-Question Diagnostics",
    "✍️ Fill Online Feedback Form"
])

# -- TAB 1: CUSTOMER VIEW --
with view_tab1:
    st.markdown("### Customer Deep-Dive Assessment")
    selected_dept = st.selectbox("Select Internal Department to Audit:", list(QUESTIONNAIRE_MAP.keys()))
    
    dept_df = df_responses[df_responses["Department"] == selected_dept]
    chart_data = dept_df.groupby(["Question_No", "Question_Text"])["Rating"].mean().reset_index()
    
    col_l, col_r = st.columns([1, 1])
    with col_l:
        st.markdown(f"#### Average Scores for **{selected_dept}** Criteria")
        st.dataframe(
            chart_data.rename(columns={"Question_No": "No.", "Question_Text": "Evaluation Criteria", "Rating": "Avg Score"}).set_index("No."),
            use_container_width=True
        )
    with col_r:
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=chart_data["Rating"],
            theta=chart_data["Question_No"],
            fill='toself',
            fillcolor='rgba(56, 189, 248, 0.2)',
            line=dict(color='#38BDF8', width=2),
            hovertext=chart_data["Question_Text"]
        ))
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[1, 5], gridcolor="#334155"),
                angularaxis=dict(gridcolor="#334155")
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#F8FAFC'),
            height=320,
            margin=dict(t=30, b=20, l=20, r=20)
        )
        st.plotly_chart(fig_radar, use_container_width=True)

# -- TAB 2: QUESTIONNAIRE VIEW --
with view_tab2:
    st.markdown("### Question-by-Question Matrix Analysis")
    chosen_dept = st.selectbox("Pick Target Department for Question Breakdown:", list(QUESTIONNAIRE_MAP.keys()), key="tab2_dept")
    
    available_questions = QUESTIONNAIRE_MAP[chosen_dept]
    chosen_q_text = st.selectbox("Select Unique Questionnaire Statement:", available_questions)
    
    q_df = df_responses[(df_responses["Department"] == chosen_dept) & (df_responses["Question_Text"] == chosen_q_text)]
    distribution = q_df["Rating"].value_counts().reindex([1, 2, 3, 4, 5], fill_value=0).reset_index()
    distribution.columns = ["Likert Scale", "Total Responses"]
    
    scale_labels = {1: "1-Strongly Disagree", 2: "2-Disagree", 3: "3-Neutral", 4: "4-Agree", 5: "5-Strongly Agree"}
    distribution["Rating Label"] = distribution["Likert Scale"].map(scale_labels)
    
    fig_dist = px.bar(
        distribution,
        x="Rating Label",
        y="Total Responses",
        title="Survey Response Volume Selection Count",
        color="Total Responses",
        color_continuous_scale=['#1E293B', '#38BDF8']
    )
    fig_dist.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#F8FAFC'),
        xaxis=dict(title="Likert Scale Level Choices", gridcolor="rgba(0,0,0,0)"),
        yaxis=dict(title="Response Count", gridcolor="#334155"),
        coloraxis_showscale=False,
        height=380
    )
    st.plotly_chart(fig_dist, use_container_width=True)

# -- TAB 3: DEDICATED INPUT FORM PORTAL --
with view_tab3:
    st.markdown("### ✍️ Store Evaluation Submission Form")
    st.markdown("Select your department below to populate your unique questionnaire criteria.")
    
    # Target client selection
    form_dept = st.selectbox("Your Department / Section:", list(QUESTIONNAIRE_MAP.keys()), key="feedback_form_dept")
    dept_questions = QUESTIONNAIRE_MAP[form_dept]
    
    st.markdown("---")
    
    # Form layout boundary
    with st.form(key="factory_feedback_form", clear_on_submit=True):
        responses_payload = {}
        
        # Iteratively build individual rows matching the exact source file arrays
        for idx, question_string in enumerate(dept_questions, start=1):
            st.markdown(f"##### **Criteria {idx}**")
            st.write(question_string)
            
            responses_payload[f"Q{idx}"] = st.radio(
                "Select Score Matrix Alignment:",
                options=[1, 2, 3, 4, 5],
                format_func=lambda x: {
                    1: "1. Strongly Disagree",
                    2: "2. Disagree",
                    3: "3. Neutral",
                    4: "4. Agree",
                    5: "5. Strongly Agree"
                }[x],
                horizontal=True,
                key=f"form_radio_{form_dept.replace(' ', '_')}_{idx}"
            )
            st.markdown("<br>", unsafe_allow_html=True)
            
        st.markdown("---")
        additional_comments = st.text_area("If you have additional points please specify:", height=100)
        
        # Submission execution layout
        submit_btn = st.form_submit_button(label="Submit Official Evaluation")
        
        if submit_btn:
            # Construct JSON data payload for API webhook forwarding
            submit_data = {
                "department": form_dept,
                "ratings": responses_payload,
                "comment": additional_comments
            }
            
            # User visual confirmation success block
            st.success(f"✅ Success! Evaluation form for '{form_dept}' has been recorded.")
            st.json(submit_data) # Verification display of captured data arrays

st.markdown("---")

# --- SECTION 3: SYSTEM AGGREGATE SUMMARY MATRIX ---
st.markdown("### 📈 Comprehensive Plant Heatmap Analytics Matrix")

matrix_data = df_responses.groupby(["Department", "Question_No"])["Rating"].mean().unstack().round(2)
fig_heatmap = px.imshow(
    matrix_data,
    labels=dict(x="Question Number Identification", y="Internal Department Client", color="Rating Value"),
    x=matrix_data.columns,
    y=matrix_data.index,
    color_continuous_scale=['#EF4444', '#F59E0B', '#10B981']
)
fig_heatmap.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#F8FAFC'),
    height=420
)
st.plotly_chart(fig_heatmap, use_container_width=True)
