import streamlit as st
from groq import Groq
import datetime

# --- Page Configuration ---
st.set_page_config(page_title="Hangout Planner", page_icon="🗺️", layout="centered")

# --- Professional Liquid Glassmorphism CSS ---
st.markdown("""
<style>
/* Smoothly animated liquid background */
@keyframes gradientBG {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* Base App Styling */
.stApp {
    background: linear-gradient(-45deg, #0f172a, #1e293b, #334155, #0f172a);
    background-size: 400% 400%;
    animation: gradientBG 15s ease infinite;
    color: #ffffff;
}

/* Hide default Streamlit elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {background: transparent !important;}

/* Liquid Glass Container */
.glass-container {
    background: rgba(255, 255, 255, 0.03);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 24px;
    padding: 2.5rem;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
    margin-bottom: 2rem;
    transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow 0.4s ease;
}

/* Custom Animation on Hover */
.glass-container:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 45px 0 rgba(0, 0, 0, 0.4);
    background: rgba(255, 255, 255, 0.05);
}

/* Strict Text Visibility Rules */
h1, h2, h3, h4, h5, h6, p, label, .stMarkdown, .stText {
    color: #ffffff !important;
    text-shadow: 0 2px 4px rgba(0,0,0,0.4);
    letter-spacing: 0.5px;
}

/* Form Inputs Styling */
.stTextInput>div>div>input, 
.stNumberInput>div>div>input, 
.stSelectbox>div>div>div, 
.stTimeInput>div>div>input {
    background-color: rgba(0, 0, 0, 0.2) !important;
    color: #ffffff !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 8px !important;
}

/* Input Focus States */
.stTextInput>div>div>input:focus, 
.stNumberInput>div>div>input:focus, 
.stSelectbox>div>div>div:focus, 
.stTimeInput>div>div>input:focus {
    border: 1px solid rgba(255, 255, 255, 0.5) !important;
    box-shadow: 0 0 10px rgba(255, 255, 255, 0.1) !important;
}

/* Professional Primary Button */
.stButton>button {
    width: 100%;
    border-radius: 12px;
    background: linear-gradient(90deg, #3b82f6 0%, #2563eb 100%);
    color: white !important;
    border: none;
    padding: 0.8rem;
    font-weight: 600;
    font-size: 1.1rem;
    letter-spacing: 1px;
    box-shadow: 0 4px 15px rgba(37, 99, 235, 0.4);
    transition: all 0.3s ease;
    text-shadow: none;
}

.stButton>button:hover {
    transform: scale(1.02);
    box-shadow: 0 6px 20px rgba(37, 99, 235, 0.6);
    background: linear-gradient(90deg, #60a5fa 0%, #3b82f6 100%);
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; margin-bottom: 2rem;'>🗺️ Perfect Hangout Planner</h1>", unsafe_allow_html=True)

# --- API Key Setup ---
api_key = st.text_input("Enter your Groq API Key:", type="password", placeholder="Paste your API key here...")

# --- Input Form ---
with st.container():
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    
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
if st.button("Generate Hangout Plan"):
    if not api_key:
        st.warning("Please enter your Groq API Key to generate the plan.")
    else:
        with st.spinner("Analyzing routes, crunching budgets, and drafting the itinerary..."):
            try:
                # Initialize Groq Client
                client = Groq(api_key=api_key)

                prompt = f"""
                You are an expert local trip planner. Create a highly detailed, chronological timetable for a short hangout based on the following parameters:
                - Start Location: {start_location}
                - Hangout Location: {hangout_location}
                - Timing: {start_time.strftime('%I:%M %p')} to {end_time.strftime('%I:%M %p')}
                - Number of People: {people_count}
                - Budget per person: ₹{budget}
                - Vibe/Place: {hangout_type}
                - Transport Mode: {transport_mode}
                - Eating Preferences: {eating}

                Provide a perfectly planned timetable. You must include:
                1. Exact meeting spots for the group.
                2. Estimated travel times considering {transport_mode} and typical traffic/external factors between {start_location} and {hangout_location}.
                3. Specific real-world venue/cafe recommendations in {hangout_location} that fit the ₹{budget} per person budget.
                4. A breakdown of the budget (transport vs. food vs. activities).
                5. Total estimated cost per person to ensure it stays strictly under budget.

                Format the output beautifully using Markdown. Use clear time blocks (e.g., **11:00 AM - 11:30 AM: Travel**). Do not use nested bullet points. Ensure the tone is structured and professional.
                """

                # Call the Groq API (using Llama 3 for fast, intelligent generation)
                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a highly efficient, budget-conscious local travel planner."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    model="llama3-8b-8192", 
                    temperature=0.7,
                )
                
                # Render Results
                st.markdown('<div class="glass-container">', unsafe_allow_html=True)
                st.success("✨ Itinerary Generated Successfully!")
                st.markdown(chat_completion.choices[0].message.content)
                st.markdown('</div>', unsafe_allow_html=True)

            except Exception as e:
                st.error(f"An error occurred: {e}")
