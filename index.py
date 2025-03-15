# from dotenv import load_dotenv
import streamlit as st
import os
import sqlite3
import pandas as pd
import google.generativeai as genai

# Load environment variables
# load_dotenv()

# Configure Gemini AI key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Dummy data for UI demo
data = {
    
    "Name": ["Krishna", "Sudanshu", "Virat", "Vikram", "Dipesh"],
    "Class": ["Data Science", "Data Science", "Computer Science", "Computer Science", "Information Security"],
    "Section": ["A", "B", "A", "A", "B"],
    "Marks": [90, 100, 86, 50, 35]
}
df = pd.DataFrame(data)

# Function to load Google Gemini model and process queries
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content([prompt[0], question])
    return response.text


# Function to retrieve query results from the database
def read_sql_query(sql,db):
    conn=sqlite3.connect(db)
    cur=conn.cursor()
    cur.execute(sql)
    rows=cur.fetchall()
    conn.commit()
    conn.close()
    for row in rows:
        print(row)
    return rows

# SQL Prompt
prompt = [
    """
    You are an expert in converting English questions to SQL queries!
    The SQL database is named STUDENT with the following columns: NAME, CLASS, SECTION and MARKS

    Example 1 - *How many records are present?*  
    SQL: SELECT COUNT(*) FROM STUDENT;

    Example 2 - *Tell me all students in the Data Science class?*  
    SQL: SELECT * FROM STUDENT WHERE CLASS="Data Science";

    Ensure your SQL output does not include ``` or "sql".
    """
]

# Streamlit App Configuration
st.set_page_config(page_title="NL to SQL Converter", layout="centered")

# Custom Styling for Modern Look
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
        
        .stApp {
            background: linear-gradient(to right, #1F1C2C, #928DAB);
            color: white;
            font-family: 'Orbitron', sans-serif;
        }
        
        .title {
            text-align: center;
            font-size: 80px;
            font-weight: bold;
            color: #FFD700;
            margin-bottom: 10px;
            animation: fadeIn 1.5s ease-in-out;
        }

        .subtitle {
            text-align: left;
            font-size: 15px;
            color: #6CB4EE;
            margin-bottom: 20px;
        }

        .sql-box {
            background: rgba(0, 0, 0, 0.6);
            padding: 15px;
            border-radius: 10px;
            margin-top: 10px;
            font-size: 18px;
            font-weight: bold;
            color: #FFD700;
            text-align: center;
            animation: fadeIn 1.5s ease-in-out;
        }

        .example-text {
            font-style: italic;
            color: #FFD700;
            font-size: 16px;
            text-align: left;
            margin-top: -10px;
            margin-bottom: 1px;
        }

        .stButton>button {
            background-color: #FF5733;
            color: white;
            padding: 12px 25px;
            font-size: 18px;
            border-radius: 10px;
            transition: 0.3s;
            font-family: 'Orbitron', sans-serif;
        }

        .stButton>button:hover {
            background-color: #FFC300;
            transform: scale(1.05);
        }

        @keyframes fadeIn {
            0% { opacity: 0; transform: translateY(-10px); }
            100% { opacity: 1; transform: translateY(0); }
        }
    </style>
""", unsafe_allow_html=True)

# App Header
st.markdown('<p class="title">Gemini-powered SQL Query Generator - QuerryBuddy</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Easily Convert Natural Language into SQL Queries!</p>', unsafe_allow_html=True)

# **📊 Demo Database Display**
st.markdown("### 📊 Sample Database")
st.dataframe(df.style.set_properties(**{'text-align': 'center'}))
st.markdown("</div>", unsafe_allow_html=True)

# **💬 User Query Input Section**
st.markdown("### 💬 Ask Any Question About the Database:")
st.markdown('<p class="example-text">*Example: "How many students are in the database?"*</p>', unsafe_allow_html=True)

question = st.text_input("", key="input", placeholder="Type your query here...")
submit = st.button("🔍 Generate SQL & Fetch Data")
st.markdown("</div>", unsafe_allow_html=True)

# **Processing User Input**
if submit:
    if question.strip() == "":
        st.warning("⚠️ Please enter a question before submitting.")
    else:
        sql_query = get_gemini_response(question, prompt)
        st.markdown(f'<div class="sql-box">📝 {sql_query}</div>', unsafe_allow_html=True)
        
        # Execute SQL and display results
        response = read_sql_query(sql_query, "student.db")
       
        if response:
            st.success("✅ Query Executed Successfully!")
            for row in response:
                st.header(row)
        else:
            st.error("❌ No matching records found.")
