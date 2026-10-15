import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="neuro-redflag-triage", layout="wide")

st.title("neuro-redflag-triage: emergency headache & intracranial risk engine")
st.caption("evidence-based triage decision support based on snoop10 criteria and the ottawa subarachnoid hemorrhage rule")

tab1, tab2 = st.tabs([
    "module 1: acute secondary red-flag triage",
    "module 2: false-negative ct & vascular pathway"
])

with tab1:
    st.subheader("clinical presentation & symptom scoring")
    st.write("evaluates the probability of secondary neurovascular emergencies vs primary benign headaches.")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### patient demographics")
        age = st.number_input("patient age (years)", min_value=1, max_value=110, value=58)
        new_onset_elderly = age >= 50
        history_cancer = st.checkbox("history of active malignancy / cancer")
        immunocompromised = st.checkbox("immunocompromised state (hiv, chemo, steroids)")
        
    with col2:
        st.markdown("#### onset & characteristics")
        onset_time = st.selectbox(
            "time to peak pain intensity",
            ["instant / < 1 minute (thunderclap)", "1 to 5 minutes", "gradual (> 5 minutes)"]
        )
        neck_stiffness = st.checkbox("neck stiffness / meningismus")
        pain_with_eye = st.checkbox("pain worsening with eye movement")
        jaw_claudication = st.checkbox("jaw claudication (pain in jaw while chewing)")
        scalp_tenderness = st.checkbox("scalp tenderness (pain when combing or on pillow)")
        
    with col3:
        st.markdown("#### vital signs & triggers")
        temp = st.number_input("body temperature (°f)", min_value=95.0, max_value=106.0, value=100.8, step=0.1)
        sbp = st.number_input("systolic blood pressure (mmhg)", min_value=60, max_value=250, value=140)
        postural_aggravation = st.checkbox("worse with coughing, bending, or valsalva")
        wakes_from_sleep = st.checkbox("headache wakes patient from sound sleep")
        preceding_vomiting = st.checkbox("unexplained vomiting preceding headache by weeks")

    red_flags = []
    triage_score = 0
    
    if "instant" in onset_time or "1 to 5" in onset_time:
        red_flags.append("thunderclap onset: hyperacute peak under 5 minutes")
        triage_score += 40
        
    if (temp >= 100.4 or neck_stiffness) and (pain_with_eye or neck_stiffness):
        red_flags.append("meningeal irritation complex: fever / nuchal rigidity")
        triage_score += 35
        
    if new_onset_elderly and (jaw_claudication or scalp_tenderness):
        red_flags.append("giant cell / temporal arteritis pattern: age >= 50 with craniofacial ischemia")
        triage_score += 35
        
    if history_cancer:
        red_flags.append("oncologic risk: rule out intracranial metastases / leptomeningeal disease")
        triage_score += 25
        
    if postural_aggravation or wakes_from_sleep or preceding_vomiting:
        red_flags.append("elevated intracranial pressure / posterior fossa mass pattern")
        triage_score += 20
        
    prob_percentage = min(100, triage_score)
    
    st.divider()
    m1, m2, m3 = st.columns(3)
    m1.metric("risk score", f"{triage_score}/100")
    m2.metric("urgency category", "high priority red flag" if triage_score >= 35 else "low / standard triage")
    m3.metric("secondary pathology probability", f"{prob_percentage}%")
    
    if triage_score >= 35:
        st.error(f"critical secondary headache suspected. identified triggers:\n\n- " + "\n- ".join(red_flags))
    else:
        st.success("low immediate red-flag burden. findings more consistent with primary headache disorder (migraine / tension).")

with tab2:
    st.subheader("emergency subarachnoid hemorrhage & diagnostic safety check")
    st.write("prevents fatal premature discharge from false-negative non-contrast ct scans.")
    
    c_a, c_b = st.columns(2)
    with c_a:
        st.markdown("#### diagnostic pathway status")
        hours_since_onset = st.slider("hours elapsed since headache onset", min_value=1, max_value=72, value=8)
        ct_performed = st.checkbox("non-contrast head ct scan completed", value=True)
        ct_result = st.radio("head ct interpretation", ["negative / normal", "positive (blood visible)"])
        
    with c_b:
        st.markdown("#### high-risk clinical context")
        st.write("- hyperacute peak reached under 5 minutes")
        st.write("- acute severe pain with neck stiffness without fever")
        st.write("- clinical concern for aneurysm rupture / arteriovenous malformation")
        
    st.divider()
    
    if ct_performed and ct_result == "positive (blood visible)":
        st.error("subarachnoid hemorrhage confirmed on neuroimaging. urgent neurosurgical consultation and angiography required.")
    elif ct_performed and ct_result == "negative / normal":
        if hours_since_onset > 6:
            st.warning(
                f"safety warning: head ct was performed {hours_since_onset} hours post-onset. "
                "sensitivity of non-contrast ct declines sharply after 6 hours, dropping below 90% as time elapses. "
                "a normal ct does not exclude small volume or infra-tentorial subarachnoid hemorrhage. "
                "mandatory action: diagnostic lumbar puncture indicated to analyze csf for opening pressure, red cell clearance, and spectrophotometric xanthochromia."
            )
        else:
            st.info(
                "head ct within 6 hours has high sensitivity (>99% with modern 3rd gen scanners), "
                "but persistent clinical suspicion or traumatic tap still warrants consideration of lumbar puncture or cta."
            )
    else:
        st.warning("imaging pending: emergency non-contrast head ct is the first-line mandatory investigation.")

    time_pts = np.linspace(1, 48, 100)
    ct_sensitivity = np.where(time_pts <= 6, 99.0, 99.0 * np.exp(-0.015 * (time_pts - 6)))
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=time_pts, y=ct_sensitivity,
        mode="lines",
        line=dict(color="#D32F2F", width=3),
        name="head ct sensitivity %"
    ))
    fig.add_vline(x=6, line_dash="dash", line_color="#0288D1", annotation_text="6-hour cutoff")
    fig.update_layout(
        title="decay of non-contrast head ct sensitivity over time in subarachnoid hemorrhage",
        xaxis_title="hours from headache onset",
        yaxis_title="diagnostic sensitivity (%)",
        height=380
    )
    st.plotly_chart(fig, use_container_width=True)