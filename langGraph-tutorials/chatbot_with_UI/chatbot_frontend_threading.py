
import streamlit as st
from langgraph_backend import chatbot
from langchain_core.messages import HumanMessage
import uuid

#***************************** utility functions **************************************
# def generate_thread_id():
#     thread_id=uuid.uuid4()
#     return thread_id


def generate_thread_id():
    return str(uuid.uuid4())
def reset_chat():
    new_id = generate_thread_id()
    st.session_state['thread_id']=new_id
    st.session_state['chat_threads'].append(new_id)
    st.session_state['message_history'] = []

def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

def get_config():
    return {'configurable': {'thread_id': st.session_state['thread_id']}}


#**************************** session Setup *****************************************

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state: # Agar "thread_id" memory me nahi haiTo ab bana do
    st.session_state['thread_id']=generate_thread_id()

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads']=[]

add_thread(st.session_state['thread_id'])

#************************************ sidebar ui ****************************************
st.sidebar.title('langGraph ChatBot')
if st.sidebar.button('New Chat'):
    reset_chat()
    st.rerun() 
st.sidebar.header('Conversations')

for thread_id in st.session_state['chat_threads']:
    st.sidebar.text(thread_id)

# loading the conversation history
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

#{'role': 'user', 'content': 'Hi'}
#{'role': 'assistant', 'content': 'Hi=ello'}

user_input = st.chat_input('Type here')

if user_input:

    # first add the message to message_history
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.text(user_input)

    # first add the message to message_history
    with st.chat_message('assistant'):

        ai_message = st.write_stream(
            message_chunk.content for message_chunk, metadata in chatbot.stream(
                {'messages': [HumanMessage(content=user_input)]},
                config= get_config(),
                stream_mode= 'messages'
            )
        )

    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})

#Session State = Streamlit ki memory