import time
import requests
import schedule

# CIJ and Discord credentials
CIJ_SESSION_TOKEN = 'YOUR_CIJ_SESSION_TOKEN'
DISCORD_GUILD_ID = '944788194895986688'
DISCORD_TOKEN = 'YOUR_DISCORD_TOKEN'
USERNAME = 'YOUR_DISCORD_USERNAME'

def fetch_study_hours():
    """Fetch the total lifetime study hours from the CIJ API."""
    url = "https://cijapanese.com/api/v1/user-stats/lifetime-hours"
    headers = {
        "Cookie": f"user_session={CIJ_SESSION_TOKEN}",
        "Accept": "*/*"
    }

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        try:
            hours = float(response.json().get("data", {}).get("hours", 0))
            print(f"Fetched study hours: {hours} hrs")
            return hours
        except (ValueError, TypeError) as e:
            print(f"Failed to parse study hours. Error: {e}")
            return -1
    elif response.status_code == 401:
        print("Unauthorized: Your cij session token has expired. Update it and restart the script.")
        exit()
    else:
        print(f"Error: Received unexpected status code {response.status_code}. Will try again later.")
        return -1

def update_discord_profile(total_study_hours):
    """Update the Discord profile nickname with the current study hours."""
    url = f"https://discord.com/api/v9/guilds/{DISCORD_GUILD_ID}/members/@me"
    headers = {
        "Authorization": DISCORD_TOKEN,
        "Content-Type": "application/json",
        "Accept": "*/*",
    }
    data = {"nick": f"{USERNAME} [{total_study_hours} hrs]"}

    response = requests.patch(url, headers=headers, json=data)

    if response.status_code == 200:
        print("Nickname updated successfully.")
    elif response.status_code == 401:
        print("Unauthorized: Your discord session token has expired. Update it and restart the script.")
        exit()
    else:
        print(f"Error: Received unexpected status code {response.status_code}. Will try again later.")
        return -1

def sync_study_hours():
    """Fetch study hours from CIJ and update Discord profile."""
    print("Starting study hours sync...")

    total_study_hours = fetch_study_hours()

    if total_study_hours > 0:
        print("Got study hours from CIJ dashboard, updating Discord profile...")
        update_discord_profile(total_study_hours)
    else:
        print("Failed to retrieve study hours.")

    print('------------------------------------------------')

if __name__ == "__main__":
    schedule.every().hour.do(sync_study_hours)

    print("Scheduler started. Running every hour.")
    while True:
        schedule.run_pending()
        time.sleep(1)
