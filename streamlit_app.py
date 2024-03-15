import streamlit as st
from datetime import datetime
from openai import OpenAI

st.title("Jarvis 🤖🔗 Chat")

# Add to your existing Streamlit script

st.markdown("""
## Use Case Example: Learning to Create GPT-like Applications

**Background**: Emily, a software developer, is interested in developing her own GPT-like applications. She has basic knowledge of AI and coding but wants to understand the practical aspects of integrating AI models into applications.

**Use Case**: Emily uses the Jarvis 🤖🔗 Chat application to learn more about this topic. She starts by asking, "What are the key components of a GPT-like application?" After receiving an overview, she dives deeper by asking, "How can I integrate a GPT model into a web application?"

**Outcome**: Through the conversation with Jarvis, Emily gains insights into the architecture of GPT-like applications, including the frontend interface, API layer, and model hosting. She also learns about different tools and libraries she can use for her project. Empowered with this knowledge, Emily feels more confident in starting her own project and exploring further.

Please feel free to ask any questions related to creating GPT-like applications or any general inquiries you might have.
""", unsafe_allow_html=True)

# Set OpenAI API key from Streamlit secrets
# .streamlit/secrets.toml

# Set OpenAI API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# Initialize chat history
if "messages" not in st.session_state:
    # Start with an introduction message from Jarvis
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.messages = [{"role": "assistant", "content": f"Hello, I am Jarvis 🤖 and today's is {current_time}.\nHow can I assist you today?"}]
    
# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

# Display assistant response in chat message container
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
