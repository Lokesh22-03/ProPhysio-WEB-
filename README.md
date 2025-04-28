# ProPhysio-WEB-
🖥️ ProPhysioAI Web App (Streamlit)
This is the Streamlit version of the ProPhysioAI project — a smart AI assistant for athletes that predicts injury risk, provides rehabilitation guidance, and suggests personalized diet plans using OpenAI's GPT-4.

✨ Main Features
🏃 Athlete Info Form:
Collects key data — age, weight, height, previous injuries, training intensity, recovery time, diet type, sport, and fitness goals.

🧮 BMI Calculation:
Automatically calculates Body Mass Index (BMI) and categorizes it (Underweight, Normal, Overweight, Obesity I, Obesity II) with color-coded status.

🧟 Injury Risk Prediction (using GPT-4):
Based on athlete data, the app predicts whether the injury risk is High or Low using natural language processing with GPT-4-turbo.

🏥 Injury Rehab & Treatment Advice:
If the athlete reports an existing injury, the app generates a treatment plan, precautions, and rehabilitation exercises using GPT-4-turbo.

🥗 Personalized Diet Plan Generator:
Based on BMI, injury risk, fitness goals, sport type, and diet preference, the app generates a 1-day meal plan along with "what to do" and "what not to do" advice.

⚙️ Technologies Used
Python (Backend)

Streamlit (Web UI Framework)

OpenAI GPT-4-turbo API (for AI responses)

dotenv (for securely loading API keys)

joblib (imported, but not used yet)

Pandas (imported, but not used yet)

🗂️ Folder Structure
bash
Copy
Edit
/prophysioai-web
  app.py          # Main Streamlit app
  .env            # For storing the OpenAI API key
  requirements.txt
  README.md
🚀 How to Run Locally
Clone the repository:

bash
Copy
Edit
git clone https://github.com/your-repo/prophysioai-web.git
cd prophysioai-web
Install dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Create a .env file:

ini
Copy
Edit
OPENAI_API_KEY=your_openai_api_key_here
Run the app:

bash
Copy
Edit
streamlit run app.py
📋 Notes
You must have an OpenAI API key (GPT-4 access).

The app uses Streamlit's session state to track injury risk before allowing diet generation.

Uses three separate GPT-4 prompts:

For predicting injury risk

For generating rehab advice

For creating diet plans

🙏 Credits
Built using OpenAI GPT-4-turbo.

Designed with Streamlit for simplicity and speed.

Created to help athletes stay healthy, recover faster, and perform better.

✅ Example Screens in the Web App
Fill in athlete details

Predict injury risk

Get rehab advice if needed

Generate a 1-day customized diet plan
