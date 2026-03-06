# QueryBOT – AI Powered SQL Generator

QueryBOT is an AI-powered application that converts natural language questions into SQL queries using Google Gemini AI and executes them on a SQLite student database.

## Features
- Convert English questions to SQL queries
- AI powered using Gemini
- Executes queries on SQLite database
- Displays results using Pandas DataFrame
- Built using Streamlit

## Technologies Used
- Python
- Streamlit
- Google Gemini API
- SQLite
- Pandas

## How to Run

1. Install dependencies  
pip install -r requirements.txt

2. Add API key in `.env`  
GOOGLE_API_KEY=your_api_key

3. Run the app  
streamlit run app.py

## Example Questions
- How many students are in MBA class?
- Show students in Section A
- Students scoring more than 80 in Math

## Author
Minal Patil