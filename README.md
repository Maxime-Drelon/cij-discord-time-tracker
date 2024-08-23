# Comprehensible Japanese Discord Server Time Tracker

This program uses Selenium to grab your total lifetime study hours from the CIJ website. I couldn’t get the info through a regular request since it’s not included in any of the network requests made while you’re on the dashboard page. Plus, cross-origin requests aren’t allowed, which makes things a bit tricky.

## How to Launch

1. **Clone the Repository** (obviously):

    ```bash
    git clone git@github.com:Maxime-Drelon/cij-discord-time-tracker.git
    cd cij-discord-time-tracker
    ```
3. **Set your discord & cij tokens as well as your username inside main.py**:

    ```py
    cij_cookie = {
      'name': 'user_session',
      'value': 'YOUR_CIJ_SESSION_TOKEN_HERE',
      'sameSite': 'Lax',
      'httpOnly': True,
      'secure': True
    }

    discord_token = 'YOUR_DISCORD_TOKEN_HERE'
    username = 'YOUR_DISCORD_USERNAME_HERE'
    ```

    - You can find your cij token directly in your cookies on [https://cijapanese.com](https://cijapanese.com/), this should never expire if the script runs at least once per month
    - For the discord token, it is not directly accessible inside the cookies so you will need to either inspect the network tab and find it inside a request or make this post request
    <br/>
    
    ```curl
    curl -X POST https://discord.com/api/v9/auth/login \
    -H "Content-Type: application/json" \
    -d '{"login": "YOUR EMAIL HERE", "password": "YOUR PASSWORD HERE"}'
    ```

    I don't know yet if and when the discord expires, if it does I will update this and automatically fetch one using this request

4. **Set how often you want it to sync**:

    The scripts was scheluded to run every 15 minutes for testing purposes, If you want to change it to something else you can refer to this [documentation](https://schedule.readthedocs.io/en/stable/index.html), and update it here
   
    ```py
    if __name__ == "__main__":
    schedule.every(15).minutes.do(sync_study_hours)

    while True:
        schedule.run_pending()
        time.sleep(1)
    ```

6. **Build and Start the Services**:

    ```bash
    docker-compose up --build -d
    ```

    - The `--build` flag ensures that the `time-scrapper` service is rebuilt.
    - The `-d` flag runs the services in detached mode (in the background).

7. **Verify that the Services are Running**:

    ```bash
    docker-compose ps
    ```

8. **Stopping the Services**:

    ```bash
    docker-compose down
    ```
