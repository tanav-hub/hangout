import streamlit as st
from groq import Groq
import datetime

# --- Page Configuration ---
st.set_page_config(page_title="Hangout Planner", page_icon="🗺️", layout="centered")

# --- Aura Fluidic Design CSS Injection ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@400;500;600;700;800&display=swap');

/* Base App Styling & Animated Background */
@keyframes gradientBG {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.stApp {
    background: linear-gradient(-45deg, #0b0f10, #101415, #001f25, #2c0051);
    background-size: 400% 400%;
    animation: gradientBG 15s ease infinite;
    font-family: 'Hanken Grotesk', sans-serif !important;
    color: #e0e3e5;
}

/* Hide default Streamlit elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {background: transparent !important;}

/* Typography Overrides */
h1, h2, h3, h4, h5, h6, p, label, .stMarkdown, .stText, span {
    font-family: 'Hanken Grotesk', sans-serif !important;
    color: #e0e3e5 !important;
    text-shadow: 0 2px 4px rgba(0,0,0,0.5);
}

h1 {
    font-weight: 800 !important;
    font-size: 48px !important;
    letter-spacing: -0.02em !important;
}

h2 {
    color: #00daf8 !important; /* Primary Accent */
    font-weight: 700 !important;
}

/* Glass Panel Component (Level 2 Elevation) */
.glass-panel {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(25px);
    -webkit-backdrop-filter: blur(25px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-top: 1px solid rgba(255, 255, 255, 0.2);
    border-left: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 16px;
    padding: 2.5rem;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
    margin-bottom: 2rem;
    transition: transform 0.4s ease, box-shadow 0.4s ease;
}

.glass-panel:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.4);
}

/* Deep Well Inputs */
.stTextInput>div>div>input, 
.stNumberInput>div>div>input, 
.stSelectbox>div>div>div, 
.stTimeInput>div>div>input {
    background: rgba(0, 0, 0, 0.4) !important;
    box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.5) !important;
    border: 1px solid rgba(255, 255, 255, 0.05) !important;
    color: #e0e3e5 !important;
    border-radius: 8px !important;
    padding: 0.75rem !important;
    transition: all 0.3s ease !important;
}

/* Deep Well Focus State */
.stTextInput>div>div>input:focus, 
.stNumberInput>div>div>input:focus, 
.stSelectbox>div>div>div:focus, 
.stTimeInput>div>div>input:focus {
    border-color: #00daf8 !important;
    box-shadow: 0 0 12px rgba(0, 224, 255, 0.5), inset 0 2px 4px rgba(0, 0, 0, 0.5) !important;
}

/* Electric Purple Primary Button */
.stButton>button {
    width: 100%;
    border-radius: 12px;
    background: linear-gradient(135deg, #00daf8, #7701d0) !important;
    color: white !important;
    border: none;
    padding: 1rem;
    font-weight: 700;
    font-size: 1.2rem;
    letter-spacing: 0.5px;
    transition: all 0.3s ease;
    text-shadow: 0 2px 4px rgba(0,0,0,0.8) !important;
}

.stButton>button:hover {
    transform: scale(1.02);
    box-shadow: 0 0 20px rgba(0, 224, 255, 0.4) !important;
}

/* Radio Buttons */
.stRadio > div {
    gap: 1.5rem;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; margin-bottom: 0.5rem;'>🗺️ Perfect Hangout Planner</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; margin-bottom: 2.5rem; color: #bac9cd !important; font-size: 18px;'>Intelligent routing, budgeting, and vibe curation for your next hangout.</p>", unsafe_allow_html=True)

# --- Input Form ---
with st.container():
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    
    st.subheader("📍 Route Details")
    col1, col2 = st.columns(2)
    start_location = col1.text_input("Starting Location", value="Kharghar")
    hangout_location = col2.text_input("Destination", value="Panvel")

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("⏰ Time & Logistics")
    col3, col4 = st.columns(2)
    start_time = col3.time_input("Start Time", datetime.time(11, 0))
    end_time = col4.time_input("End Time", datetime.time(15, 0))

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("👥 Group & Budget")
    col5, col6 = st.columns(2)
    people_count = col5.number_input("Number of People", min_value=1, value=3)
    budget = col6.number_input("Budget per person (₹)", min_value=0, value=500)

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("🎭 Vibe & Transport")
    col7, col8 = st.columns(2)
    hangout_type = col7.selectbox("Hangout Type", ["Cafe", "Mall", "Garden/Park", "Arcade/Gaming", "Movie", "Street Food Hopping"])
    transport_mode = col8.selectbox("Transport Mode", ["Rapido / Bike Taxi", "Public Transport (Bus/Train)", "Walk", "Personal Vehicle"])
    
    eating = st.radio("Dining Preferences", ["Yes, a full meal", "Yes, just snacks/drinks", "No food needed"], horizontal=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# --- Generation Logic ---
if st.button("✨ Generate Hangout Plan"):
    if "GROQ_API_KEY" not in st.secrets:
        st.error("API Key not found! Please ensure it is configured in Streamlit Secrets.")
    else:
        api_key = st.secrets["GROQ_API_KEY"]
        
        with st.spinner("Mapping routes, pulling local venue data, and crunching the budget..."):
            try:
                client = Groq(api_key=api_key)

                prompt = f"""
                You are an expert, hyper-local trip planner with up-to-date knowledge of current prices, transport routes, and real-world venues. 
                
                Create a detailed, step-by-step hangout roadmap based on these parameters:
                - Start Location: {start_location}
                - Hangout Location: {hangout_location}
                - Timing: {start_time.strftime('%I:%M %p')} to {end_time.strftime('%I:%M %p')}
                - Group Size: {people_count} people
                - Budget: ₹{budget} per person (STRICT LIMIT)
                - Vibe/Activity: {hangout_type}
                - Transport Mode: {transport_mode}
                - Dining Preference: {eating}

                CRITICAL INSTRUCTIONS:
                1. **Real Entities Only:** Name ACTUAL cafes, restaurants, parks, or malls in {hangout_location}. 
                2. **Realistic Pricing:** Factor in current inflation for India. Use realistic estimates for {transport_mode} and food.
                3. **Actionable Roadmap:** Provide a step-by-step transit roadmap between locations.
                4. **Itemized Budget:** You MUST end with a receipt-style breakdown proving the plan stays under the ₹{budget} per person limit. 

                Format the output beautifully using Markdown. 
                """

                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": "You are an elite local concierge and routing expert."},
                        {"role": "user", "content": prompt}
                    ],
                    model="llama-3.3-70b-versatile", 
                    temperature=0.4, 
                )
                
                # Render Results
                st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
                st.success("✨ Detailed Roadmap Generated Successfully!")
                st.markdown(chat_completion.choices[0].message.content)
                st.markdown('</div>', unsafe_allow_html=True)

            except Exception as e:
                st.error(f"An error occurred: {e}")
