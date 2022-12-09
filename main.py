import streamlit as st
import os
import openai

default_prompt = """
Once upon a time, there lived a troll named Marty. His father was a bridge troll. His grandfather was a bridge troll. Every one of Marty’s ancestors had all been bridge trolls.

A proud troll, Marty’s father longed for the day when his son would fulfill his family’s legacy of collecting bridge tolls.

And yet, Marty’s true passion had always been dance.
""".strip()

openai.api_key = os.getenv("API_KEY")

if not st.session_state.get("logged_in"):
    with st.form("login"):
        password = st.text_input("password", type="password")
        submitted_login = st.form_submit_button("submit")
        if submitted_login:
            if password == "password":
                st.session_state.logged_in = True
                st.experimental_rerun()
            else:
                st.error("invalid password")
else:

    st.title("Story Teller")


    prompt = st.text_area("prompt", value=default_prompt, label_visibility="collapsed")
    continue_ = st.button("continue")
    reset = st.button("reset")


    prompt = st.session_state.get("prompt") or prompt

    if continue_:
        resp = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=256,
            temperature=0.7,
        )
        [choice] = resp["choices"]
        text = prompt + choice["text"]
        st.text(text)
        st.session_state.prompt = text

    if reset and st.session_state.get("prompt"):
        del st.session_state.prompt
