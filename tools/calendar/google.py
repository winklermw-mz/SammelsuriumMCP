import os
from utils.config import GOOGLE_TOKEN, GOOGLE_CREDENTIALS, GOOGLE_SCOPES
from datetime import datetime, timedelta, timezone
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


def get_google_service():
    creds = None
    if os.path.exists(GOOGLE_TOKEN):
        creds = Credentials.from_authorized_user_file(GOOGLE_TOKEN, GOOGLE_SCOPES)

    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(GOOGLE_CREDENTIALS, GOOGLE_SCOPES)
        creds = flow.run_local_server(port=0)
        with open(GOOGLE_TOKEN, "w") as token:
            token.write(creds.to_json())

    return build("calendar", "v3", credentials=creds)

def _print_event_details(summary: str, start: str, end: str, duration: str) -> str:
    return f"Event '{summary}', from {start} to {end}, duration: {duration}"

def _list_all_calendars(service) -> dict:
    calendar_list = service.calendarList().list().execute()
    calendars = {}
    for cal in calendar_list.get("items", []):
        calendars[cal.get("id")] = cal.get("summary", "untitled")
    return calendars

def _find_calendar_by_name(calendar_name: str, calendars: dict) -> str:
    for id, name in calendars.items():
        if name == calendar_name:
            return id
    raise Exception(f"Calendar '{name}' not found")

def _get_all_events(service, calendar_id: str, days: int):
    now = datetime.now(timezone.utc)
    week_later = now + timedelta(days=days)

    events_result = service.events().list(
        calendarId=calendar_id,
        timeMin=now.isoformat(),
        timeMax=week_later.isoformat(),
        singleEvents=True,
        orderBy="startTime"
    ).execute()
    return events_result.get("items", [])

def get_all_available_calendars() -> str:
    service = get_google_service()
    calendars = _list_all_calendars(service)
    if not calendars:
        raise Exception("No calendars found")

    result = []
    for id, name in calendars.items():
        result.append(name)
    return ", ".join(result)

def get_all_calendar_entries(calendar_name: str, days: int) -> str:
    service = get_google_service()
    id = _find_calendar_by_name(calendar_name, _list_all_calendars(service))
    events = _get_all_events(service, id, days)
    
    if not events:
        return f"{calendar_name}: No events within the next 7 days"

    entries = [f"{calendar_name}:"]

    for event in events:
        start_raw = event["start"].get("dateTime", event["start"].get("date"))
        end_raw = event["end"].get("dateTime", event["end"].get("date"))

        is_full_day = "T" not in start_raw
        start_dt = datetime.fromisoformat(start_raw)
        end_dt = datetime.fromisoformat(end_raw)
        duration = end_dt - start_dt

        if is_full_day:
            start_str = start_dt.strftime("%Y-%m-%d")
            end_str = end_dt.strftime("%Y-%m-%d")
            duration_str = f"{duration.days} day(s)"
            entries.append(_print_event_details(event.get('summary'), start_str, end_str, duration_str))
        else:
            start_str = start_dt.strftime("%Y-%m-%d %H:%M")
            end_str = end_dt.strftime("%Y-%m-%d %H:%M")
            hours = duration.total_seconds() / 3600
            duration_str = f"{hours:.1f} h"
            entries.append(_print_event_details(event.get('summary'), start_str, end_str, duration_str))
    
    return "\n".join(entries)
