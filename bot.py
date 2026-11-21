import os
from dotenv import load_dotenv

from bs4 import BeautifulSoup
import requests
from datetime import date, timedelta
import json

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

        if start is not None and today <= start <= target:
            reminders.append((item, "Starts"))

        if end is not None and end != start and today <= end <= target:
            reminders.append((item, "Ends"))

    return reminders

def date_format(text):
    d = to_date(text)
    if d is None:
        return "N/A"
    return d.strftime("%A, %B %d")

def load_sent():
    try:
        with open(SENT_FILE, encoding="utf-8") as f:
            return set(json.load(f))

    except FileNotFoundError:
        return set()

def save_sent(sent):
    with open(SENT_FILE, "w", encoding="utf-8") as f:
        json.dump(sorted(sent), f, indent=2)

def reminder_key(item, action):
    return f"{action}|{item['start']}|{item['end']}|{item['subject']}"

load_dotenv()
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
DATES_URL = "https://www.torontomu.ca/calendar/2026-2027/dates/"
HEADERS = {"User-Agent": "TMU-CS-Discord-Bot (student project)"}
SENT_FILE = "sent_reminders.json"

dates = get_key_dates()
#print(f"Found {len(dates)} key dates.")
#print(dates[0])


today = date.today()
sent = load_sent()
reminders = reminders_due(dates, today)
new_count = 0

for item, action in reminders:
    key = reminder_key(item, action)
    if key in sent:
        continue

    title = f"{action} Soon: {item['subject']}"
    content = f"{item['description']}\n\nStart: {date_format(item['start'])}\nEnd: {date_format(item['end'])}"
    
    send_discord_message(WEBHOOK_URL, title, content, DATES_URL)

    sent.add(key)
    save_sent(sent)
    new_count += 1

print(f"{today}: {len(reminders)} due, {new_count} sent")
