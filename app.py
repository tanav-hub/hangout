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
    if "GROQ_API_KEY" not in st.secrets:
        st.error("API Key not found! Please ensure it is configured in Streamlit Secrets.")
    else:
        api_key = st.secrets["GROQ_API_KEY"]
        
        with st.spinner("Mapping routes, pulling local venue data, and crunching the budget..."):
            try:
                client = Groq(api_key=api_key)

                # --- REFINED PROMPT ENGINEERING ---
                prompt = f"""
                You are an expert, hyper-local trip planner with up-to-date knowledge of current (2026) prices, transport routes, and real-world venues. 
                
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
                1. **Real Entities Only:** Name ACTUAL cafes, restaurants, parks, or malls in {hangout_location}. Do not use generic placeholders. If they want a cafe, name a specific, popular local cafe that fits their budget.
                2. **Realistic 2026 Pricing:** Factor in current inflation for India. Use realistic estimates for {transport_mode} (e.g., current auto-rickshaw meter rates, Rapido fares, local bus/metro tickets) and food menus.
                3. **Actionable Roadmap:** 
                   - Define an exact, recognizable meeting landmark in {start_location}.
                   - Provide a step-by-step transit roadmap between locations.
                4. **Itemized Budget:** You MUST end with a receipt-style breakdown proving the plan stays under the ₹{budget} per person limit (split into Transport, Food, and Activities). 

                Format the output beautifully using Markdown. 
                Use clear time blocks (e.g., **11:00 AM - 11:30 AM: Transit via [Mode]**). 
                Do not use nested bullet points.
                """

                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "system",
                            "content": "You are an elite local concierge and routing expert. You prioritize absolute geographical accuracy, real-world businesses, and strict budget adherence."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    model="llama-3.3-70b-versatile", 
                    temperature=0.4, # Lowered temperature slightly for more factual/less creative entity generation
                )
                
                # Render Results
                st.markdown('<div class="glass-container">', unsafe_allow_html=True)
                st.success("✨ Detailed Roadmap Generated Successfully!")
                st.markdown(chat_completion.choices[0].message.content)
                st.markdown('</div>', unsafe_allow_html=True)

            except Exception as e:
                st.error(f"An error occurred: {e}")
