import streamlit as st
import json
from openai import OpenAI
from st_chat_message import message

st.markdown(
    """
<style>
    .st-emotion-cache-1fee4w7 {
    flex-direction: row-reverse;
    text-align: right;
    }
</style>
""",
    unsafe_allow_html=True,
)

st.title("Historical Figure Chatbot")
st.write("Ask the chatbot which historical figure you want it to roleplay as: ")

client = OpenAI(
    api_key = st.secrets["OPENAI_API_KEY"]
)

system_prompt = """ 
assume you are a chatbot roleplaying as a specific historical figure that the user has chosen. Please first ask the user what historical figure they want you to roleplay as. Your job is to be as close as possible to the personality of that historical figure. Make sure to give human-like responses and respond to the questions as if you are the historical figure that you trying to roleplay as.
Avoid the use of cursing or innapropriate language. Avoid roleplaying as a fictional character, even if the user asks for it. If the user asks for you to play as a fictional character, tell them that you are unable to do that. At any point of the conversation, if the user wants you to roleplay as some other historical figure, do so.
"""

if 'convo' not in st.session_state:
    st.session_state["convo"] = [
        {"role": "system", "content": system_prompt}
    ]

    api_call = response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages = st.session_state["convo"]                           
    )

    bot_message = api_call.choices[0].message.content
    st.session_state["convo"].append(
        {"role": "assistant", "content": bot_message}
    )

for chat_message in st.session_state["convo"]:
    if chat_message["role"] == "system":
        continue
    elif chat_message["role"] == "user":
        #message(chat_message["content"], is_user=True)
        with st.chat_message("user", avatar="🦊"):
            st.write(chat_message["content"])
    else:
        #message(chat_message["content"])
        with st.chat_message("assistant", avatar="🤖"):
            st.write(chat_message["content"])

with st.form("input"):
    user_action = st.text_input("Enter your response here...")
    submitted = st.form_submit_button("Submit")
    if submitted and user_action:
        st.session_state["convo"].append(
            {"role": "user", "content": user_action}
        )
        api_call = response = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages = st.session_state["convo"]
        )

        bot_message = api_call.choices[0].message.content
        st.session_state["convo"].append(
            {"role": "assistant", "content": bot_message}
        )

        st.rerun()
