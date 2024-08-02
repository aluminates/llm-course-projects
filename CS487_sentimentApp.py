from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama
import streamlit as st

st.set_page_config (
    page_title="Sentiment Analyzer",
    layout="wide",
)

template = """You are a sentiment analyzer. Look at the statement below and provide the sentiment behind it:
Statement: {statement}"""

model = Ollama(model="llama3.1")

def generate_response(input_text):
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model
    response = chain.invoke({"statement":input_text})
    st.info(response)

with st.form("my_form"):
    text = st.text_area(
        "Enter text:"
    )
    submitted = st.form_submit_button("Submit")
    if submitted:
        generate_response(text)