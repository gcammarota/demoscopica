# Copyright (c) 2023 Giuseppe Cammarota

from requests_oauthlib import OAuth2Session
import streamlit as st


REDIRECT_URI = "https://demoscopica.streamlit.app/"
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


def authorize():
    google = OAuth2Session(st.secrets["CLIENT_ID"], redirect_uri=REDIRECT_URI, scope=SCOPES)
    authorization_url, state = google.authorization_url(
        "https://accounts.google.com/o/oauth2/v2/auth",
        access_type="offline",
        prompt="select_account"
    )
    st.markdown(f"[Login with Google]({authorization_url})")


def run():
    st.write("# Giuria Demoscopica Privata 👋")
    authorize


if __name__ == "__main__":
    run()
