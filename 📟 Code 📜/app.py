import streamlit as st
from openai import OpenAI
import os

# ========== CONFIG ==========
st.set_page_config(page_title="AI Clinical Assistant", layout="wide")

# ========== API KEY ==========
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ========== TITLE ==========
st.title("🩺 AI Clinical Assistant")

# ========== SIDEBAR ==========
page = st.sidebar.radio("Choose Module", [
    "💬 Chat",
    "🧠 Diagnosis",
    "💊 Treatment",
    "💉 Drug Checker"
])

# ========== CHAT MODULE ==========
if page == "💬 Chat":
    st.header("💬 AI Doctor Chat")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    user_input = st.chat_input("Describe symptoms or case...")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=st.session_state.messages
        )

        reply = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": reply})

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])


# ========== DIAGNOSIS ==========
elif page == "🧠 Diagnosis":
    st.header("🧠 Diagnosis Assistant")

    age = st.number_input("Age", 0, 120)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    symptoms = st.text_area("Symptoms")

    if st.button("Analyze"):
        prompt = f"""
        You are a clinical assistant.

        Patient:
        Age: {age}
        Gender: {gender}
        Symptoms: {symptoms}

        Provide:
        1. Possible diagnoses
        2. Risk level
        3. Suggested tests
        4. Red flags
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        st.write(response.choices[0].message.content)


# ========== TREATMENT ==========
elif page == "💊 Treatment":
    st.header("💊 Treatment Planner")

    diagnosis = st.text_area("Diagnosis")

    if st.button("Generate Plan"):
        prompt = f"""
        You are a treatment planning assistant.

        Diagnosis: {diagnosis}

        Provide:
        - Treatment options
        - Medications
        - Lifestyle advice
        - When to see a doctor
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        st.write(response.choices[0].message.content)


# ========== DRUG CHECKER ==========
elif page == "💉 Drug Checker":
    st.header("💉 Drug Interaction Checker")

    drugs = st.text_area("Enter drugs (comma separated)")

    if st.button("Check"):
        prompt = f"""
        You are a pharmacology expert.

        Drugs: {drugs}

        Provide:
        - Interactions
        - Warnings
        - Safer alternatives
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        st.write(response.choices[0].message.content)


# ========== DISCLAIMER ==========
st.warning("⚠️ This tool is for educational purposes only. Not a real medical diagnosis.")