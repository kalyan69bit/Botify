import requests
import random
import time
import os

# Telegram Bot Configuration
BOT_TOKEN = "7999323068:AAGugLV6QNeT16-CGl_sPKvFNSbWmyAmrak"
CHAT_ID = "6903781705"

# API URL format without the need for an API key
API_URL = "https://api.skrapp.io/v3/open/verify?email={email}"

# Updated list of proxy servers
proxy_list = [
    "156.233.72.152:3128", "156.233.86.13:3128", "156.228.94.124:3128", "154.214.1.161:3128",
    "156.228.190.138:3128", "156.253.177.223:3128", "104.167.28.51:3128", "156.253.168.215:3128",
    "45.201.11.7:3128", "104.207.52.20:3128", "104.167.31.132:3128", "104.207.33.164:3128",
    "156.228.87.166:3128", "154.94.14.24:3128", "156.228.96.73:3128", "156.228.97.162:3128",
    "156.228.185.54:3128", "104.207.45.4:3128", "156.228.88.252:3128", "156.233.93.89:3128",
    "156.228.124.179:3128", "156.233.85.83:3128", "156.240.99.251:3128", "156.228.82.126:3128",
    "45.202.76.119:3128", "156.228.111.252:3128", "156.233.73.10:3128", "104.207.37.23:3128",
    "154.213.202.130:3128", "156.228.106.196:3128", "156.228.95.251:3128", "156.228.189.72:3128",
    "104.207.60.135:3128", "156.228.118.77:3128", "156.228.181.26:3128", "156.233.91.154:3128",
    "104.167.29.103:3128", "156.228.185.151:3128", "156.228.189.208:3128", "156.228.176.18:3128",
    "104.207.34.212:3128", "156.228.93.104:3128", "156.228.177.137:3128", "156.228.79.66:3128",
    "156.228.106.28:3128", "156.228.95.4:3128", "104.207.44.216:3128", "156.228.82.198:3128",
    "45.202.77.120:3128", "104.207.35.98:3128", "156.233.72.76:3128", "156.228.112.131:3128",
    "156.228.109.17:3128", "156.228.90.193:3128", "156.228.119.6:3128", "104.167.29.206:3128",
    "156.228.118.221:3128", "156.228.98.184:3128", "104.207.60.181:3128", "45.202.76.24:3128",
    "156.228.77.96:3128", "156.228.180.140:3128", "156.228.89.17:3128", "156.253.173.48:3128",
    "154.94.15.143:3128", "156.228.110.76:3128", "104.167.28.160:3128", "156.253.167.158:3128",
    "156.253.170.74:3128", "104.207.50.41:3128", "156.228.184.0:3128", "104.207.56.254:3128",
    "104.207.51.15:3128", "156.228.185.138:3128", "156.228.190.85:3128", "156.233.73.58:3128",
    "154.94.14.148:3128", "156.228.98.195:3128", "104.207.38.175:3128", "104.207.44.137:3128",
    "156.228.98.112:3128", "156.253.175.149:3128", "45.201.11.204:3128", "154.94.13.219:3128",
    "104.207.56.226:3128", "154.213.193.213:3128", "156.228.119.239:3128", "154.214.1.213:3128",
    "104.207.46.115:3128", "156.253.178.187:3128", "104.207.63.24:3128", "156.233.85.247:3128",
    "156.233.86.112:3128", "156.228.108.93:3128", "45.202.76.97:3128", "156.228.101.63:3128",
    "156.228.183.181:3128", "156.253.168.56:3128", "104.167.28.64:3128", "156.228.177.9:3128"
]

# Function to get a random proxy
def get_random_proxy():
    proxy = random.choice(proxy_list)
    return {"http": proxy, "https": proxy}

# Telegram Functions
def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    response = requests.post(url, json={"chat_id": CHAT_ID, "text": text})
    if response.status_code == 200:
        return response.json()["result"]["message_id"]
    else:
        print(f"Failed to send Telegram message: {response.status_code}")
        return None

def edit_telegram_message(message_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/editMessageText"
    response = requests.post(url, json={"chat_id": CHAT_ID, "message_id": message_id, "text": text})
    if response.status_code != 200:
        print(f"Failed to edit Telegram message: {response.status_code}")

def send_telegram_file(file_path):
    """Function to send a file to Telegram."""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
    with open(file_path, 'rb') as file:
        response = requests.post(url, data={"chat_id": CHAT_ID}, files={"document": file})
    if response.status_code != 200:
        print(f"Failed to send file to Telegram: {response.status_code}")

# Read emails from file.txt (adjust path for VPS)
email_file_path = '/root/Botify/file.txt'
try:
    with open(email_file_path, 'r') as file:
        emails = file.read().splitlines()
except FileNotFoundError:
    print(f"The file `file.txt` was not found at {email_file_path}.")
    exit()

# Initialize Counters
total_emails = len(emails)
valid_emails = []
invalid_emails = []
checked_emails = 0

# Send initial progress message to Telegram
progress_message = f"""
Script Started 📤
-------------------
Total Emails: {total_emails}
Checked: {checked_emails}
Valid: {len(valid_emails)}
Invalid: {len(invalid_emails)}
"""
message_id = send_telegram_message(progress_message)

# File path to save valid emails (adjust path for VPS)
output_file_path = '/root/Botify/valid.txt'

# Validate Emails
for email in emails:
    proxy = get_random_proxy()  # Get a random proxy for each request
    try:
        response = requests.get(API_URL.format(email=email), proxies=proxy, timeout=10)
        if response.status_code == 200:
            data = response.json()
            # Check if the email is valid
            if data.get("email_status") == "valid" and data.get("mailbox_status") == "valid":
                valid_emails.append(email)
            else:
                invalid_emails.append(email)  # Add to invalid emails list
        else:
            print(f"Failed to verify {email}: {response.status_code}")
            invalid_emails.append(email)  # Treat as invalid if the request fails
    except requests.exceptions.RequestException as e:
        print(f"Request failed for {email} using proxy {proxy}: {e}")
        invalid_emails.append(email)  # Treat as invalid if there's a request exception

    # Update counters
    checked_emails += 1

    # Update progress in Telegram every 50 emails or after all are processed
    if checked_emails % 50 == 0 or checked_emails == total_emails:
        progress_message = f"""
📊 Progress Update:
-------------------
Total Emails: {total_emails}
Checked: {checked_emails}
Valid: {len(valid_emails)}
Invalid: {len(invalid_emails)}
"""
        if message_id:
            edit_telegram_message(message_id, progress_message)

    # Write valid emails to file every 500 emails or at the end
    if checked_emails % 500 == 0 or checked_emails == total_emails:
        with open(output_file_path, 'w') as valid_file:
            valid_file.write("\n".join(valid_emails))

        # Send the valid emails file to Telegram every 500 valid emails or at the end
        send_telegram_file(output_file_path)

    # Pause to avoid rate limiting
    time.sleep(1)

# Final update when the script finishes
progress_message = f"""
✅ Script Completed:
-------------------
Total Emails: {total_emails}
Checked: {checked_emails}
Valid: {len(valid_emails)}
Invalid: {len(invalid_emails)}
Valid emails written to `valid.txt` 📁.
"""
if message_id:
    edit_telegram_message(message_id, progress_message)

# Send final valid email file at the end
send_telegram_file(output_file_path)
