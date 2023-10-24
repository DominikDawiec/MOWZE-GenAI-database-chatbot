# Probelm do zaafresowania #1 - czy wartość maksymalna w max tokens nie powinna być dostarczona do modelu?

import streamlit as st
    
# Model names
models_openai = [
    'gpt-3.5-turbo-16k-0613',
    'gpt-3.5-turbo-0613',
    'gpt-3.5-turbo-instruct',
    'gpt-3.5-turbo-16k',
    'gpt-3.5-turbo',
    'gpt-4-32k-0314 (Legacy)', 
    'gpt-4-0314 (Legacy)', 
    'gpt-4-32k-0613', 
    'gpt-4-32k', 
    'gpt-4-0613', 
    'gpt-4', 
]

st.title("Model Configuration")

model_provider = st.selectbox("Choose a model provider:", ["Sample Model (Recommended)", "OpenAI"])

if model_provider == "Sample Model (Recommended)":
    st.subheader('Sample Model (Recommended)')
    selected_model = 'gpt-3.5-turbo-16k-0613'
    key = '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' #schować w przypadku upublicznienia kodu
    
    with st.expander('Model Parameters'):
        temperature = 0.2
        top_p = 0.8
        max_tokens = 12000
        presence_penalty = 0.0
        frequency_penalty = 0.0
        
        st.write('temperature:',temperature)
        st.write('top_p:',top_p)
        st.write('max_tokens:',max_tokens)
        st.write('presence_penalty:',presence_penalty)
        st.write('frequency_penalty:',frequency_penalty)

elif model_provider == "OpenAI":
    st.subheader('OpenAI Model Selection')
    selected_model = st.selectbox('Select a model:', models_openai)
    key = st.text_input("Enter your OpenAI key:")
    
    with st.expander('Model Parameters'):
        temperature = st.slider("Temperature:", min_value=0.0, max_value=2.0, value=0.2, step=0.05)
        top_p = st.slider("Top P:", min_value=0.0, max_value=1.0, value=0.8, step=0.01)
        max_tokens = st.slider("Max Tokens:", min_value=1, max_value=15000, value=5000)
        presence_penalty = st.slider("Presence Penalty:", min_value=-2.0, max_value=2.0, value=0.0, step=0.05)
        frequency_penalty = st.slider("Frequency Penalty:", min_value=-2.0, max_value=2.0, value=0.0, step=0.05)

#elif model_provider == "Replicate LLM":
#    st.subheader('Replicate LLM Model Selection')
#    selected_model = st.text_input('Select a model:')
#    key = st.text_input("Enter your Replicate key:")
#    
#    with st.expander('Model Parameters'):
#        temperature = st.slider("Temperature:", min_value=0.0, max_value=2.0, value=0.2, step=0.05)
#        top_p = st.slider("Top P:", min_value=0.0, max_value=1.0, value=1.0, step=0.01)
#        max_tokens = st.slider("Max Tokens:", min_value=1, max_value=5000, value=5000)
#        frequency_penalty = st.slider("Presence Penalty:", min_value=-2.0, max_value=2.0, value=0.0, step=0.05)
#        presence_penalty = st.slider("Frequency Penalty:", min_value=-2.0, max_value=2.0, value=0.0, step=0.05)

if st.button("Save", key="save_button", on_click=None, args=None, kwargs=None, use_container_width=True): # make the button wide
    with st.spinner('Saving the data...'):
        st.session_state.model_provider = model_provider
        st.session_state.selected_model = selected_model
        st.session_state.key = key
        st.session_state.temperature = temperature
        st.session_state.top_p = top_p
        st.session_state.max_tokens = max_tokens
        st.session_state.presence_penalty = presence_penalty
        st.session_state.frequency_penalty = frequency_penalty
        st.success('Model Settings saved successfully!')

