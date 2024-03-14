import streamlit as st
from openai import OpenAI

st.title("Jarvis 🤖🔗 Chat")

# Set OpenAI API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# Initialize chat history
if "messages" not in st.session_state:
    # Start with an introduction message from Jarvis
    st.session_state.messages = [{"role": "assistant", "content": "Hello, I am Jarvis. How can I assist you today?"}]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Generate assistant's response
    response_messages = [
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state.messages
    ]

    # Ensure the first message from Jarvis sets the context for its personality and capabilities
    if len(response_messages) == 1:  # Only the initial message from Jarvis is present
        response_messages.insert(0, {"role": "system", "content": "You are speaking with Jarvis 🤖, an AI assistant designed to help you."})

    # Call OpenAI API to generate the response
    response = client.chat_completions.create(
        model=st.session_state["openai_model"],
        messages=response_messages
    )

    # Assuming response.choices[0].message.content contains the text response from OpenAI
    # This might need adjustment based on the actual structure of the response object
    assistant_response = response.choices[0].message.content if response.choices else "I'm having trouble understanding that."

    # Display assistant's response
    with st.chat_message("assistant"):
        st.markdown(assistant_response)
    
    # Add assistant's response to chat history
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
