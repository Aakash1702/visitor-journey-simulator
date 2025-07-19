import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os
from datetime import datetime
import folium
from streamlit_folium import st_folium
from PIL import Image


logo = Image.open("1740753183850.JPG")
st.image(logo, width=200)

st.markdown("<h1 style='color: #0094D8;'>Destination Cleveland: Visitor Journey Simulator</h1>", unsafe_allow_html=True)
st.markdown("### Discover Cleveland through the eyes of every kind of visitor 🚶‍♀️🍽️🎭")

st.markdown("""
    <style>
        .main {
            background-color: #f9fcff;
        }
        .stApp {
            font-family: 'Segoe UI', sans-serif;
        }
        h1, h2, h3, h4 {
            color: #0094D8;
        }
        .css-18e3th9 {
            background-color: #ffffff;
        }
        .stButton > button {
            background-color: #0094D8;
            color: white;
            border-radius: 5px;
            border: none;
            padding: 8px 16px;
        }
        .stButton > button:hover {
            background-color: #007bbf;
        }
    </style>
""", unsafe_allow_html=True)



st.set_page_config(page_title="Visitor Journey Simulator", layout="wide")
tab1, tab2 = st.tabs(["🚦 Visitor Simulator", "📊 Visitor Insights"])

with tab1:
    st.title("🗺️ Visitor Journey Simulator – Cleveland Edition")

    # --- 1. Persona
    st.header("👤 Select Your Visitor Persona")
    persona = st.radio("What best describes you?", [
        "First-time Tourist", "Food Lover", "Arts & Culture Fan", "Family Traveler", "Budget Explorer"
    ])

    # --- 2. Journey Stops
    st.header("📍 Your Suggested Journey")
    journey_stops = {
        "First-time Tourist": ["West Side Market", "Rock & Roll Hall of Fame", "Edgewater Park", "East 4th Street Dining"],
        "Food Lover": ["West Side Market", "Momocho", "Lucky's Cafe", "E 4th Street Food Tour"],
        "Arts & Culture Fan": ["Cleveland Museum of Art", "Severance Hall", "MOCA", "Playhouse Square"],
        "Family Traveler": ["Cleveland Zoo", "Great Lakes Science Center", "Edgewater Beach", "Cleveland Aquarium"],
        "Budget Explorer": ["Public Square", "Cleveland Public Library", "Edgewater Park", "Little Italy Walk"]
    }

    for stop in journey_stops[persona]:
        st.write(f"- {stop}")

    # --- 3. Map
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

    stops = journey_stops[persona]
    journey_map = folium.Map(location=location_coords[stops[0]], zoom_start=13)
    points = []
    for stop in stops:
        coord = location_coords.get(stop)
        if coord:
            folium.Marker(coord, popup=stop, tooltip=stop).add_to(journey_map)
            points.append(coord)
    if len(points) > 1:
        folium.PolyLine(points, color="blue", weight=3).add_to(journey_map)
    st_folium(journey_map, width=750, height=500)

    # --- 4. Form
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
        write_headers = not os.path.exists("visitor_logs.csv")
        df.to_csv("visitor_logs.csv", mode="a", index=False, header=write_headers)
        st.success("✅ Submission recorded.")

        # 🔄 Force rerun to clear form inputs
        st.rerun()


    # Optional log view
    if st.checkbox("📂 Preview Submitted Logs"):
        try:
            logs = pd.read_csv("visitor_logs.csv")
            st.dataframe(logs.tail(5))
        except Exception as e:
            st.warning(f"Error loading file: {e}")

# ---- 5. DASHBOARD TAB ----
with tab2:
    st.header("📊 Visitor Insights Dashboard")
    try:
        df = pd.read_csv("visitor_logs.csv")
        st.write("✅ Columns found:", df.columns.tolist())  # Debug
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])

        st.subheader("👤 Most Selected Visitor Personas")
        st.bar_chart(df['Persona'].value_counts())

        st.subheader("🎯 Travel Purpose Breakdown")
        st.bar_chart(df['Reason'].value_counts())

        st.subheader("📅 Submission Timeline")
        daily = df['Timestamp'].dt.date.value_counts().sort_index()
        st.line_chart(daily)

        st.subheader("🧭 Recent ZIP Codes (Last 5)")
        st.write(df[['ZIP', 'Reason', 'Duration']].tail(5))

        # Word Cloud of Favorite Experiences
        st.subheader("🧡 What Visitors Enjoy Most (Word Cloud)")

        fav_text = " ".join(df["Liked Most"].dropna().astype(str))
        if fav_text.strip():
            wordcloud = WordCloud(width=800, height=300, background_color='white').generate(fav_text)
            fig, ax = plt.subplots()
            ax.imshow(wordcloud, interpolation='bilinear')
            ax.axis("off")
            st.pyplot(fig)
        else:
            st.info("No favorite experience data yet.")

        # Trip Duration
        st.subheader("⏳ Trip Duration Breakdown")
        duration_counts = df['Duration'].value_counts()
        st.bar_chart(duration_counts)

        st.subheader("👥 Who Do Visitors Travel With?")
        companion_counts = df['Companion'].value_counts()
        st.bar_chart(companion_counts)

        st.subheader("😕 Common Pain Points (Least Liked Experiences)")
        least_liked_counts = df["Liked Least"].dropna().str.lower().value_counts().head(10)
        st.write(least_liked_counts)

        # import seaborn as sns

        # st.subheader("📆 Daily Submissions Heatmap")
        # df["Date"] = pd.to_datetime(df["Timestamp"]).dt.date
        # daily_counts = df.groupby("Date")["Email"].count().reset_index(name="Submissions")

        # if not daily_counts.empty:
        #     fig, ax = plt.subplots()
        #     heatmap_data = daily_counts.pivot_table(index="Date", values="Submissions").astype(int)
        #     sns.heatmap(data=heatmap_data, annot=True, fmt="d", cmap="Blues", ax=ax)
        #     st.pyplot(fig)
        # else:
        #     st.info("No submissions yet for heatmap.")


        st.download_button("⬇️ Download Visitor Data", df.to_csv(index=False), "visitor_data.csv", "text/csv")




    except Exception as e:
        st.warning(f"No data found yet. Submit a journey first! ({e})")
