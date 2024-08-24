# Comprehensible Japanese Discord Server Time Tracker

This very basic script fetches your total lifetime study hours directly from the CIJ API. Big thanks to [Bennycopter](https://github.com/Bennycopter) for providing this endpoint and making the script a lot simpler. 

## How to Launch

1. **Clone the Repository** (obviously):

    ```bash
    git clone git@github.com:Maxime-Drelon/cij-discord-time-tracker.git
    cd cij-discord-time-tracker
    ```
3. **Set your discord & cij tokens as well as your username inside main.py**:

    ```py
    CIJ_SESSION_TOKEN = 'YOUR_CIJ_SESSION_TOKEN'
    DISCORD_TOKEN = 'YOUR_DISCORD_TOKEN'
    USERNAME = 'YOUR_DISCORD_USERNAME'
    ```

    - You can find your cij token directly in your cookies on [https://cijapanese.com](https://cijapanese.com/), this should never expire if the script runs at least once per month
    - For the discord token, it is not directly accessible inside the cookies so you will need to either inspect the network tab and find it inside a request or make this post request
    <br/>
    
    ```curl
    curl -X POST https://discord.com/api/v9/auth/login \
    -H "Content-Type: application/json" \
    -d '{"login": "YOUR EMAIL HERE", "password": "YOUR PASSWORD HERE"}'
    ```

    *I don't know yet if and when the discord expires, if it does I will update this and automatically fetch one using this request*

4. **Set how often you want it to sync**:

    The scripts is scheluded to run every hour, If you want to change it to something else you can refer to this [documentation](https://schedule.readthedocs.io/en/stable/index.html), and update it here
   
    ```py
    if __name__ == "__main__":
    schedule.every().hour.do(sync_study_hours)

    print("Scheduler started. Running every hour.")
    while True:
        schedule.run_pending()
        time.sleep(1)
    ```

6. **Build and Start the Services**:

    ```bash
    ./run_container.sh
    ```

    If you'r on a windows device, just copy the commands from run_container.sh, the same applies when you want to stop it

7. **Verify that the Services are Running**:

    ```bash
    docker-compose ps
    ```

8. **Stopping the Services**:

    ```bash
    ./stop_container.sh
    ```
