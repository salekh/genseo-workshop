import os
from google_auth_oauthlib.flow import InstalledAppFlow
from pathlib import Path
from dotenv import load_dotenv

# Load .env from project root
env_path = Path(__file__).resolve().parents[3] / '.env'
load_dotenv(dotenv_path=env_path)

def main():
    client_id = os.getenv("GOOGLE_ADS_CLIENT_ID")
    client_secret = os.getenv("GOOGLE_ADS_CLIENT_SECRET")

    if not client_id or not client_secret:
        print("Error: GOOGLE_ADS_CLIENT_ID and GOOGLE_ADS_CLIENT_SECRET must be set in .env")
        return

    # Scopes for Google Ads API
    scopes = ["https://www.googleapis.com/auth/adwords"]

    # Create the flow using the client ID and secret directly
    flow = InstalledAppFlow.from_client_config(
        {
            "installed": {
                "client_id": client_id,
                "client_secret": client_secret,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
            }
        },
        scopes=scopes
    )

    print("Launching browser for authentication...")
    # Use port 8080 to match a likely registered redirect URI for Web Apps
    # If using Desktop App, this still works.
    creds = flow.run_local_server(port=8080)

    print("\nSuccessfully authenticated!")
    print(f"Refresh Token: {creds.refresh_token}")
    print("\nCopy this Refresh Token into your .env file as GOOGLE_ADS_REFRESH_TOKEN")

if __name__ == "__main__":
    main()
