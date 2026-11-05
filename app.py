
import streamlit as st

from src.agent import ask_legal_agent


# -----------------------------------
# PAGE CONFIGURATION
# -----------------------------------

st.set_page_config(
    page_title="German Legal AI",
    page_icon="⚖️",
    layout="wide"
)


# -----------------------------------
# CUSTOM DESIGN
# -----------------------------------

st.markdown("""
<style>

.stApp {
    background-color: #101827;
    color: #FFFFFF;
}

h1, h2, h3 {
    color: #E5E7EB;
}

.stChatMessage {
    background-color: #1E293B;
    border-radius: 12px;
}

section[data-testid="stSidebar"] {
    background-color: #172033;
}

.stButton button {
    background-color: #6366F1;
    color: white;
    border-radius: 8px;
    border: none;
}

</style>
""", unsafe_allow_html=True)


# -----------------------------------
# SIDEBAR
# -----------------------------------

with st.sidebar:

    st.title("⚖️ German Legal AI")

    st.caption("Your private legal research assistant")

    st.divider()

    st.subheader("Knowledge Base")

    st.write("📚 German legislation")

    st.write("📄 BGB")
    st.write("📄 StGB")
    st.write("📄 StPO")

    st.divider()

    st.subheader("System")

    st.success("Local AI enabled")

    st.caption("Powered by Ollama + ChromaDB")


# -----------------------------------
# MAIN INTERFACE
# -----------------------------------

st.title("German Legal Intelligence")

st.write(
    "Research German law, analyse legal questions "
    "and prepare your defence."
)

st.info(
    "This assistant provides legal research support, "
    "not professional legal representation."
)


# -----------------------------------
# CHAT HISTORY
# -----------------------------------

if "messages" not in st.session_state:

    st.session_state.messages = []


for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# -----------------------------------
# USER INPUT
# -----------------------------------

question = st.chat_input(
    "Ask a question about German law..."
)


if question:

    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):

        st.markdown(question)

    with st.chat_message("assistant"):

        with st.spinner("Analysing German legislation..."):

            try:

                answer = ask_legal_agent(question)

                st.markdown(answer)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

            except Exception as error:

                st.error(f"Error: {error}")
