from langchain.chains.summarize import load_summarize_chain
# from langchain_community.document_loaders import WebBaseLoader
from langchain.llms import OpenAI
# from langchain_community.document_loaders import JSONLoader
# from langchain_core.documents import Document
from langchain_community.document_loaders import TextLoader

pth1 = r"C:\home\ananth\research\my_projects\adobe_doc_cloud_june_2024\session4_rag\apqr_table_3.json"
pth2 = r"C:\home\ananth\research\my_projects\adobe_doc_cloud_june_2024\session4_rag\apqr_table_4.json"

import json
from pathlib import Path
from pprint import pprint

loader = TextLoader(pth2)
docs = loader.load()

data = json.loads(Path(pth1).read_text())
pprint(data)

llm = OpenAI(temperature=0, base_url="http://localhost:1234/v1", api_key="lm_studio")
chain = load_summarize_chain(llm, chain_type="stuff")

result = chain.invoke(docs)

print(result["output_text"])
