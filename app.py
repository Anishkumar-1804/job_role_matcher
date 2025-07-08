import streamlit as st
import requests

# ✅ Gemini 1.5 model endpoint
GEMINI_API_KEY = "AIzaSyCqkQOhb5XTr0K4LUtdAyolyXcNBT3l1uc"
GEMINI_MODEL = "gemini-1.5-pro-latest"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"

def get_job_roles(skills, experience, interests):
    prompt = f"""
    User Profile:
    - Skills: {skills}
    - Experience: {experience}
    - Interests: {interests}

    Based on this information, suggest the top 5 job roles the user is most suited for. 
    For each role, include:
    - Job Title
    - Why it matches the user
    - Required upskilling or certifications
    - Industry domain

    Format:
    1. Role: ...
       Match Reason: ...
       Upskilling: ...
       Industry: ...
    """

    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }

    response = requests.post(
        f"{GEMINI_URL}?key={GEMINI_API_KEY}",
        headers=headers,
        json=data
    )

    if response.status_code == 200:
        return response.json()["candidates"][0]["content"]["parts"][0]["text"]
    else:
        return f"❌ Gemini API Error {response.status_code}: {response.text}"

# ✅ Streamlit Interface
st.set_page_config(page_title="Job Role Matcher AI")
st.title("🔍 Job Role Matcher using Gemini 1.5")
st.write("Get job recommendations based on your skills, experience, and interests.")

skills = st.text_area("🧠 Skills", placeholder="e.g. Python, Machine Learning, SQL")
experience = st.text_input("📅 Experience", placeholder="e.g. 2 years in data science")
interests = st.text_area("💡 Interests", placeholder="e.g. AI, fintech, edtech")

if st.button("Suggest Jobs"):
    if not skills or not experience or not interests:
        st.warning("Please complete all fields.")
    else:
        with st.spinner("Contacting Gemini 1.5..."):
            result = get_job_roles(skills, experience, interests)
            st.subheader("🎯 Suggested Roles:")
            st.markdown(result)
