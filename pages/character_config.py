import json

import streamlit as st
from streamlit_cookies_controller import CookieController

from backend.storage.character_storage_context import CharacterContext
from backend.storage.cookie_management import read_cookie

st.set_page_config(page_title="Character Configuration", layout="wide")

# Protect access
if "character_context" not in st.session_state:
    cookie_controller = CookieController()
    ajs_id = cookie_controller.get("ajs_anonymous_id")
    stored_username = read_cookie(ajs_id, "username")
    if stored_username is None:
        st.error("No character loaded. Please go back to the main page.")
        st.stop()
    else:
        st.session_state["username"] = stored_username
        ctx_dict = json.loads(read_cookie(ajs_id, "character_context"))
        st.session_state["character_context"] = CharacterContext.from_dict(ctx_dict)

character = st.session_state["character_context"]

st.title(f"Character: {st.session_state['username']}")
st.write("Configuration options go here...")

# Example: show stats
#st.json(character)