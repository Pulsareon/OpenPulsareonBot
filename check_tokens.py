
import os
import json
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import datetime

# Directory containing your token files
TOKEN_DIR = r'E:\PulsareonThinker\data\secrets\api_credentials\AuthenticationFiles'
SCOPES = ['https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/drive.metadata.readonly']

def create_dummy_client_secret():
    # This function is a placeholder. In a real scenario, you'd get this from your Google Cloud project.
    # We'll try to extract client_id and client_secret from the token files if they are available
    # or assume the token files are complete enough for refresh.
    dummy_client_secret = {
        "installed": {
            "client_id": "YOUR_CLIENT_ID", # Placeholder
            "project_id": "YOUR_PROJECT_ID", # Placeholder
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_secret": "YOUR_CLIENT_SECRET", # Placeholder
            "redirect_uris": ["http://localhost"]
        }
    }
    with open("client_secret.json", "w") as f:
        json.dump(dummy_client_secret, f, indent=4)
    return "client_secret.json"

def get_credentials_from_file(token_file_path):
    creds = None
    if os.path.exists(token_file_path):
        with open(token_file_path, 'r') as token:
            token_data = json.load(token)
            creds = Credentials.from_authorized_user_info(token_data, SCOPES)
    return creds, token_data # Also return token_data to check for client_id/secret

def check_and_refresh_token(creds, token_file_path, token_data):
    status = "UNKNOWN"
    
    # Try to refresh if expired
    if creds and creds.expired and creds.refresh_token:
        print(f"Attempting to refresh token from {token_file_path}...")
        try:
            # Check if client_id and client_secret are available in token_data
            if 'client_id' in token_data and 'client_secret' in token_data:
                # Use client_id and client_secret from the token_data if available
                # This part is tricky as Credentials.refresh expects a Request object which would typically have flow.client_config
                # For direct refresh, we generally need the client_config
                # As a workaround, we could reconstruct a flow for refresh or rely on the existence of a client_secret.json
                # For now, let's assume `client_secret.json` is present or creds object has enough info.
                
                # A more robust way to refresh without relying on a separate client_secret.json if client info is in token:
                # This requires constructing a new Credentials object with client_id and client_secret directly
                # However, the standard google.oauth2.credentials.Credentials.refresh() method
                # relies on credentials having client_id and client_secret attributes which are set from the initial flow.
                # If they are not present in the initial token file, the refresh might fail.

                # Let's try to update the dummy client_secret.json if values are found in the token file
                # This might not be ideal but ensures the flow has necessary info.
                # In a production setup, client_secret.json should be static.
                with open("client_secret.json", "r+") as f:
                    client_secret_config = json.load(f)
                    if token_data.get('client_id') and token_data.get('client_secret'):
                         client_secret_config['installed']['client_id'] = token_data['client_id']
                         client_secret_config['installed']['client_secret'] = token_data['client_secret']
                    f.seek(0)
                    json.dump(client_secret_config, f, indent=4)
                    f.truncate()
                
                flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
                creds.refresh(Request())
                status = "REFRESHED"
                # Save the refreshed token
                with open(token_file_path, 'w') as token:
                    token.write(creds.to_json())
            else:
                # If client_id and client_secret are not in the token data, try refreshing with existing creds
                creds.refresh(Request())
                status = "REFRESHED"
                # Save the refreshed token
                with open(token_file_path, 'w') as token:
                    token.write(creds.to_json())

        except Exception as e:
            print(f"Failed to refresh token for {token_file_path}: {e}")
            status = "DEAD"
    elif creds and not creds.expired:
        status = "ALIVE"
    elif creds and creds.expired and not creds.refresh_token:
        status = "DEAD (no refresh token)"
    elif not creds:
        status = "DEAD (could not load credentials)"
    
    return status, creds

def verify_token_with_api(creds):
    if not creds:
        return False
    try:
        # Use Google Drive API to make a simple call
        service = build('drive', 'v3', credentials=creds)
        # Attempt to list files, but only metadata for a small number to keep it light
        service.files().list(pageSize=1, fields="nextPageToken, files(id, name)").execute()
        return True
    except Exception as e:
        print(f"API call failed: {e}")
        return False

def main():
    token_files = [f for f in os.listdir(TOKEN_DIR) if f.endswith('.json')]
    results = []

    # Create a dummy client_secret.json if it doesn't exist. This is needed by InstalledAppFlow.
    # In a real setup, you would have your actual client_secret.json
    client_secret_path = "client_secret.json"
    if not os.path.exists(client_secret_path):
        create_dummy_client_secret()

    for token_file in token_files:
        full_path = os.path.join(TOKEN_DIR, token_file)
        creds, token_data = get_credentials_from_file(full_path)
        token_status = "DEAD" # Default to dead

        if creds:
            if verify_token_with_api(creds):
                token_status = "ALIVE"
            else:
                # API call failed, try to refresh
                token_status, updated_creds = check_and_refresh_token(creds, full_path, token_data)
                if updated_creds and verify_token_with_api(updated_creds):
                    token_status = "REFRESHED" # Successfully refreshed and now alive
                elif token_status == "REFRESHED": # If refresh was successful but API still fails
                    token_status = "DEAD (refreshed but still failed API)"
        
        results.append({"file": token_file, "status": token_status})

    print("\n--- Token Validation Summary ---")
    print(f"{'Token File':<50} {'Status':<20}")
    print(f"{'-'*50} {'-'*20}")
    for result in results:
        print(f"{result['file']:<50} {result['status']:<20}")

if __name__ == "__main__":
    main()
