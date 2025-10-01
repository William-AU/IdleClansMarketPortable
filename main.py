import json

import streamlit as st
import logging
from backend.storage.character_storage import get_character_context
from streamlit_cookies_controller import CookieController
from backend.storage.cookie_management import save_cookie
from configuration.log.logconfig import setup_logging

logger = logging.getLogger(__name__)
st.set_page_config(page_title="Main Page", layout="centered")
setup_logging()

def load_character(username: str):
    return get_character_context(username)


st.title("IdleClans Market Analyzer")
st.write("Enter a character username to load data")
cookie_controller = CookieController()

with st.form("character_form"):
    username = st.text_input("Character Username", placeholder="Enter player name...")

    submitted = st.form_submit_button("Load Character")

    if submitted:
        if username.strip() == "":
            st.error("Please enter a valid username.")
        else:
            try:
                character_context = load_character(username)
                if character_context is None:
                    raise ValueError("Character data could not be retrieved (check case sensitivity)")

                # Store in session_state for easy navigation
                st.session_state["username"] = username
                st.session_state["character_context"] = character_context
                logger.debug("Getting ajs ID")
                ajs_id = cookie_controller.get("ajs_anonymous_id")
                logger.debug("Saving cookies")
                save_cookie(ajs_id, "username", username)
                save_cookie(ajs_id, "character_context", json.dumps(character_context.to_dict()))
                logger.debug("Cookies set:")
                logger.debug(cookie_controller.getAll())

                st.success(f"Data for **{username}** has been fetched and stored successfully!")
                st.switch_page("pages/character_config.py")

            except Exception as e:
                st.error(f"An error occurred: {e}")
                logger.error(f"An error occurred: {e}")
