import streamlit as st
from datetime import datetime
from openai import OpenAI

st.title("Jarvis 🤖🔗 - Learning to create GPT like app")

# Add to your existing Streamlit script

st.markdown("""
## Use Case Example: Gaining Insights on Diverse Topics

**Background**: Alex is a curious individual with a wide range of interests, from history and science to cooking and gardening. While Alex enjoys learning, he often finds it time-consuming to search for and digest large amounts of information on different topics.

**Use Case**: Alex discovers the Jarvis 🤖🔗 Chat application (based on GPT-3), which can provide concise answers and explanations on a variety of topics. He starts by asking, "What is the history of the Roman Empire?" After reviewing the summary, he moves on to different questions like "How does photosynthesis work?" and "What are some easy recipes for homemade bread?"

**Outcome**: Using Jarvis, Alex can quickly obtain clear and concise information on all his questions. This saves him time and makes learning new topics an enjoyable and efficient process. He now uses Jarvis as his go-to tool for satisfying his curiosity and expanding his knowledge base.

Feel free to ask any questions you might have, whether they're about historical events, scientific concepts, cooking tips, or anything else you're curious about.
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
