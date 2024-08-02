from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema import StrOutputParser
from ingest import DB_CHROMA_PATH
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI

custom_prompt_template = """
You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question concisely.
If you don't know the answer, just say that you don't know.

Question: {question}

Context: {context}

Answer:
"""

def set_custom_prompt():
    prompt = PromptTemplate(template=custom_prompt_template, input_variables=['context', 'question'])
    return prompt

def format_docs(docs):
    context = "\n\n".join([d.page_content for d in docs])
    return {"context": context}

def load_llm_client():
    client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
    return client

def get_retriever():
    embeddings = HuggingFaceEmbeddings(model_name="thenlper/gte-large")
    vectordb = Chroma(persist_directory=DB_CHROMA_PATH, embedding_function=embeddings)
    return vectordb

def qa_bot():
    vectordb = get_retriever()
    retriever = vectordb.as_retriever(search_kwargs={"k": 8})
    llm = load_llm_client()

    chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough(),
         }
        | set_custom_prompt()
        | llm
        | StrOutputParser()
    )

    query = ""
    while query != "quit":
        query = input("Your Query: ")
        output = chain.invoke(query)
        print("-" * 100)
        print(output)

qa_bot()