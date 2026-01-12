from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

# Simple one-line prompt
prompt = PromptTemplate.from_template("{question}")
from langchain_groq import ChatGroq
import os

llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API"),
    model="llama-3.3-70b-versatile"
)
parser = StrOutputParser()

# Chain: prompt → model → parser
chain = prompt | llm | parser

# Run it
result = chain.invoke({"question": "What is the capital of Peru?"})
print(result)