# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 3

import pandas as pd
import numpy as np
from plotnine import *
from shiny import App, ui, render

# Note: gargle is an R package specifically for Google API authentication.
# In Python, the equivalent is using google-auth and google-auth-oauthlib.

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import os
import pickle

# r2py:entity:drive_auth
def drive_auth(email=None, 
               path=None, 
               scopes=["https://www.googleapis.com/auth/drive"], 
               cache=None, 
               use_oob=False, 
               token=None):
    """
    Python implementation of a Google Drive authentication flow 
    similar to gargle's drive_auth.
    """
    # Use provided token if available
    if token:
        return token

    # Set default cache path if not provided
    if cache is None:
        cache = "token.pickle"
    if path:
        cache = os.path.join(path, cache)

    creds = None
    # Try loading existing credentials from cache
    if os.path.exists(cache):
        with open(cache, 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and Request().refresh_token(creds):
            with open(cache, 'wb') as token:
                pickle.dump(creds, token)
        else:
            # This assumes client_secrets.json is in the working directory
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secrets.json', scopes=scopes
            )
            
            if use_oob:
                # Out-of-band flow for environments without browser access
                flow.run_local_server(port=0, open_browser=False)
            else:
                flow.run_local_server(port=0)
                
            creds = flow.credentials
            
            # Save the credentials for the next run
            with open(cache, 'wb') as token:
                pickle.dump(creds, token)

    return creds