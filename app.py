import streamlit as st
from datetime import datetime
from src.database.database import read_db
import time
from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from src.utils.custom_tools import custom_query_pasien
from src.interface.prompt import *
from dotenv import load_dotenv
import os
import uuid
from audio_recorder_streamlit import audio_recorder
from src.speech.tts import text_to_speech_response, autoplay_audio
from src.speech.stt import transcribe_audio

# Ensure necessary folders exist
os.makedirs('suara', exist_ok=True)
os.makedirs('bot_responses', exist_ok=True)

# Set page configuration
st.set_page_config(
    page_title="Nana AI-APPS",
    page_icon="🌙",
    layout="wide"
)

# Custom CSS and JavaScript for autoplay
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
    </style>
    <script>
        function autoPlayAudio(audioId) {
            const audio = document.getElementById(audioId);
            if (audio) {
                audio.play();
            }
        }
    </script>
""", unsafe_allow_html=True)

# Initial message
initial_message = {
    "role": "assistant",
    "content": "Hello, my name is NANA (Nurturing AI Nurse Assistant) and I am your personal healthcare assistant.",
    "timestamp": datetime.now().strftime('%I:%M %p'),
    "audio_path": None
}

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = [initial_message]
if 'conversation_memory' not in st.session_state:
    st.session_state.conversation_memory = ""

# Display chat history
for message in st.session_state.messages:
    role = message["role"]
    content = message["content"]
    timestamp = message["timestamp"]
    audio_path = message.get("audio_path")
    
    with st.chat_message(role):
        st.markdown(f"{timestamp} - {content}")
        if audio_path and os.path.exists(audio_path):
            st.audio(audio_path, format='audio/mp3')

def initialize_openai():
    return ChatOpenAI(
        model="gpt-4o",
        temperature=0.2
    )

def create_sql_connection(llm):
    db = read_db()
    tools = SQLDatabaseToolkit(db=db, llm=llm)
    return tools

def create_agent(toolkit, llm):
    custom_tools_pasien = custom_query_pasien()
    custom_tools = custom_tools_pasien
    return create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        extra_tools=custom_tools,
        prefix=prefix_template,
        agent_type="openai-tools",
        format_instructions=format_instructions_template,
        verbose=True
    )

# Initialize components
load_dotenv()
llm = initialize_openai()
sql_toolkit = create_sql_connection(llm)
agent_executor = create_agent(sql_toolkit, llm)

# Sidebar for input methods
with st.sidebar:
    st.title('Your AI Appointments Assistant')
    
    st.subheader("Voice Input")
    audio_value = audio_recorder("Press to talk:", icon_size="3x", neutral_color="#6ca395", )
    prompt = None
    
    if audio_value:
        # st.audio(audio_value)
        unique_filename = f"suara/audio_{uuid.uuid4()}.wav"
        
        try:
            with open(unique_filename, "wb") as f:
                f.write(audio_value)
            
            prompt = transcribe_audio(unique_filename)
            st.write(f"Transcribed text: {prompt}")
        except Exception as e:
            st.error(f"Error processing audio: {e}")

# Text input
text_prompt = st.chat_input("Type your message here...")

# Determine the input prompt
if prompt:
    input_prompt = prompt
elif text_prompt:
    input_prompt = text_prompt
else:
    input_prompt = None

# Process the input
if input_prompt:
    current_time = datetime.now().strftime("%I:%M %p")
    
    # Add user message
    st.session_state.messages.append({
        "role": "user", 
        "content": input_prompt,
        "timestamp": current_time,
        "audio_path": None
    })

    with st.chat_message("user"):
        st.markdown(f"{current_time} - {input_prompt}", unsafe_allow_html=True)

    with st.chat_message("assistant"):
        with st.spinner("I'm on it, please wait..."):
            st.session_state.conversation_memory = "\n".join(
                f"{msg['role'].capitalize()}: {msg['content']}" for msg in st.session_state.messages)
            
            full_input = f"{st.session_state.conversation_memory}\nAssistant:"
            response = agent_executor.invoke({"input": full_input})
            response_text = response['output']

            # Generate audio response
            audio_path = text_to_speech_response(response_text)

        response_timestamp = datetime.now().strftime("%I:%M %p")
        placeholder = st.empty()
        displayed_text = f"{response_timestamp} - "

        # Animated text display
        for char in response_text:
            displayed_text += char
            placeholder.markdown(displayed_text, unsafe_allow_html=True)
            time.sleep(0.01)

        # Display and autoplay audio
        if audio_path:
            st.markdown(autoplay_audio(audio_path), unsafe_allow_html=True)

        # Add assistant message with audio path
        st.session_state.messages.append({
            "role": "assistant",
            "content": response_text,
            "timestamp": response_timestamp,
            "audio_path": audio_path
        })