import streamlit as st
from groq import Groq
import datetime

# --- Page Configuration ---
st.set_page_config(page_title="Hangout Planner", page_icon="🗺️", layout="centered")

# --- Professional Liquid Glassmorphism CSS with Background Image ---
st.markdown("""
<style>
/* Stunning Background Image */
.stApp {
    background-image: url("https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=2564&auto=format&fit=crop");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    color: #ffffff;
}

/* Hide default Streamlit elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {background: transparent !important;}

/* Liquid Glass Container */
.glass-container {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(25px);
    -webkit-backdrop-filter: blur(25px);
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 24px;
    padding: 2.5rem;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4);
    margin-bottom: 2rem;
    transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow 0.4s ease, background 0.4s ease;
}

/* Custom Animation on Hover */
.glass-container:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 45px 0 rgba(0, 0, 0, 0.5);
    background: rgba(255, 255, 255, 0.08);
}

/* Strict Text Visibility Rules - Ensuring high contrast against the background */
h1, h2, h3, h4, h5, h6, p, label, .stMarkdown, .stText {
    color: #ffffff !important;
    text-shadow: 0 2px 6px rgba(0,0,0,0.7);
    letter-spacing: 0.5px;
}

/* Form Inputs Styling */
.stTextInput>div>div>input, 
.stNumberInput>div>div>input, 
.stSelectbox>div>div>div, 
.stTimeInput>div>div>input {
    background-color: rgba(0, 0, 0, 0.35) !important;
    color: #ffffff !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    border-radius: 8px !important;
}

/* Input Focus States */
.stTextInput>div>div>input:focus, 
.stNumberInput>div>div>input:focus, 
.stSelectbox>div>div>div:focus, 
.stTimeInput>div>div>input:focus {
    border: 1px solid rgba(255, 255, 255, 0.6) !important;
    box-shadow: 0 0 12px rgba(255, 255, 255, 0.2) !important;
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
    box-shadow: 0 4px 15px rgba(37, 99, 235, 0.5);
    transition: all 0.3s ease;
    text-shadow: none;
}

.stButton>button:hover {
    transform: scale(1.02);
    box-shadow: 0 6px 20px rgba(37, 99, 235, 0.7);
    background: linear-gradient(90deg, #60a5fa 0%, #3b82f6 100%);
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; margin-bottom: 2rem;'>🗺️ Perfect Hangout Planner</h1>", unsafe_allow_html=True)

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
    # Securely checking for the API Key in Streamlit Secrets
    if "GROQ_API_KEY" not in st.secrets:
        st.error("API Key not found! Please ensure it is configured in Streamlit Secrets.")
    else:
        api_key = st.secrets["GROQ_API_KEY"]
        
        with st.spinner("Analyzing routes, crunching budgets, and drafting the itinerary..."):
            try:
                # Initialize Groq Client securely
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

                # Call the Groq API using Llama 3.3 70B
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
                    model="llama-3.3-70b-versatile", 
                    temperature=0.7,
                )
                
                # Render Results
                st.markdown('<div class="glass-container">', unsafe_allow_html=True)
                st.success("✨ Itinerary Generated Successfully!")
                st.markdown(chat_completion.choices[0].message.content)
                st.markdown('</div>', unsafe_allow_html=True)

            except Exception as e:
                st.error(f"An error occurred: {e}")
