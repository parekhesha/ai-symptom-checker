import streamlit as st
from checker import analyze_symptoms

st.set_page_config(
    page_title="AI Symptom Checker",
    page_icon="🏥",
    layout="centered"
)

st.title("🏥 AI Symptom Checker")
st.warning("This tool is for informational purposes only. Always consult a doctor.")

st.subheader("Patient Information")
col1, col2 = st.columns(2)
with col1:
    age = st.number_input("Age", min_value=1, max_value=120, value=25)
with col2:
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])

st.subheader("Enter Your Symptoms")
symptom_input = st.text_area(
    "Describe your symptoms (comma-separated)",
    placeholder="e.g., fever, headache, fatigue"
)

duration = st.selectbox(
    "How long have you had these symptoms?",
    ["Less than 24 hours", "1-3 days", "4-7 days", "More than a week"]
)

if st.button("🔍 Analyze Symptoms", type="primary"):
    if symptom_input.strip():
        symptoms_list = [s.strip() for s in symptom_input.split(",")]
        with st.spinner("Analyzing your symptoms..."):
            result = analyze_symptoms(symptoms_list, age, gender)
        st.subheader("📋 Analysis Results")
        if result.get("severity") == "EMERGENCY":
            st.error(result["message"])
            st.error(result["advice"])
        else:
            st.success("Analysis Complete")
            st.markdown(result["analysis"])
            st.info(result["disclaimer"])
    else:
        st.error("Please enter at least one symptom.")