import argparse
import requests
import csv
import time
from datetime import datetime
from dateutil.parser import isoparse

# ------------------- CLI ARGUMENT PARSING -------------------
parser = argparse.ArgumentParser(description='Fetch WATI conversations.')
parser.add_argument('--date', required=True, help='Target date in DD-MM-YYYY format')
parser.add_argument('--token', required=True, help='Bearer token for API authorization')

args = parser.parse_args()

# Parse date
try:
    TARGET_DATE = datetime.strptime(args.date, "%d-%m-%Y")
except ValueError:
    print("❌ Invalid date format. Please use DD-MM-YYYY.")
    exit(1)

TOKEN = args.token

# ------------------- CONFIG -------------------
API_URL = 'https://live-mt-server.wati.io/444/api/v1/conversations/filter'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:138.0) Gecko/20100101 Firefox/138.0',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Referer': 'https://live-444.wati.io/',
    'Content-Type': 'application/json',
    'Pragma': 'no-cache',
    'Authorization': f'Bearer {TOKEN}',
    'Origin': 'https://live-444.wati.io',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'Priority': 'u=4',
    'TE': 'trailers'
}

BASE_PAYLOAD = {
    "filterType": 0,
    "filterChannelIds": [""],
    "channelType": 0,
    "filterAttribute": [{"filterType": 4, "name": "", "operator": "", "value": ""}],
    "filterTopicNames": [
        "Counselor: Arshiya (FSC)",
        "Counselor: Arshiya Instagram",
        "counselor: Arshiya( fsc)"
    ],
    "filterAssignee": [],
    "filterStatus": [],
    "filterTeams": [],
    "searchString": "",
    "searchOptionType": 0,
    "pageSize": 50,
    "lastId": None,
    "showSpinner": True,
    "overViewModel": None,
    "oldChatsFirst": False,
    "lastConversation": None,
    "version": "v2"
}

def format_date(iso_str):
    try:
        dt = isoparse(iso_str)
        return dt.strftime('%b %d, %Y')
    except:
        return iso_str

def parse_notes(notes_list):
    if notes_list and isinstance(notes_list[0], dict):
        return '\n\n'.join(note.get('value', '') for note in notes_list)
    return ''

# ------------------- MAIN LOOP -------------------
all_rows = []
stop = False
last_id = None
target_date_hits = 0

while not stop:
    payload = BASE_PAYLOAD.copy()
    payload["lastId"] = last_id

    response = requests.post(API_URL, headers=HEADERS, json=payload)
    if response.status_code != 200:
        print(f"❌ Request failed with status code {response.status_code}")
        break

    items = response.json().get('result', {}).get('items', [])
    print(f"📥 Retrieved {len(items)} items")

    if not items:
        break

    for item in items:
        assigned_at_raw = item.get("ticket", {}).get("assignedAt", "")
        last_updated_raw = item.get("ticket", {}).get("lastUpdated", "")
        assigned_date = isoparse(assigned_at_raw) if assigned_at_raw else None

        if assigned_date and assigned_date.date() <= TARGET_DATE.date():
            target_date_hits += 1
            print(f"✅ Target date hit {target_date_hits} time(s) at: {assigned_date.date()}")
            if target_date_hits >= 2:
                stop = True
                break

        all_rows.append({
            'Name': item.get('name', ''),
            'Contact Number': item.get('whatsappId', ''),
            'Date Created': format_date(assigned_at_raw),
            'Last Modified': format_date(last_updated_raw) if last_updated_raw else '',
            'Notes': parse_notes(item.get('listNotes', []))
        })

    last_id = items[-1].get('id') if items else None
    if not last_id or stop:
        break

    print("⏳ Waiting 5 seconds before next request...")
    time.sleep(5)

# ------------------- WRITE TO CSV -------------------
with open('wati_conversations.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Name', 'Contact Number', 'Date Created', 'Last Modified', 'Notes']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(all_rows)

print("✅ Data saved to wati_conversations.csv")

