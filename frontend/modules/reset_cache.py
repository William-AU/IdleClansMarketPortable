import streamlit as st
from backend.storage.cookie_management import clear_cookies

def create_reset_cache_button(ajs_id):
    if st.button("Reset Cache", type="primary"):
        clear_cookies(ajs_id)
        st.switch_page("main.py")
