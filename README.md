With this script you'll get the 42Urduliz campus leaderboard

Open a terminal and paste/run this command:

    https://github.com/tentaclepurple/42_urduliz_leaderboard.git

In order to make it work you'll need to register your own app so you can use 42 API.

To do that go to your 42 intra -> Settings -> API -> Register new app 

Just choose a **name** for your app and a valid url in **redirect url** (doesn´t matter what as you'll not use it this time)

Click **submit**

Now that you have your UID and SECRET put them in the appropiate place of the 42_leaderboard.py code:

It should look like this:

    def get_access_token():
        url = "https://api.intra.42.fr/oauth/token"
    
        # Replace the values with your UID and Secret from your 42 registered app
        uid = "u-s4t2ud-ca8799da64518f941f7a66f9693a5c426aa78da783ba9eec6cf79dee98371b"
        secret = "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"
        
        if not uid or not secret:
            print("Missing UID or Secret. Line 98 in 42_leaderboard.py")
            exit()
        data = {
            "grant_type": "client_credentials",
            "client_id": uid,
            "client_secret": secret
        }
    
        response = requests.post(url, data=data)
        
        if response.status_code == 200:
            access_token = response.json().get("access_token")
            return access_token
        else:
            print(f"Error: {response.status_code}")
            return None


Now run:

    python3 42_leaderboard.py
