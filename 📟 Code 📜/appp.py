import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv

# ========== LOAD ENV ==========
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

# ========== CONFIG ==========
st.set_page_config(page_title="🩺 AI Clinical Assistant 🤖", layout="wide")

# ========== CHECK API KEY ==========
if not api_key:
    st.error("🚨 GROQ_API_KEY not found. Please check your .env file.")
    st.stop()

client = Groq(api_key=api_key)

# ========== MODEL ==========
MODEL = "llama-3.3-70b-versatile"  # Updated Groq model

# ========== TITLE ==========
st.title("🩺 AI Clinical Assistant 🤖")

# ========== SIDEBAR ==========
page = st.sidebar.radio("✅ Choose Module", [
    "💬 Chat",
    "🧠 Diagnosis",
    "💊 Treatment",
    "💉 Drug Checker"
])

# ========== HELPER FUNCTION ==========
def get_ai_response(prompt=None, messages=None):
    try:
        if messages:
            response = client.chat.completions.create(
                model=MODEL,
                messages=messages
            )
        else:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[{"role": "user", "content": prompt}]
            )

        return response.choices[0].message.content

    except Exception as e:
        return f"❌ Error ☠️ : {str(e)}"


# ========== CHAT MODULE ==========
if page == "💬 Chat":
    st.header("AI 🤖 Doctor Chat 💬")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    user_input = st.chat_input("Describe 📝 symptoms or case...")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.spinner("AI 🤖 is typing..."):
            reply = get_ai_response(messages=st.session_state.messages)
        st.session_state.messages.append({"role": "assistant", "content": reply})

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])


# ========== DIAGNOSIS ==========
elif page == "🧠 Diagnosis 🩺":
    st.header("🧠 Diagnosis Assistant 🤖")

    age = st.number_input("Age 🔢", 10, 100)
    gender = st.selectbox("Gender", ["Male ♂️", "Female ♀️", "Other ⚧️"])
    symptoms = st.text_area("Symptoms 🤒")

    if st.button("Analyze 🔎"):
        prompt = f"""
        You are a clinical assistant 🤖.

        Patient:
        Age 🔢: {age}
        Gender: {gender}
        Symptoms 🤒: {symptoms}

        Provide:
        1. Possible diagnoses 🩺
        2. Risk level 🚨
        3. Suggested tests 📝
        4. Red flags 🚩
        """
        with st.spinner("Analyzing 🔄..."):
            result = get_ai_response(prompt=prompt)
        st.write(result)


# ========== TREATMENT ==========
elif page == "💊 Treatment":
    st.header("💊 Treatment Planner 📜")

    diagnosis = st.text_area("🧠 Diagnosis 🩺")

    if st.button("Generate Plan 📜"):
        prompt = f"""
        You are a treatment planning assistant 🤖.

        🧠 Diagnosis 🩺: {diagnosis}

        Provide:
        - Treatment 🩺 options
        - Medications 💊
        - Lifestyle advice 💡
        - When to see a 👩‍⚕️ doctor 👨‍⚕️
        """
        with st.spinner("🤖 Generating treatment 🧬 plan 📜..."):
            result = get_ai_response(prompt=prompt)
        st.write(result)


# ========== DRUG CHECKER ==========
elif page == "💉 Drug Checker":
    st.header("💉 Drug Interaction Checker")

    drugs = st.text_area("Enter drugs 💊 (comma separated)")

    if st.button("Check ✅"):
        prompt = f"""
        You are a pharmacology expert.

        Drugs 💊: {drugs}

        Provide:
        - Interactions
        - Warnings ⚠️
        - Safer alternatives
        """
        with st.spinner("Checking interactions..."):
            result = get_ai_response(prompt=prompt)
        st.write(result)


# ========== DISCLAIMER ==========
st.warning("⚠️ This tool 🤖 is for educational purposes only. NOT ❌ a real medical diagnosis. 🚨")

# =========================
# FOOTER
# =========================
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:orange;'>Designed & Developed by</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:gold;'>Hemant Katta</p>", unsafe_allow_html=True)

# streamlit run appp.py