# -------------------- Visitor Journey Simulator ---------------------
import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from PIL import Image
import folium
from streamlit_folium import st_folium
import socket
import os

# -------------------- Config ---------------------
st.set_page_config(page_title="Visitor Journey Simulator", layout="wide")
LOG_FILE = "visitor_logs.csv"

# -------------------- Session State Initialization ---------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "show_login" not in st.session_state:
    st.session_state.show_login = False

# -------------------- Visit Logging ---------------------
def log_visit(visitor_type="anonymous"):
    try:
        ip_address = requests.get('https://api64.ipify.org').text
    except:
        ip_address = "Unknown"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = {"Timestamp": timestamp, "IP": ip_address, "VisitorType": visitor_type}
    df = pd.DataFrame([entry])
    file_exists = os.path.exists(LOG_FILE)
    df.to_csv(LOG_FILE, mode="a", index=False, header=not file_exists)

log_visit("admin" if st.session_state.authenticated else "visitor")

# -------------------- Styling ---------------------
st.markdown("""
    <style>
        .main { background-color: #f9fcff; }
        .stApp { font-family: 'Segoe UI', sans-serif; }
        h1, h2, h3, h4 { color: #0094D8; }
        .css-18e3th9 { background-color: #ffffff; }
        .stButton > button {
            background-color: #0094D8;
            color: white;
            border-radius: 5px;
            border: none;
            padding: 8px 16px;
        }
        .stButton > button:hover { background-color: #007bbf; }
    </style>
""", unsafe_allow_html=True)

# -------------------- Admin Credentials ---------------------
ADMIN_CREDENTIALS = {
    "adminuser": "Cleveland2025!",
    "karin": "DC2025rocks"
}

# -------------------- Admin Login Form ---------------------
def login_section():
    st.subheader("🔐 Admin Login")
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.form_submit_button("Login"):
            if username in ADMIN_CREDENTIALS and ADMIN_CREDENTIALS[username] == password:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("❌ Invalid credentials")

# -------------------- Visitor Simulator ---------------------
def visitor_simulator():
    st.title("🗺️ Visitor Journey Simulator – Cleveland Edition")

    if not st.session_state.authenticated and not st.session_state.show_login:
        if st.button("🔐 Admin Login"):
            st.session_state.show_login = True
            st.rerun()

    if st.session_state.show_login and not st.session_state.authenticated:
        login_section()
        return

    # Header and logo
    logo = Image.open("1740753183850.JPG")
    st.image(logo, width=200)
    st.markdown("<h1 style='color: #0094D8;'>Destination Cleveland: Visitor Journey Simulator</h1>", unsafe_allow_html=True)
    st.markdown("### Discover Cleveland through the eyes of every kind of visitor 🚶‍♀️🍽️🎭")

    st.header("👤 Select Your Visitor Persona")
    persona = st.radio("What best describes you?", [
        "First-time Tourist", "Food Lover", "Arts & Culture Fan", "Family Traveler", "Budget Explorer"
    ])

    # Map Locations
    journey_stops = {
        "First-time Tourist": ["West Side Market", "Rock & Roll Hall of Fame", "Edgewater Park", "East 4th Street Dining"],
        "Food Lover": ["West Side Market", "Momocho", "Lucky's Cafe", "E 4th Street Food Tour"],
        "Arts & Culture Fan": ["Cleveland Museum of Art", "Severance Hall", "MOCA", "Playhouse Square"],
        "Family Traveler": ["Cleveland Zoo", "Great Lakes Science Center", "Edgewater Beach", "Cleveland Aquarium"],
        "Budget Explorer": ["Public Square", "Cleveland Public Library", "Edgewater Park", "Little Italy Walk"]
    }
    location_coords = {
        "West Side Market": (41.4841, -81.7038),
        "Rock & Roll Hall of Fame": (41.5080, -81.6954),
        "Edgewater Park": (41.4946, -81.7482),
        "East 4th Street Dining": (41.4993, -81.6892),
        "Momocho": (41.4899, -81.7031),
        "Lucky's Cafe": (41.4780, -81.6901),
        "Cleveland Museum of Art": (41.5085, -81.6118),
        "Severance Hall": (41.5079, -81.6097),
        "MOCA": (41.5081, -81.6106),
        "Playhouse Square": (41.5010, -81.6806),
        "Cleveland Zoo": (41.4457, -81.7054),
        "Great Lakes Science Center": (41.5076, -81.6986),
        "Edgewater Beach": (41.4930, -81.7480),
        "Cleveland Aquarium": (41.4963, -81.7061),
        "Public Square": (41.4981, -81.6954),
        "Cleveland Public Library": (41.4993, -81.6921),
        "Little Italy Walk": (41.5098, -81.5985)
    }

    st.header("📍 Your Suggested Journey")
    for stop in journey_stops[persona]:
        st.write(f"- {stop}")

    # Map Rendering
    stops = journey_stops[persona]
    journey_map = folium.Map(location=location_coords[stops[0]], zoom_start=13)
    points = [location_coords[stop] for stop in stops if stop in location_coords]
    for stop, coord in zip(stops, points):
        folium.Marker(coord, popup=stop, tooltip=stop).add_to(journey_map)
    if len(points) > 1:
        folium.PolyLine(points, color="blue", weight=3).add_to(journey_map)
    st_folium(journey_map, width=750, height=500)

    # Feedback Form
    st.header("📝 Help Us Improve Cleveland Experiences")
    with st.form("visitor_form"):
        zip_code = st.text_input("ZIP Code")
        travel_reason = st.selectbox("Reason for Travel", ["Leisure", "Business", "Event/Festival", "Visiting Family", "Other"])
        trip_duration = st.selectbox("Trip Duration", ["Day trip", "1–2 days", "3–5 days", "1 week or more"])
        travel_companion = st.radio("Who are you traveling with?", ["Solo", "Family", "Friends", "Partner", "Group Tour"])
        favorite_experience = st.text_area("🧡 What did you enjoy most about your Cleveland visit?")
        least_fav_experience = st.text_area("😕 What could have been better?")
        email = st.text_input("Email (optional)")
        submitted = st.form_submit_button("Submit")

    if submitted:
        data = {
            "Timestamp": [datetime.now()],
            "Persona": [persona],
            "ZIP": [zip_code],
            "Reason": [travel_reason],
            "Duration": [trip_duration],
            "Companion": [travel_companion],
            "Liked Most": [favorite_experience],
            "Liked Least": [least_fav_experience],
            "Email": [email]
        }
        df = pd.DataFrame(data)
        write_headers = not os.path.exists(LOG_FILE)
        df.to_csv(LOG_FILE, mode="a", index=False, header=write_headers)
        st.success("✅ Submission recorded.")
        st.rerun()

# -------------------- Dashboard ---------------------
def admin_dashboard():
    st.header("📊 Visitor Insights Dashboard")
    if st.button("🚪 Logout"):
        st.session_state.authenticated = False
        st.session_state.show_login = False
        st.rerun()

    try:
        df = pd.read_csv(LOG_FILE)
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])

        st.subheader("👤 Most Selected Visitor Personas")
        st.bar_chart(df['Persona'].value_counts())

        st.subheader("🎯 Travel Purpose Breakdown")
        st.bar_chart(df['Reason'].value_counts())

        st.subheader("📅 Submission Timeline")
        st.line_chart(df['Timestamp'].dt.date.value_counts().sort_index())

        st.subheader("🧭 Recent ZIP Codes")
        st.write(df[['ZIP', 'Reason', 'Duration']].tail(5))

        st.subheader("🧡 Favorite Experiences (Word Cloud)")
        text = " ".join(df["Liked Most"].dropna().astype(str))
        if text.strip():
            wc = WordCloud(width=800, height=300, background_color='white').generate(text)
            fig, ax = plt.subplots()
            ax.imshow(wc, interpolation='bilinear')
            ax.axis("off")
            st.pyplot(fig)
        else:
            st.info("No favorite experiences yet.")

        st.subheader("⏳ Trip Duration")
        st.bar_chart(df['Duration'].value_counts())

        st.subheader("👥 Travel Companions")
        st.bar_chart(df['Companion'].value_counts())

        st.subheader("😕 Pain Points")
        st.write(df["Liked Least"].dropna().str.lower().value_counts().head(10))

        st.download_button("⬇️ Download Visitor Data", df.to_csv(index=False), "visitor_data.csv", "text/csv")

    except Exception as e:
        st.warning(f"No data available. Please submit some visitor data first. ({e})")

# -------------------- Launch App ---------------------
if st.session_state.authenticated:
    admin_dashboard()
else:
    visitor_simulator()
