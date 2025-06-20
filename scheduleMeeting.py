import os
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict

import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    st.error("Please set the GOOGLE_API_KEY in .env file")
    st.stop()

genai.configure(api_key=GOOGLE_API_KEY)

# Constants
DATA_DIR = Path.home() / "Desktop/ML-main/ML/meeting_data"
MEETINGS_FILE = DATA_DIR / "meetings.json"

# Functions for meeting management
def save_meeting(meeting_data: Dict) -> bool:
    try:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        existing_meetings = []
        if MEETINGS_FILE.exists():
            with open(MEETINGS_FILE, 'r') as f:
                existing_meetings = json.load(f)
        existing_meetings.append(meeting_data)
        with open(MEETINGS_FILE, 'w') as f:
            json.dump(existing_meetings, f, indent=2)
        return True
    except Exception as e:
        st.error(f"Error saving meeting: {str(e)}")
        return False

def get_all_meetings() -> List[Dict]:
    try:
        if not MEETINGS_FILE.exists():
            return []
        with open(MEETINGS_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error loading meetings: {str(e)}")
        return []

def schedule_meeting(attendees: List[str], date: str, time: str, topic: str) -> Dict:
    try:
        return {
            "attendees": attendees,
            "date": date,
            "time": time,
            "topic": topic,
            "status": "scheduled",
            "created_at": datetime.now().isoformat()
        }
    except Exception as e:
        return {"error": f"Failed to schedule meeting: {str(e)}"}

def process_scheduling_query(query: str) -> Dict:
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        prompt = f"""
        Extract meeting details from the following query and format as JSON.
        Rules:
        - Convert relative dates (tomorrow, next Monday) to YYYY-MM-DD format
        - Convert time to 24-hour format (HH:MM)
        - Include all mentioned attendees
        - Extract or infer meeting topic
        Example: Schedule a meeting with Bob tomorrow at 2 PM about project review
        Current Query: {query}
        """
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        if "```" in response_text:
            json_content = response_text.split("```")[1]
            if json_content.startswith("json\n"):
                json_content = json_content[5:]
        else:
            json_content = response_text
        meeting_params = json.loads(json_content.strip())
        meeting_data = schedule_meeting(**meeting_params)
        if save_meeting(meeting_data):
            return {
                "status": "success",
                "message": f"Meeting scheduled for {meeting_data['date']} at {meeting_data['time']}",
                "meeting": meeting_data
            }
        else:
            return {"status": "error", "message": "Failed to save meeting."}
    except json.JSONDecodeError as e:
        return {"status": "error", "message": f"JSON parse error: {str(e)}", "raw": response.text}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Streamlit UI
st.set_page_config(page_title="AI Meeting Scheduler", layout="centered")

with st.container():
    st.markdown("""
        <style>
            .main {
                background-color: #f4f6f9;
            }
            .stTextInput>div>div>input {
                background-color: #ffffff;
            }
            .title-style {
                font-size: 2.5em;
                font-weight: bold;
                color: #3a3a3a;
                margin-bottom: 0.5em;
            }
            .subtitle-style {
                color: #6c757d;
                font-size: 1.1em;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1 class='title-style'>📅 AI Meeting Scheduler</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle-style'>Schedule meetings effortlessly using natural language powered by Gemini AI.</p>", unsafe_allow_html=True)

query = st.text_area("✍️ Enter your meeting request:",
                    placeholder="e.g. Schedule a meeting with Alice and Bob tomorrow at 3 PM about project launch",
                    height=150)

col1, col2 = st.columns([1, 2])

with col1:
    if st.button("🚀 Schedule Meeting") and query:
        with st.spinner("Processing your request..."):
            result = process_scheduling_query(query)
        if result['status'] == "success":
            st.success(result['message'])
            with st.expander("📄 Meeting Details"):
                st.json(result['meeting'])
        else:
            st.error(result['message'])
            if 'raw' in result:
                st.code(result['raw'], language="json")

with col2:
    with st.expander("📂 View Scheduled Meetings"):
        meetings = get_all_meetings()
        if not meetings:
            st.info("No meetings scheduled.")
        for i, meeting in enumerate(meetings, 1):
            with st.expander(f"#{i}: {meeting['topic']}"):
                st.markdown(f"**📅 Date:** {meeting['date']}")
                st.markdown(f"**⏰ Time:** {meeting['time']}")
                st.markdown(f"**👥 Attendees:** {', '.join(meeting['attendees'])}")
                st.markdown(f"**📌 Status:** {meeting['status']}")
                st.markdown(f"**🕓 Created At:** {meeting['created_at']}")