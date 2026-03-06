from dotenv import load_dotenv  # Load API key
import streamlit as st  # Frontend library
import google.generativeai as genai  # Google AI model
import os
import sqlite3
import pandas as pd  # For constructing DataFrame

# Load environment variables
load_dotenv()

# Configure API key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    st.error("API Key is missing! Please set GOOGLE_API_KEY in your .env file.")
    st.stop()

genai.configure(api_key=GOOGLE_API_KEY)

# Function to get Gemini response (SQL generation)
def get_gemini_response(prompt, question):
    cleaned_question = question.lstrip("🔍 ").strip()
    print(f"Cleaned Question: {cleaned_question}")

    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt[0], cleaned_question])
    
    # Ensure query is clean
    query = response.text.strip().strip("```sql").strip("```")
    print(f"Generated SQL Query: {query}")
    
    return query

# Function to connect to database and execute query
def hit_query_db(query, db="student.db"):
    try:
        connection = sqlite3.connect(db)
        cursor = connection.cursor()
        cursor.execute(query)
        
        # Fetch column names
        columns = [desc[0] for desc in cursor.description] if cursor.description else []
        data = cursor.fetchall()
        
        connection.commit()
        connection.close()

        return (columns, data) if data else (columns, "No results found")
    
    except Exception as e:
        return None, f"Error: {str(e)}"

# Prompt for the Gemini model
prompt = ["""
You are an expert in converting English questions to SQL queries! 
The SQL database is called 'student' and has the following tables:

1. **student table**:
   - student_id (Primary Key)
   - Name, Class, Section, Age, Gender, EnrollmentDate, Address, Email, Phone
   - Grade, GPA

2. **marks table**:
   - mark_id (Primary Key)
   - student_id (Foreign Key)
   - Subject, Marks

3. **student_documents table**:
   - doc_id (Primary Key)
   - student_id (Foreign Key)
   - Photo, TenthMarksheet, TwelfthMarksheet, GraduationMarksheet, DocumentStatus

4. **attendance table**:
   - attendance_id (Primary Key)
   - student_id (Foreign Key)
   - TotalDays, PresentDays, AttendancePercentage, AttendanceStatus

5. **student_fees table**:
   - fee_id (Primary Key)
   - student_id (Foreign Key)
   - TotalFees, FeesPaid, FeesDue

6. **library table**:
   - issue_id (Primary Key)
   - student_id (Foreign Key)
   - BookTitle, IssueDate, ReturnDate

**Examples of converting questions to SQL**:
- How many students are in MBA class?  
  → `SELECT COUNT(*) FROM student WHERE Class='MBA';`

- What are the details of students in Section A?  
  → `SELECT * FROM student WHERE Section='A';`

- Show students who scored more than 80 in Math  
  → `SELECT s.Name, m.Subject, m.Marks FROM student s JOIN marks m ON s.student_id = m.student_id WHERE m.Subject='Math' AND m.Marks > 80;`

- What is the attendance percentage of Geeta?  
  → `SELECT AttendancePercentage FROM attendance WHERE student_id = (SELECT student_id FROM student WHERE Name='Geeta');`

- What is the total fee due for MCA students?  
  → `SELECT s.Name, f.FeesDue FROM student s JOIN student_fees f ON s.student_id = f.student_id WHERE s.Class='MCA';`

**Note:** 
- Ignore the "🔍" icon when processing user input.
- Do **not** include triple quotes (`'''`) or unnecessary words like "SQL" in the query output.
"""]

# Streamlit UI setup
st.title("📊 QueryBOT - AI-Powered SQL Generator")
question = st.text_input("Ask your question:", value="🔍 ")
submit = st.button("Search")

# Handle button click and generate SQL query
if submit:
    if not question.strip():
        st.warning("Please enter a valid question! ⚠")
    else:
        query = get_gemini_response(prompt, question)

        # Display generated SQL query
        st.subheader("Generated SQL Query:")
        st.code(query, language="sql")

        # Validate query
        if not query or "-" in query:
            st.warning("Invalid query generated. Try rephrasing your question.")
        else:
            columns, data = hit_query_db(query)

            # Display results
            if isinstance(data, str) and "Error" in data:
                st.error(data)
            elif data == "No results found":
                st.subheader("No results found.")
            else:
                st.subheader("Query Results:")
                st.dataframe(pd.DataFrame(data, columns=columns))
