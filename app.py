import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from agent import process_agent_message, get_first_message, set_llm

set_llm(st.secrets['GOOGLE_API_KEY'])

st.set_page_config(page_title="Assistente de Renegociação", page_icon="🤖")
st.title("🤖 Renê do Banco Confiança")
st.write("Bem-vindo(a) ao seu assistente de renegociação de dívidas. Estou aqui para ajudar!")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "current_client" not in st.session_state:
    st.session_state.current_client = None

def start_streamlit_conversation():
    if not st.session_state.chat_history:
        first_agent_message = get_first_message()
        st.session_state.chat_history.append(AIMessage(content=first_agent_message))

start_streamlit_conversation()

for message in st.session_state.chat_history:
    if isinstance(message, HumanMessage):
        _, col = st.columns([0.5, 0.5])
        with col.chat_message("user"):
            st.markdown(message.content)
    else:
        with st.chat_message("assistant"):
            st.markdown(message.content)

user_input = st.chat_input("Sua mensagem para o assistente:")

if user_input:
    st.session_state.chat_history.append(HumanMessage(content=user_input))

    _, col = st.columns([0.5, 0.5])
    with col.chat_message("user"):
        st.markdown(user_input)

    agent_response, st.session_state.current_client = process_agent_message(
        user_input,
        st.session_state.chat_history,
        st.session_state.current_client
    )

    with st.chat_message("assistant"):
        st.markdown(agent_response)

    st.session_state.chat_history.append(AIMessage(content=agent_response))

if st.button("Reiniciar Conversa"):
    st.session_state.chat_history = []
    st.session_state.current_client = None

    start_streamlit_conversation()
    st.rerun()