import streamlit as st
from st_pages import Page, show_pages

# Add a robot emoji icon and set the tab name
st.set_page_config(page_title="MOWZE", page_icon="🤖")

with st.sidebar:
    show_pages([
        Page("main.py", "Chatbot"),
        Page("database_connection.py", "Database Connection"),
        Page("model_settings.py", "Language Model Settings"),
        Page("about_contact.py", "About & Contact"),
    ])
    

st.title("About & Contact")

st.subheader("About")
st.write("""
This chatbot offers a unique capability to allow users to ask questions to a connected database in natural language without needing to know the SQL language or its flavors. This simplifies the interaction with data and promotes a more intuitive way to extract insights. 
""")

st.subheader("Author")
st.write("""
Hi there! I'm Dominik Dawiec, Junior Data Scientist at PwC with a strong financial background, specializing in bridging the gap between IT and business. Equipped with a bachelor's and master's degree in Accounting and Controlling, I have honed my skills in financial analysis. My current focus is on developing expertise in machine learning to tackle real-world business challenges. 
    """)

st.subheader("Contact")
st.link_button("LinkedIn", "https://www.linkedin.com/in/dominikdawiec/", use_container_width = True)

st.subheader("See my other projects")
st.link_button("GitHub", "https://github.com/DominikDawiec", use_container_width = True)

st.subheader("Proposed Changes for Future Versions")
st.write("""
- Integrate with custom LLM models or open-source models using Replicate. (medium priority)
- Allow users to choose separate models: one for SQL code generation and another for generating responses. (low priority)
""")
