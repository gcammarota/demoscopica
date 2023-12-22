# Copyright (c) 2023 Giuseppe Cammarota

import sys

from dotenv import dotenv_values
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import streamlit as st


CREDENTIAL_KEY = "credentials"
REDIRECT_URIS = ["https://demoscopica.onrender.com", "http://localhost:8501/"]
SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "openid", "https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email"]


def read_client_config_env_file(client_config):
    client_config = {"web": {k: v for k, v in dotenv_values(client_config).items()}}
    client_config["web"].update({"redirect_uris": REDIRECT_URIS, "redirect_uri": [REDIRECT_URIS[1]]})
    return client_config


def get_credentials(client_config):
    if "token" in st.session_state:
        st.session_state[CREDENTIAL_KEY] = Credentials.from_authorized_user_info(st.session_state["token"], SCOPES)
    credentials = st.session_state.get(CREDENTIAL_KEY)
    # If there are no (valid) credentials available, let the user log in.
    if credentials is None or not credentials.valid:
        if credentials is not None and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = Flow.from_client_config(read_client_config_env_file(client_config), SCOPES)
            flow.redirect_uri = REDIRECT_URIS[0]
            url, _ = flow.authorization_url()
            st.link_button("Accedi a Goole", url, type="primary")
            user_info = None
            params = st.experimental_get_query_params()
            if params:
                token = flow.fetch_token(code=params["code"][0])
                credentials = Credentials(token["access_token"])
                st.session_state[CREDENTIAL_KEY] = credentials
                user_info_service = build('oauth2', 'v2', credentials=credentials)
                user_info = user_info_service.userinfo().get().execute()
                # Save the credentials for the next run
                st.session_state["token"] = token
            st.write(user_info)


def run(client_config):
    st.title("# Giuria Demoscopica Privata 👋")
    if st.session_state.get(CREDENTIAL_KEY) is None:
        get_credentials(client_config=client_config)
    else:
        st.write(st.session_state)

if __name__ == "__main__":
    client_config = "client_secret.env"
    if len(sys.argv) > 1:
        client_config = sys.argv[1]
    run(client_config=client_config)

