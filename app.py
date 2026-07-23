import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="Cotiviti Clinical Intelligence Platform",
    page_icon="🏥",
    layout="wide"
)

st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #06111f 0%, #0b1220 100%);
}
[data-testid="stSidebar"] {
    background-color: #050b14;
}
.main-title {
    font-size: 42px;
    font-weight: 800;
    color: #f8fafc;
}
.subtitle {
    color: #94a3b8;
    font-size: 17px;
}
.metric-card {
    background: #0f172a;
    padding: 22px;
    border-radius: 16px;
    border: 1px solid #334155;
    min-height: 160px;
}
.red { border-color: #ef4444; }
.blue { border-color: #3b82f6; }
.orange { border-color: #f59e0b; }
.green { border-color: #10b981; }
.purple { border-color: #8b5cf6; }

.card-title {
    color: #cbd5e1;
    font-size: 13px;
    font-weight: 700;
    text-transform: uppercase;
}
.card-value {
    font-size: 32px;
    font-weight: 800;
    color: white;
    margin-top: 14px;
}
.badge {
    display: inline-block;
    margin-top: 14px;
    padding: 6px 12px;
    border-radius: 8px;
    font-weight: 700;
    font-size: 13px;
}
.badge-red { background: #450a0a; color: #fecaca; border: 1px solid #ef4444; }
.badge-blue { background: #082f49; color: #bfdbfe; border: 1px solid #3b82f6; }
.badge-orange { background: #451a03; color: #fde68a; border: 1px solid #f59e0b; }
.badge-green { background: #052e16; color: #bbf7d0; border: 1px solid #10b981; }
.badge-purple { background: #2e1065; color: #ddd6fe; border: 1px solid #8b5cf6; }

.panel {
    background: #0f172a;
    padding: 22px;
    border-radius: 16px;
    border: 1px solid #334155;
    margin-top: 18px;
}
.summary {
    background: #0b1b33;
    padding: 20px;
    border-radius: 16px;
    border: 1px solid #3b82f6;
    margin-top: 20px;
}
.footer {
    text-align: center;
    color: #94a3b8;
    font-size: 13px;
    padding: 25px;
}
</style>
""", unsafe_allow_html=True)

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("## ✚ COTIVITI")
    st.caption("Clinical Intelligence Platform")

    st.divider()

    language = st.selectbox(
        "🌍 Patient Preferred Language",
        ["English", "Spanish", "French", "Arabic", "Amharic", "Tigrinya", "Chinese", "Vietnamese"]
    )

    st.divider()

    st.markdown("### Modules")
    st.write("✅ Clinical Risk")
    st.write("✅ Payment Integrity")
    st.write("✅ Documentation Review")
    st.write("✅ Operations Support")
    st.write("✅ Exportable Report")

    st.divider()

    st.info("Educational demo only. Not a substitute for clinical judgment.")

# ---------- Header ----------
st.markdown('<div class="main-title">🏥 Cotiviti Clinical Intelligence Platform</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Clinical risk scoring, payment integrity, documentation review, and operations support.</div>',
    unsafe_allow_html=True
)

st.warning("Educational proof of concept only. This tool does not provide medical advice.")

st.divider()

# ---------- Inputs ----------
st.header("Patient Case Input")

col1, col2, col3 = st.columns(3)

with col1:
    age = st.number_input("Age", 0, 120, 67)
    sex = st.selectbox("Sex", ["Female", "Male", "Other / Not specified"])

with col2:
    oxygen = st.slider("Oxygen Saturation (%)", 70, 100, 91)
    heart_rate = st.number_input("Heart Rate", 30, 220, 112)

with col3:
    temperature = st.number_input("Temperature (°F)", 90.0, 110.0, 101.2)
    visit_type = st.selectbox("Visit Type", ["Emergency", "Inpatient", "Outpatient"])

symptoms = st.text_area("Symptoms", value="Fever, cough, shortness of breath, fatigue")
history = st.text_area("Medical History", value="Hypertension and type 2 diabetes")
labs = st.text_area("Lab Results / Notes", value="Low oxygen saturation. Elevated white blood cell count.")

# ---------- Logic ----------
def calculate_risk(age, oxygen, heart_rate, temperature, symptoms):
    score = 0
    reasons = []

    if age >= 65:
        score += 15
        reasons.append("Age over 65 increased the risk score.")
    if oxygen < 92:
        score += 35
        reasons.append("Oxygen saturation below 92% is a major risk factor.")
    elif oxygen < 95:
        score += 20
        reasons.append("Oxygen saturation below 95% needs review.")
    if heart_rate > 110:
        score += 15
        reasons.append("Heart rate above 110 may show clinical stress.")
    if temperature >= 100.4:
        score += 20
        reasons.append("Fever may suggest infection or inflammation.")
    if symptoms.strip():
        score += 15
        reasons.append("Symptoms were documented and support clinical review.")

    score = min(score, 100)

    if score >= 70:
        return score, "High Risk", "Immediate Review", reasons
    elif score >= 40:
        return score, "Moderate Risk", "Clinician Review", reasons
    else:
        return score, "Low Risk", "Routine Review", reasons


def documentation_score(symptoms, history, labs):
    score = 40
    if symptoms.strip():
        score += 20
    if history.strip():
        score += 20
    if labs.strip():
        score += 20
    return min(score, 100)


def confidence_score(symptoms, history, labs):
    score = 60
    if symptoms.strip():
        score += 15
    if history.strip():
        score += 10
    if labs.strip():
        score += 15
    return min(score, 100)


def icd_suggestions(symptoms):
    text = symptoms.lower()
    codes = []

    if "cough" in text:
        codes.append("R05.9 — Cough, unspecified")
    if "shortness" in text or "breath" in text:
        codes.append("R06.02 — Shortness of breath")
    if "fever" in text:
        codes.append("R50.9 — Fever, unspecified")
    if "fatigue" in text:
        codes.append("R53.83 — Other fatigue")

    if not codes:
        codes.append("No symptom-based ICD-10 categories suggested.")

    return codes


def build_report(case_id, risk_score, level, priority, doc_score, confidence, language):
    return f"""
Cotiviti Clinical Intelligence Platform
Case Report

Case ID: {case_id}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Preferred Language: {language}

Risk Score: {risk_score}/100
Risk Level: {level}
Priority: {priority}
Documentation Quality: {doc_score}%
Clinical Confidence: {confidence}%

Summary:
This case was reviewed using a transparent rule-based clinical intelligence prototype.
The tool supports treatment, payment, and operations workflows.

Disclaimer:
This is an educational proof of concept and does not provide medical advice.
"""

# ---------- Results ----------
if st.button("Analyze Patient Case", use_container_width=True):
    case_id = "CTVT-" + datetime.now().strftime("%Y%m%d-%H%M%S")

    risk_score, level, priority, reasons = calculate_risk(
        age, oxygen, heart_rate, temperature, symptoms
    )
    doc_score = documentation_score(symptoms, history, labs)
    confidence = confidence_score(symptoms, history, labs)

    st.divider()

    top1, top2 = st.columns([3, 1])
    with top1:
        st.markdown('<div class="main-title">Clinical Intelligence Results</div>', unsafe_allow_html=True)
        st.markdown('<div class="subtitle">AI-style clinical analysis and decision support.</div>', unsafe_allow_html=True)
    with top2:
        st.download_button(
            "⬇ Export Report",
            data=build_report(case_id, risk_score, level, priority, doc_score, confidence, language),
            file_name=f"{case_id}_clinical_report.txt",
            mime="text/plain",
            use_container_width=True
        )

    st.write("")

    m1, m2, m3, m4, m5 = st.columns(5)

    with m1:
        st.markdown(f"""
        <div class="metric-card red">
            <div class="card-title">Risk Score</div>
            <div class="card-value">{risk_score}/100</div>
            <span class="badge badge-red">▲ {level.upper()}</span>
        </div>
        """, unsafe_allow_html=True)

    with m2:
        st.markdown(f"""
        <div class="metric-card blue">
            <div class="card-title">Risk Level</div>
            <div class="card-value">{level}</div>
            <span class="badge badge-blue">Critical</span>
        </div>
        """, unsafe_allow_html=True)

    with m3:
        st.markdown(f"""
        <div class="metric-card orange">
            <div class="card-title">Priority</div>
            <div class="card-value">{priority}</div>
            <span class="badge badge-orange">Urgent</span>
        </div>
        """, unsafe_allow_html=True)

    with m4:
        st.markdown(f"""
        <div class="metric-card green">
            <div class="card-title">Documentation</div>
            <div class="card-value">{doc_score}%</div>
            <span class="badge badge-green">Excellent</span>
        </div>
        """, unsafe_allow_html=True)

    with m5:
        st.markdown(f"""
        <div class="metric-card purple">
            <div class="card-title">Confidence</div>
            <div class="card-value">{confidence}%</div>
            <span class="badge badge-purple">High</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="summary">
        <h3>📋 Executive Summary</h3>
        This case is categorized as <b>{level}</b> and should receive
        <b>{priority}</b>. Patient preferred language is <b>{language}</b>.
        This dashboard supports clinical review, payment integrity, and operational prioritization.
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="panel"><h3>👤 Patient Summary</h3>', unsafe_allow_html=True)

    p1, p2, p3, p4, p5, p6 = st.columns(6)
    p1.metric("Gender", sex)
    p2.metric("Age", f"{age} years")
    p3.metric("Visit Type", visit_type)
    p4.metric("Oxygen", f"{oxygen}%")
    p5.metric("Heart Rate", f"{heart_rate} bpm")
    p6.metric("Temperature", f"{temperature}°F")

    st.markdown("</div>", unsafe_allow_html=True)

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🧠 Clinical Reasoning",
        "💰 Payment Integrity",
        "📋 Documentation",
        "⚙️ Operations",
        "🏷 ICD-10 Suggestions",
        "⬇ Export"
    ])

    with tab1:
        st.markdown('<div class="panel"><h2>🧠 Clinical Reasoning</h2>', unsafe_allow_html=True)

        st.error(
            f"{level} pattern detected. This does not diagnose the patient, "
            "but it organizes the case for clinical review."
        )

        st.subheader("Risk Score Explanation")
        for reason in reasons:
            st.write(f"✅ {reason}")

        st.markdown("</div>", unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="panel"><h2>💰 Payment Integrity Review</h2>', unsafe_allow_html=True)
        st.write(
            "Documentation should support medical necessity, selected level of care, "
            "abnormal vital signs, clinical decision-making, and billed services."
        )
        st.write("The review should confirm that the services match the documented clinical picture.")
        st.markdown("</div>", unsafe_allow_html=True)

    with tab3:
        st.markdown('<div class="panel"><h2>📋 Documentation Review</h2>', unsafe_allow_html=True)
        st.metric("Documentation Completeness", f"{doc_score}%")
        st.progress(doc_score / 100)
        st.write("Recommended documentation items:")
        st.write("✅ Symptom onset and duration")
        st.write("✅ Current medications")
        st.write("✅ Allergy history")
        st.write("✅ Abnormal vital sign trends")
        st.write("✅ Medical necessity for tests or treatment")
        st.markdown("</div>", unsafe_allow_html=True)

    with tab4:
        st.markdown('<div class="panel"><h2>⚙️ Operations Recommendation</h2>', unsafe_allow_html=True)
        if level == "High Risk":
            st.write("**Suggested Department:** Emergency / Clinical Review Team")
            st.write("**Queue Priority:** Urgent")
            st.write("**Action:** Route immediately for clinician review.")
        elif level == "Moderate Risk":
            st.write("**Suggested Department:** Clinical Review / Care Management")
            st.write("**Queue Priority:** Standard Review")
            st.write("**Action:** Review documentation and follow-up needs.")
        else:
            st.write("**Suggested Department:** Routine Review")
            st.write("**Queue Priority:** Normal")
            st.write("**Action:** Process through standard workflow.")
        st.markdown("</div>", unsafe_allow_html=True)

    with tab5:
        st.markdown('<div class="panel"><h2>🏷 Educational ICD-10 Suggestions</h2>', unsafe_allow_html=True)
        st.caption("Educational only. Final coding decisions require qualified coding review.")
        for code in icd_suggestions(symptoms):
            st.write(f"✅ {code}")
        st.markdown("</div>", unsafe_allow_html=True)

    with tab6:
        st.markdown('<div class="panel"><h2>⬇ Export Case Report</h2>', unsafe_allow_html=True)
        st.download_button(
            "Download Case Report",
            data=build_report(case_id, risk_score, level, priority, doc_score, confidence, language),
            file_name=f"{case_id}_report.txt",
            mime="text/plain",
            use_container_width=True
        )
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="footer">
        Cotiviti Clinical Intelligence Platform<br>
        Internship Proof of Concept • Developed by Misgana Okbagaber • University of Washington<br>
        Python • Streamlit
    </div>
    """, unsafe_allow_html=True)