# import os
# from typing import List, Dict
# import google.generativeai as genai
# from dotenv import load_dotenv
# import json
# from datetime import datetime
# from pathlib import Path
# # Load environment variables
# load_dotenv()

# # Configure API key
# GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
# if not GOOGLE_API_KEY:
#     raise ValueError("Please set the GOOGLE_API_KEY in .env file")

# # Configure Gemini API
# genai.configure(api_key=GOOGLE_API_KEY)


# # Add these constants after imports
# DATA_DIR = Path.home() / "Desktop/ML-main/ML/meeting_data"
# MEETINGS_FILE = DATA_DIR / "meetings.json"

# def save_meeting(meeting_data: Dict) -> bool:
#     """Save meeting data to local storage"""
#     try:
#         # Create data directory if it doesn't exist
#         DATA_DIR.mkdir(parents=True, exist_ok=True)
        
#         # Load existing meetings
#         existing_meetings = []
#         if MEETINGS_FILE.exists():
#             with open(MEETINGS_FILE, 'r') as f:
#                 existing_meetings = json.load(f)
        
#         # Add new meeting
#         existing_meetings.append(meeting_data)
        
#         # Save updated meetings
#         with open(MEETINGS_FILE, 'w') as f:
#             json.dump(existing_meetings, f, indent=2)
#         return True
#     except Exception as e:
#         print(f"Error saving meeting: {str(e)}")
#         return False
# def format_meeting_display(meeting: Dict) -> str:
#     """Format a meeting for display"""
#     return (f"Topic: {meeting['topic']}\n"
#             f"Date: {meeting['date']} at {meeting['time']}\n"
#             f"Attendees: {', '.join(meeting['attendees'])}\n"
#             f"Status: {meeting['status']}\n"
#             f"Created: {meeting['created_at']}\n")

# # Add this right after get_all_meetings function
# def display_meetings(meetings: List[Dict]) -> None:
#     """Display all meetings in a formatted way"""
#     if not meetings:
#         print("\nNo meetings scheduled.")
#         return
        
#     print("\n=== Scheduled Meetings ===")
#     for i, meeting in enumerate(meetings, 1):
#         print(f"\nMeeting #{i}")
#         print(format_meeting_display(meeting))
#     print("=======================")


# def get_all_meetings() -> List[Dict]:
#     """Retrieve all saved meetings"""
#     try:
#         if not MEETINGS_FILE.exists():
#             return []
            
#         with open(MEETINGS_FILE, 'r') as f:
#             meetings = json.load(f)
#         return meetings
        
#     except Exception as e:
#         print(f"Error loading meetings: {str(e)}")
#         return []

# def schedule_meeting(attendees: List[str], date: str, time: str, topic: str) -> Dict:
#     """
#     Schedule a meeting with the given parameters.
#     """
#     try:
#         # In a real application, this would interface with a calendar API
#         meeting = {
#             "attendees": attendees,
#             "date": date,
#             "time": time,
#             "topic": topic,
#             "status": "scheduled",
#             "created_at": datetime.now().isoformat()
#         }
#         return meeting
#     except Exception as e:
#         return {"error": f"Failed to schedule meeting: {str(e)}"}

# def process_scheduling_query(query: str) -> str:
#     """Process meeting scheduling query using Gemini function calling"""
    
#     try:
#         # Initialize Gemini model
#         model = genai.GenerativeModel('gemini-2.0-flash')  
        
#         # Improved prompt with better structure and examples
#         analysis_prompt = """
#         Extract meeting details from the following query and format as JSON.
        
#         Rules:
#         - Convert relative dates (tomorrow, next Monday) to YYYY-MM-DD format
#         - Convert time to 24-hour format (HH:MM)
#         - Include all mentioned attendees
#         - Extract or infer meeting topic
        
#         Example Input: "Schedule a meeting with Bob tomorrow at 2 PM about project review"
#         Example Output: {
#             "attendees": ["Bob"],
#             "date": "2024-05-26",
#             "time": "14:00",
#             "topic": "project review"
#         }
        
#         Current Query: """ + query
        
#        # Get structured data from Gemini
#         analysis = model.generate_content(analysis_prompt)
#         print("Debug - Model Response:", analysis.text)  
        
#         try:
#             # Clean the response text
#             response_text = analysis.text.strip()
#             if "```" in response_text:
#                 # Extract content between markdown tags if present
#                 json_content = response_text.split("```")[1]
#                 if json_content.startswith("json\n"):
#                     json_content = json_content[5:]
#             else:
#                 json_content = response_text
            
#             # Parse the cleaned JSON
#             meeting_params = json.loads(json_content.strip())
            
#             # Schedule meeting with extracted parameters
#             meeting_data = schedule_meeting(**meeting_params)
#              # Save the meeting and return response
#             if save_meeting(meeting_data):
#                 print("\nMeeting saved successfully!")
#                 return json.dumps({
#                     "status": "success",
#                     "message": f"Meeting scheduled successfully for {meeting_data['date']} at {meeting_data['time']}",
#                     "meeting_details": meeting_data
#                 }, indent=2)
#             else:
#                 return json.dumps({
#                     "status": "error",
#                     "message": "Failed to save meeting"
#                 }, indent=2)
            
            
#         except json.JSONDecodeError as e:
#             return json.dumps({
#                 "status": "error",
#                 "message": f"JSON parsing error: {str(e)}",
#                 "raw_response": analysis.text
#             }, indent=2)
    
#     except Exception as e:
#         return json.dumps({
#             "status": "error",
#             "message": f"Error: {str(e)}"
#         }, indent=2)

# def main():
#     print("Meeting Scheduler (Type 'quit' to exit and Type 'show' to view all meetings)")
#     print("Example queries:")
#     print("- Schedule a meeting with Bob and Alice tomorrow at 2 PM about project planning")
#     print("- Set up a team meeting on 2024-06-15 at 10:00 AM to discuss Q3 goals")
#     print("- Arrange a meeting with the development team next Monday at 3 PM\n")
    
#     while True:
#         query = input("\nEnter your scheduling request or command: ")
        
#         if query.lower() == 'quit':
#             break
#         elif query.lower() == 'show':
#             meetings = get_all_meetings()
#             if meetings:
#                 print("\nAll Scheduled Meetings:")
#                 for i, meeting in enumerate(meetings, 1):
#                     print(f"\nMeeting #{i}")
#                     print(format_meeting_display(meeting))
#             else:
#                 print("\nNo meetings scheduled yet.")
#             continue
        
#         response = process_scheduling_query(query)
#         print("\nResponse:")
#         print(response)  
# if __name__ == "__main__":
#     main()


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
st.set_page_config(page_title="Meeting Scheduler", layout="centered")
st.title("📅 AI Meeting Scheduler")

st.markdown("Enter your meeting request in natural language. Example:")
st.code("Schedule a meeting with Alice tomorrow at 3 PM about product launch")

query = st.text_area("Meeting Request:")
if st.button("Schedule Meeting") and query:
    with st.spinner("Processing your request..."):
        result = process_scheduling_query(query)
    if result['status'] == "success":
        st.success(result['message'])
        st.json(result['meeting'])
    else:
        st.error(result['message'])
        if 'raw' in result:
            st.text(result['raw'])

st.markdown("---")

if st.checkbox("📂 Show All Scheduled Meetings"):
    meetings = get_all_meetings()
    if not meetings:
        st.info("No meetings scheduled.")
    for i, meeting in enumerate(meetings, 1):
        with st.expander(f"Meeting #{i}: {meeting['topic']}"):
            st.write(f"**Date:** {meeting['date']}")
            st.write(f"**Time:** {meeting['time']}")
            st.write(f"**Attendees:** {', '.join(meeting['attendees'])}")
            st.write(f"**Status:** {meeting['status']}")
            st.write(f"**Created:** {meeting['created_at']}")
