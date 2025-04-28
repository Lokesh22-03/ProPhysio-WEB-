import streamlit as st
import pandas as pd
import joblib
import time
import os
import openai
from dotenv import load_dotenv

# Page Config
st.set_page_config(page_title="ProPhysio AI", layout="wide", page_icon="⚕️")

# Load API Key
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    st.error("🔑 OpenAI API key is missing! Set it in a .env file.")
else:
    openai.api_key = API_KEY

st.title("🏃 ProPhysio AI: Injury Risk, Diet & Rehab Coach")

# Sidebar Inputs
with st.sidebar:
    st.header("⚙️ Athlete Information")
    Player_Age = st.number_input('Enter Age', min_value=0, value=24)
    Player_Weight = st.number_input('Enter Weight (kg)', min_value=0.0, value=66.25)
    Player_Height = st.number_input('Enter Height (cm)', min_value=0.0, value=175.73)

    Previous_Injuries = st.radio('Previous Injuries?', ['No', 'Yes'])
    Injury_Type = st.text_input('Type of Injury', placeholder='e.g., Ankle Sprain, ACL Tear') if Previous_Injuries == 'Yes' else "None"

    Training_Intensity = st.slider('Training Intensity (1-10)', min_value=0.1, max_value=10.0, value=0.46)
    Recovery_Time = st.number_input('Recovery Time (days)', min_value=0, value=5)
    Diet_Type = st.radio("Diet Preference:", ["Veg", "Non-Veg"])

    Fitness_Goal = st.selectbox("🏋️ Select Fitness Goal:", [
        "Build Muscle", "Lose Fat", "Improve Endurance", "Increase Flexibility", "Injury Prevention"
    ])

    Sport_Type = st.selectbox("🏆 Select Sport:", [
        "Football", "Basketball", "Running", "Swimming", "Tennis", "Weightlifting", "Cricket", "Other"
    ])

# BMI Calculations
bmi_value = Player_Weight / ((Player_Height / 100) ** 2)
if bmi_value < 18.5:
    BMI_Classification = "Underweight"
elif bmi_value < 24.9:
    BMI_Classification = "Normal"
elif bmi_value < 29.9:
    BMI_Classification = "Overweight"
elif bmi_value < 34.9:
    BMI_Classification = "Obesity I"
else:
    BMI_Classification = "Obesity II"

bmi_color_map = {
    'Normal': 'green', 'Obesity I': 'red', 'Obesity II': 'darkred',
    'Overweight': 'orange', 'Underweight': 'blue'
}
bmi_color = bmi_color_map[BMI_Classification]
st.markdown(f"### 🧮 BMI Status: <span style='color:{bmi_color}; font-weight:bold'>{BMI_Classification} ({bmi_value:.2f})</span>", unsafe_allow_html=True)

# GPT-4: Injury Treatment
def get_injury_treatment(injury):
    prompt = f"""
You are a licensed physiotherapist. An athlete is recovering from this injury: {injury}.
Provide:
- ✅ A treatment plan (what to do)
- ❌ Precautions or actions to avoid (what not to do)
- 💪 Recommended rehabilitation exercises
Be concise and helpful.
"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful physiotherapist."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Error: {e}"

# GPT-4: Diet Plan
def get_diet_plan(prompt):
    full_prompt = f"""
You are a certified sports nutritionist.
Create a personalized diet plan for this athlete:
{prompt}

Include:
- ✅ What foods/nutrients to include (what to do)
- ❌ What foods/behaviors to avoid (what not to do)
- 🍽️ Meal plan suggestions for 1 day

Use clear formatting. Sign the response as ProPhysioAI.
"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a"
                " certified nutritionist."},
                {"role": "user", "content": full_prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Error generating diet plan: {e}"

# GPT-4: Injury Risk Explanation
def get_gpt_risk_explanation(predicted_risk):
    prompt = f"""
You are a professional sports physiotherapist.
Explain for this athlete:

- Age: {Player_Age}, Weight: {Player_Weight}kg, Height: {Player_Height}cm
- Previous Injuries: {Previous_Injuries} ({Injury_Type})
- Training Intensity: {Training_Intensity}/10, Recovery Time: {Recovery_Time} days
- BMI Category: {BMI_Classification}
- Fitness Goal: {Fitness_Goal}, Sport: {Sport_Type}
- Predicted Injury Risk: {predicted_risk}

Provide:
✅ Why this risk level may be predicted  
❌ Behaviors to avoid  
💡 Tips to improve safety and performance

Sign the response as ProPhysioAI.
"""
    try:
        explanation_response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a knowledgeable and supportive physiotherapist."},
                {"role": "user", "content": prompt}
            ]
        )
        return explanation_response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Unable to generate explanation: {e}"

# Injury Risk (via GPT-4)
st.subheader("🧟 Injury Risk Prediction")
if st.button("⚡ Predict Injury Risk (via ProPhysioAI)"):
    with st.spinner("ProPhysioAI is analyzing..."):
        time.sleep(2)
        risk_prompt = f"""
Based on the following athlete profile, predict injury risk as 'High' or 'Low':
- Age: {Player_Age}, Weight: {Player_Weight}kg, Height: {Player_Height}cm
- Previous Injuries: {Previous_Injuries} ({Injury_Type})
- Training Intensity: {Training_Intensity}/10, Recovery Time: {Recovery_Time} days
- BMI Category: {BMI_Classification}
- Fitness Goal: {Fitness_Goal}, Sport: {Sport_Type}
"""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert physiotherapist."},
                    {"role": "user", "content": risk_prompt}
                ]
            )
            risk_level = "High" if "High" in response.choices[0].message.content else "Low"
            st.session_state.injury_risk = 3 if risk_level == "High" else 1

            if risk_level == "High":
                st.error("🚨 High Risk of Severe Injury!")
            else:
                st.success("✅ Athlete is Fit!")

            # Expert Explanation
            st.subheader("🧠 ProPhysioAI's Expert Explanation")
            st.info(get_gpt_risk_explanation(risk_level))

        except Exception as e:
            st.error(f"⚠️ Unable to get injury risk: {e}")

# Injury Treatment Plan
if Injury_Type != "None" and Injury_Type.strip():
    st.subheader("🏥 Injury Rehab & Treatment")
    st.info(get_injury_treatment(Injury_Type))

# Diet Plan
st.subheader("🥗 Personalized Diet Plan (ProPhysioAI)")
if st.session_state.get("injury_risk", None):
    additional_input = st.text_area("📝 Additional Notes (allergies, preferences, etc.)", placeholder="e.g., lactose intolerant, high protein, avoid sugar")
    user_input = (
        f"Athlete with {BMI_Classification} BMI, injury risk level {st.session_state.injury_risk}, "
        f"fitness goal: {Fitness_Goal}, sport: {Sport_Type}, previous injury: {Injury_Type}, prefers {Diet_Type} diet."
    )
    if additional_input:
        user_input += f" Additional notes: {additional_input}"

    if st.button("🍱 Generate Diet Plan"):
        with st.spinner("ProPhysioAI is crafting your personalized nutrition guide..."):
            st.info(get_diet_plan(user_input))
else:
    st.warning("⚠️ Please predict the injury risk first before generating a diet plan.")
