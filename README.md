# WATI Conversations Export Script

This script allows you to retrieve and export conversation data from the WATI API (WhatsApp Business API) and save it into a CSV file. It is designed to filter conversations by a given **target date** and uses a **Bearer token** for authentication.

---

## 🧰 Features

- Connects to the WATI Conversations API.
- Filters conversations by a given date.
- Stops after encountering 2 conversations assigned before or on the specified date.
- Extracts key details: Name, Contact Number, Created Date, Last Modified Date, and Notes.
- Outputs the result into a `wati_conversations.csv` file.
- CLI-based for flexible automation and integration.

---

## 📦 Requirements

- Python 3.7+
- Internet connection
- A valid WATI Bearer Token (with access to the appropriate WATI tenant)

Install the required Python modules (if not already installed):

```bash
pip install requests python-dateutil
```

## 🚀 How to Use
1. Clone or Download This Script
Save the script file as wati_fetcher.py.

2. Run from the Command Line

```bash
python wati_fetcher.py --date <DD-MM-YYYY> --token <YOUR_BEARER_TOKEN>
```
## Example:

```bash
python wati_fetcher.py --date 26-05-2025 --token eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```
## CLI Arguments
Argument	Required	Description

--date	✅ Yes	Target cutoff date (format: DD-MM-YYYY)

--token	✅ Yes	Your WATI Bearer token

## 📄 Output
The script generates a CSV file in the current directory:


```bash
wati_conversations.csv
```

## Columns in CSV:

Name – Contact name

Contact Number – WhatsApp ID

Date Created – Date the conversation was assigned

Last Modified – Last updated timestamp

Notes – Internal notes attached to the conversation

## ⏱ Behavior Notes

The script retrieves data in pages of 50 items.

After detecting 2 conversations with assignedAt date on or before the target date, it will stop fetching.

A 5-second pause occurs between paginated API requests to reduce server load and avoid throtal.

##❗ Disclaimer

Make sure your token is valid and has appropriate access permissions. Unauthorized or expired tokens will result in request failures.

