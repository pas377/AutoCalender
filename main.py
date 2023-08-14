import os.path
import datetime as dt

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/calendar"]

def get_credentials():
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json")

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds

def create_event(start_time, end_time):
    creds = get_credentials()
    service = build("calendar", "v3", credentials=creds)
    event = {
        "summary": "Coding",
        "colorId": 2,
        "start": {
            "dateTime": start_time.isoformat(),
            "timeZone": "America/Denver"
        },
        "end": {
            "dateTime": end_time.isoformat(),
            "timeZone": "America/Denver"
        },
        "reminders": {
            "useDefault": False,
            "overrides": []
        }
    }

    try:
        event = service.events().insert(calendarId="primary", body=event).execute()
        print(f"Event created {event.get('htmlLink')}")
    except HttpError as error:
        print("An Error Occurred:", error)

def main():
    while True:
        action = input("Enter 's' to start time, 't' to see session length,"
                       " 'e' to end time or 'q' to quit: ").strip().lower()

        if action == "s":
            start_time = dt.datetime.now()
            print(f"Started at {start_time}")

        elif action == "t":
            if 'start_time' in locals():
                time_elapsed = dt.datetime.now() - start_time
                time_in_minutes = int(time_elapsed.total_seconds() / 60)
                print(f"Session: {time_in_minutes} minutes")
            else:
                print("Please start the time first!")

        elif action == "e":
            if 'start_time' in locals():
                end_time = dt.datetime.now()
                print(f"Ended at {end_time}")
                create_event(start_time, end_time)
            else:
                print("Please start the time first!")

        elif action == "q":
            break

        else:
            print("Invalid command!")


if __name__ == "__main__":
    main()