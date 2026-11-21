import os
from dotenv import load_dotenv

from bs4 import BeautifulSoup
import requests
from datetime import date, timedelta

def send_discord_message(webhook_url, title, content, url):
    post = {"embeds": [{"title": title, "description": content, "url": url, "color": 0x004C9B}]}
    response = requests.post(webhook_url, json=post)
    response.raise_for_status()
    print("Message sent to Discord successfully.")

def get_key_dates():

    response = requests.get(DATES_URL, headers=HEADERS)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    table = soup.find("table")

    key_dates = []
    for row in table.find_all("tr")[1:]:
        cells = [td.get_text(strip=True) for td in row.find_all("td")]

        if len(cells) < 5:
            continue

        key_dates.append({
            "start": cells[0],
            "end": cells[1],
            "category": cells[2],
            "subject": cells[3],
            "description": cells[4]
        })
    
    return key_dates

def to_date(text):
    try: 
        return date.fromisoformat(text)
    except ValueError:
        return None

def is_relevant(dates):
    subject = dates["subject"]

    if dates["category"] == "Chang School Session Start/End Dates":
        return False

    if "Engineering" in subject:
        if "Other than" in subject or "Including" in subject or "except" in subject:
            return True
        return False

    return True

def reminders_due(key_dates, today):
    target = today + timedelta(days=3)
    reminders = []

    for item in key_dates:
        if not is_relevant(item):
            continue

        start = to_date(item["start"])
        end = to_date(item["end"])

        if start == target:
            reminders.append((item, "Starts"))

        if end == target and end != start:
            reminders.append((item, "Ends"))

    return reminders

def date_format(text):
    d = to_date(text)
    if d is None:
        return "N/A"
    return d.strftime("%A, %B %d")

load_dotenv()
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

DATES_URL = "https://www.torontomu.ca/calendar/2026-2027/dates/"
HEADERS = {"User-Agent": "TMU-CS-Discord-Bot (student project)"}

dates = get_key_dates()
#print(f"Found {len(dates)} key dates.")
#print(dates[0])

today = date(2026, 12, 17)

reminders = reminders_due(dates, today)

for item, action in reminders:
    title = f"{action} Soon: {item['subject']}"
    content = f"{item['description']}\n\nStart: {date_format(item['start'])}\nEnd: {date_format(item['end'])}"
    send_discord_message(WEBHOOK_URL, title, content, DATES_URL)
