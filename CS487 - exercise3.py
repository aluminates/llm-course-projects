import pandas as pd
import sqlite3
import streamlit as st
import requests
import json
import os

st.set_page_config(
    page_title="Poll Analyzer"
)

def preprocess_data():
    df = pd.read_csv('C:/Users/Ria/OneDrive/Desktop/PESU/UE21CS326C - Large Language Models/Day 2/file34.csv')
    df = df.dropna() # columns renamed manually
    return df

# creating an sqlite database
def create_database(df):
    conn = sqlite3.connect('elections.db')
    df.to_sql('elections_2019', conn, if_exists='replace', index=False)
    conn.close()

# creating a cursor to query
def execute_sql(query):
    conn = sqlite3.connect('elections.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        column_names = [description[0] for description in cursor.description]
        conn.close()
        return results, column_names
    except sqlite3.Error as e:
        conn.close()
        raise e

# added validation function to prevent data manipulation
def validate_sql(query):
    dangerous_keywords = ['DROP', 'DELETE', 'TRUNCATE', 'UPDATE', 'INSERT']
    return not any(keyword in query.upper() for keyword in dangerous_keywords)

# here i am generating SQL query from NL text
def generate_sql(question):
    url = "http://localhost:1234/v1/chat/completions"
    headers = {"Content-Type": "application/json"}
    data = {
        "messages": [
            {"role": "system", "content": "You are a SQL expert. Generate only the SQL query without any explanation."},
            {"role": "user", "content": f"""
            Given the following database schema:
            Table: elections_2019
            Columns: state_name, constituency_number, constituency_name, assembly_constituency_number, assembly_constituency_name, total_voters, total_votes_in_state, nota_votes, candidate_name, party_name, secured_votes

            Generate a SQL query to answer the following question:
            {question}
            """}
        ],
        "temperature": 0,
        "max_tokens": 150,
        "stream": False
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content'].strip()
    else:
        raise Exception(f"Error generating SQL: {response.text}")

# 6. Post-process results
def format_results(results, column_names, question):
    url = "http://localhost:1234/v1/chat/completions"
    headers = {"Content-Type": "application/json"}
    data = {
        "messages": [
            {"role": "system", "content": "You are a data analyst. Summarize the given data concisely."},
            {"role": "user", "content": f"""
            Question: {question}
            Column names: {', '.join(column_names)}
            Results: {results}

            Provide a concise summary of these results in a human-readable format.
            """}
        ],
        "temperature": 0.3,
        "max_tokens": 150,
        "stream": False
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content'].strip()
    else:
        raise Exception(f"Error formatting results: {response.text}")

# UI function
def main():
    st.title("2019 Indian General Elections Poll Analyzer")

    user_input = st.text_input("Ask a question about the 2019 Indian General Elections:")

    if user_input:
        try:
            with st.spinner("Generating SQL query..."):
                sql_query = generate_sql(user_input)
            st.code(sql_query, language='sql')
            
            if validate_sql(sql_query):
                with st.spinner("Executing query..."):
                    results, column_names = execute_sql(sql_query)
                
                with st.spinner("Formatting results..."):
                    formatted_results = format_results(results, column_names, user_input)
                
                st.write(formatted_results)
            else:
                st.error("Invalid SQL query generated. Please try rephrasing your question.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    if not os.path.exists('elections.db'):
        with st.spinner("Initializing database..."):
            df = preprocess_data()
            create_database(df)
    main()