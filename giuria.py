# Copyright (c) 2023 Giuseppe Cammarota

from dotenv import dotenv_values
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import streamlit as st

SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "openid", "https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email"]
CREDENTIAL_KEY = "credentials"


def get_client_config():
    client_config = {"web": {k: v for k, v in dotenv_values("client_secret.env").items()}}
    client_config["web"].update({
        "redirect_uris": ["https://demoscopica.streamlit.app/", "http://localhost:8501/", "http://localhost:8500/"],
    })
    return client_config

def get_credentials():
    if st.session_state.get(CREDENTIAL_KEY) is not None:
        return
    if "token" in st.session_state:
        st.session_state[CREDENTIAL_KEY] = Credentials.from_authorized_user_info(st.session_state["token"], SCOPES)
    credentials = st.session_state.get(CREDENTIAL_KEY)
    # If there are no (valid) credentials available, let the user log in.
    if credentials is None or not credentials.valid:
        if credentials is not None and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_config(get_client_config(), SCOPES)
            credentials = flow.run_local_server(port=8500)
            st.session_state[CREDENTIAL_KEY] = credentials
        # Save the credentials for the next run
        st.session_state["token"] = credentials.to_json()


if __name__ == "__main__":
    st.title("# Giuria Demoscopica Privata 👋")
    get_credentials()
    st.write(st.session_state)

