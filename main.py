import streamlit as st
from st_pages import Page, show_pages
import streamlit.components.v1 as components
import json
import openai
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from sqlalchemy.exc import ProgrammingError
import pandas as pd

db_name = st.session_state.get("db_name", "Not Set")
selected_model = st.session_state.get("selected_model", "Not Set")
model_provider = st.session_state.get("model_provider", "Not Set")
key = st.session_state.get("key", "Not Set")
temperature = st.session_state.get("temperature", "Not Set")
top_p = st.session_state.get("top_p", "Not Set")
max_tokens = st.session_state.get("max_tokens", "Not Set")
presence_penalty = st.session_state.get("presence_penalty", "Not Set")
frequency_penalty = st.session_state.get("frequency_penalty", "Not Set")
selected_model = st.session_state.get("selected_model", "Not Set")
schema_details_json = st.session_state.get("schema_details_json", "Not Set")
connection_str = st.session_state.get("connection_str", "Not Set")
db_type = st.session_state.get("db_type", "Not Set")

openai.api_key = key

# Add a robot emoji icon and set the tab name
st.set_page_config(page_title="MOWZE", page_icon="🤖")

st.subheader("MOWZE - AI-Powered Database Chatbot")

with st.sidebar:
    show_pages([
        Page("main.py", "Chatbot"),
        Page("database_connection.py", "Database Connection"),
        Page("model_settings.py", "Language Model Settings"),
        Page("about_contact.py", "About & Contact"),
    ])
    
    # Displaying the database and model information
    st.markdown("#### **Database Information**")
    st.write(f"Connected to: **{db_name}**")
    
    st.markdown("#### **Language Model**")
    st.write(f"Using: **{selected_model}**")
    
    with st.expander('Model Details'):
        st.markdown("#### **model_provider:**")
        st.write(f"{model_provider}")

        st.markdown("#### **temperature:**")
        st.write(f"{temperature}")

        st.markdown("#### **top_p:**")
        st.write(f"{top_p}")

        st.markdown("#### **max_tokens:**")
        st.write(f"{max_tokens}")

        st.markdown("#### **presence_penalty:**")
        st.write(f"{presence_penalty}")

        st.markdown("#### **frequency_penalty:**")
        st.write(f"{frequency_penalty}")
   
    def clear_chat_history():
        st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
    st.sidebar.button('Clear Chat History', on_click=clear_chat_history, use_container_width=True) 

with st.expander("How to Use the Chatbot Assistant", expanded=False):
    st.markdown("""
    **Welcome to the Chatbot Assistant!** Here's a quick guide:

    1. **Database Connection**: 
        - Visit the `Database Connection` tab.
        - Connect with a sample database or use yours.
        - Fill in the details and hit `connect`.

    2. **Language Model Settings**: 
        - Go to `Language Model Settings` tab.
        - Select a model or customize one.
        - Press `save` when done.

    3. **Chat with the Bot**: 
        - Switch to the `Chatbot` tab.
        - Type your questions and get real-time responses.

    4. **Reset Chat**: 
        - Use `Clear Chat History` in the sidebar for a fresh start.

    5. **About & Contact**: 
        - Know more about this bot in the `About & Contact` tab.

    Dive in and enjoy the experience! 🚀📊
    """)
    
# Function for generating LLM response
def generate_response(prompt_input):
    try:
        # If configurations are not set, provide appropriate feedback
        if connection_str == "Not Set" and selected_model == "Not Set":
            return "Please set up your database connection and select a model before proceeding."
        elif connection_str == "Not Set":
            return "Please set up your database connection before proceeding."
        elif selected_model == "Not Set":
            return "Please select a model before proceeding."
        else:
            if not generate_response:
                return 'Error:', 'Please enter a request'

            if db_type == 'Sample DatabaseOnly':
                db_dialect = 'Postgres'
            else:
                db_dialect = db_type

            prompt = "You are an SQL assistant."
            prompt += f"\n\n Based on the provided database schema, recent user interactions and the current request, construct SQL query that extracts the information."
            prompt += f"\n\n User request is: {prompt_input}."
            prompt += "\n\nOnly craft the SQL code without any comments or explanations."
            prompt += "ALWAYS reference columns using their respective table names to avoid ambiguity."
            prompt += f"\n\nAdhere to the SQL dialect: {db_type}"
            prompt += f"\n\nOnly utilize columns and tables from the provided schema below: {schema_details_json}"

            response = openai.ChatCompletion.create(model=selected_model,
                                                   temperature=temperature,
                                                   messages=[{"role": "user", "content": prompt}])

            code = response.choices[0].message.content

            with st.sidebar:
                st.markdown('**Generated SQL Query**')
                st.code(code, language='sql')

            engine = create_engine(connection_str)
            with engine.connect() as conn, conn.begin():
                result = conn.execute(text(code))
                data = pd.DataFrame(result.fetchall(), columns=result.keys())
                st.write(data)

            second_prompt = "You are an SQL assistant."
            second_prompt += f"\n\n User question was {prompt_input}."
            second_prompt += f"\n\n You have executed this code {code}."
            second_prompt += f"\n\n It has returned that dataframe output: {data.to_string()}."
            second_prompt += f"Please answer the User question based on the output data."

            response = openai.ChatCompletion.create(model=selected_model,
                                                    temperature=temperature,
                                                    messages=[{"role": "user", "content": second_prompt}])

            answer = response.choices[0].message.content

            return answer

    except ProgrammingError as e:
        error_message = "There was an issue executing the query. Please check your question and try again."
        #st.write(f"Error: {error_message}")
        return error_message

# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I help you?"}]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User-provided prompt
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = generate_response(prompt) 
            st.write(response) 
    message = {"role": "assistant", "content": response}
    st.session_state.messages.append(message)
        
