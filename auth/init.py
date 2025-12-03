from utils.config import GOOGLE_TOKEN, GOOGLE_CREDENTIALS, GOOGLE_SCOPES
from google_auth_oauthlib.flow import InstalledAppFlow

flow = InstalledAppFlow.from_client_secrets_file(GOOGLE_CREDENTIALS, GOOGLE_SCOPES)
creds = flow.run_local_server(port=0)
with open(GOOGLE_TOKEN, "w") as token:
    token.write(creds.to_json())