import time
import requests
import schedule
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException

# Selenium driver options
options = webdriver.FirefoxOptions()
options.add_argument('--headless')
selenium_url = 'http://selenium:4444/wd/hub'

# CIJ credentials
cij_cookie = {
    'name': 'user_session',
    'value': 'YOUR_CIJ_SESSION_TOKEN_HERE',
    'sameSite': 'Lax',
    'httpOnly': True,
    'secure': True
}

# Discord parameters
guild_id = '944788194895986688'
discord_token = 'YOUR_DISCORD_TOKEN_HERE'
username = 'YOUR_DISCORD_USERNAME_HERE'

def fetch_study_hours(driver):
    try:
        print("Loading login page...")
        driver.get('https://cijapanese.com/login')
        time.sleep(5)

        print("Adding session cookie & refreshing page...")
        driver.add_cookie(cij_cookie)
        driver.refresh()
        time.sleep(5)

        if 'login' in driver.current_url:
            print("Couldn't login using existing cookie, please refresh it...")
            return -1

        print("Loading dashboard page...")
        driver.get('https://cijapanese.com/dashboard')
        time.sleep(5)

        print("Searching for total lifetime study hours...")
        total_study_hours_div = driver.find_element(By.XPATH, '//div[@class="mt-4"]')
        total_study_hours_text = total_study_hours_div.text.split()[-1]

        try:
            total_study_hours = float(total_study_hours_text)
            print(f"Total lifetime study hours: {total_study_hours}")
            return total_study_hours
        except ValueError:
            print("The extracted value is not a valid float.")
            return -1

    except WebDriverException as e:
        print(f"WebDriverException occurred: {e}")
        return -1

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return -1

def update_discord_profile(total_study_hours):
    url = f"https://discord.com/api/v9/guilds/{guild_id}/members/@me"
    headers = {
        "Authorization": discord_token,
        "Content-Type": "application/json",
        "Accept": "*/*",
    }
    data = {"nick": f"{username} [{total_study_hours} hrs]"}
    
    response = requests.patch(url, headers=headers, json=data)
    if response.status_code == 200:
        print("Nickname updated successfully.")
    else:
        print(f"Failed to update nickname. Status code: {response.status_code}")
        print(response.text)

def sync_study_hours():
    print("Starting study hours sync...")

    try:
        driver = webdriver.Remote(selenium_url, options=options)
    except:
        print("Failed to initialize webdriver, skipping this sync")
        return

    total_study_hours = fetch_study_hours(driver)

    if total_study_hours > 0:
        print("Got study hours from CIJ dashboard, updating Discord profile...")
        update_discord_profile(total_study_hours)
    else:
        print("Failed to retrieve study hours.")

    try:
        driver.quit()
    except:
        pass

    print('------------------------------------------------')

if __name__ == "__main__":
    schedule.every(15).minutes.do(sync_study_hours)

    while True:
        schedule.run_pending()
        time.sleep(1)
