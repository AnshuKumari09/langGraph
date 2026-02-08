import os
from langgraph.graph import StateGraph, START, MessagesState
from langgraph.checkpoint.postgres import PostgresSaver

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize model
from langchain_groq import ChatGroq


llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API"),
    model="llama-3.3-70b-versatile"
)


# Define node
def call_model(state: MessagesState):
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

# Build graph
builder = StateGraph(MessagesState)
builder.add_node("call_model", call_model)
builder.add_edge(START, "call_model")

# Database connection string
DB_URI = "postgresql://postgres:postgres@localhost:5434/llm_memory_db"

# Create checkpointer and run
with PostgresSaver.from_conn_string(DB_URI) as checkpointer:
    # Run ONCE (creates tables)
    checkpointer.setup()
    
    # Compile graph with checkpointer
    graph = builder.compile(checkpointer=checkpointer)
    
    # Thread 1 (remembers context)
    t1 = {"configurable": {"thread_id": "thread-1"}}
    
    # First message
    graph.invoke({"messages": [{"role": "user", "content": "Hi, my name is Nitish"}]}, t1)
    
    # Second message - should remember the name
    out1 = graph.invoke({"messages": [{"role": "user", "content": "What is my name?"}]}, t1)
    
    print(out1["messages"][-1].content)
