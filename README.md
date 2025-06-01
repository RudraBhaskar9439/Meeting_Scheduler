
# Meeting Scheduler with Gemini AI
A smart meeting scheduling system powered by Google's Gemini AI that understands natural language requests and manages meeting data locally.

# 🎯 Features

🗣️ Natural language meeting scheduling

📅 Automatic date and time parsing

👥 Multiple attendee support

💾 Local storage for meeting data

📋 Meeting list viewing and management

🤖 AI-powered request interpretation


# 📋 Prerequisites

Python 3.8+

Google Gemini API key



# 🛠️ Installation
## 1. Clone the repository
```python
git clone <your-repo-url>
cd <your-repo-directory>
```
## 2. Install required packages
```python
pip3 install google-generativeai python-dotenv
```
## 3. Create environment file:
```python
# Create .env file
echo "GOOGLE_API_KEY=your_gemini_api_key_here" > .env

# Create meeting data directory
mkdir -p ~/Desktop/ML-main/ML/meeting_data
```


# 📁 Project Structure
```python
.
├── scheduleMeeting.py     # Main application file
├── meeting_data/         # Directory for meeting storage
│   └── meetings.json    # Meeting database
├── .env                 # Environment variables
└── README.md            # Documentation
```

# 💻 Usage
1. Run the script:
```python
python3 scheduleMeeting.py
```


2. Example Commands:

```python
- Schedule a meeting with Bob and Alice tomorrow at 2 PM about project planning
- Set up a team meeting on 2024-06-15 at 10:00 AM to discuss Q3 goals
- show (displays all scheduled meetings)
- quit (exits the program)
```

## 🔍 Features in Detail

Natural Language Processing

Understands relative dates (tomorrow, next Monday)

Converts times to 24-hour format

Extracts attendee lists automatically

Infers meeting topics from context

## Meeting Management

Saves meetings locally in JSON format

Displays formatted meeting lists

Maintains creation timestamps

Tracks meeting status



# 🔒 Security

API key management through environment variables

Input validation for file access

Error handling for API operations


# 🤝 Contributing

Fork the repository

Create your feature branch (git checkout -b feature/AmazingFeature)

Commit your changes (git commit -m 'Add some AmazingFeature')

Push to the branch (git push origin feature/AmazingFeature)

Open a Pull Request

# MIT License

Copyright (c) 2024 [Rudra Bhaskar]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Security Note
⚠️ Never commit your .env file or expose your API keys.

Author
[Rudra Bhaskar]