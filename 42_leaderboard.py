import requests
import json
import time
import os
from Loading import ft_tqdm


def get_users_data(token):

    base_url = "https://api.intra.42.fr/v2/campus/40/users"
    params = {
        "sort": "-updated_at",
        "filter[staff?]": "false",
        "page[size]": 100,
        "page[number]": 1
    }

    headers = {
        "Authorization": token
    }

    users_data = {}

    while params["page[number]"] < 6:
        response = requests.get(base_url, headers=headers, params=params)
        data = response.json()

        if response.status_code == 401:
            print(f"Authentication error: {response.status_code}")
            return None
        elif response.status_code != 200:
            print(f"Error: {response.status_code}")
            return None
        
        for user in data:
            users_data[user["login"]] = user["id"]
        
        params["page[number]"] += 1

    with open("42_user_list.txt", "w") as file:
        for login, user_id in users_data.items():
            file.write(f"{login}: {user_id}\n")

    print("User list saved in 42_user_list.txt")

    return users_data


def get_xp_data(token, users_data):

    base_url = f"https://api.intra.42.fr/v2/users/"

    headers = {
        "Authorization": token
    }

    user_levels = {}

    for login, user_id in ft_tqdm(users_data.items()):
        url = base_url + str(user_id)
        response = requests.get(url, headers=headers)

        time.sleep(1)

        while response.status_code == 429:
            print("Too many requests. Waiting before retrying...")
            time.sleep(5)
            response = requests.get(url, headers=headers)

        if response.status_code == 401:
            print(f"Authentication error: {response.status_code}")
            return None
        elif response.status_code != 200:
            print(f"Error: {response.status_code}")
            return None

        data = response.json()

        for cursus_user in data.get("cursus_users", []):
            if cursus_user.get("grade") in ["Member", "Learner"]:
                user_levels[login] = cursus_user.get("level")
                break
        
    sorted_user_levels = dict(sorted(user_levels.items(), key=lambda item: item[1], reverse=True))

    with open("42_LeaderBoard.txt", "w") as file:
        for login, level in sorted_user_levels.items():
            file.write(f"{login}: {level}\n")

    print("42_LeaderBoard.txt created")
    return sorted_user_levels


def get_access_token():
    url = "https://api.intra.42.fr/oauth/token"

    # Replace the values with your UID and Secret from your registered 42 app
    uid = ""
    secret = ""
    
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


if __name__ == "__main__":

    token = "Bearer " + get_access_token()

    print("\n\033[1mPress 1, 2 or 3 to choose an option:\n\033[0m")
    print("\033[94m1\033[0m Get user the Leaderboard without intermediate steps. This may take a while...\n")
    print("\033[94m2\033[0m Use local 42_user_list.txt file if you already have one\n")
    print("\033[94m3\033[0m Get 42_user_list.txt file. You can edit the list and make it shorter to avoid too many requests. Do it at your own risk\n")

    option = input()
    if option == "1":
        users_data = get_users_data(token)
    elif option == "2":
        filename = "42_user_list.txt"
        if os.path.exists(filename) and os.access(filename, os.R_OK):		
            try:
                with open(filename, "r") as file:
                    users_data = {}
                    for line in file:
                        login, user_id = line.split(": ")
                        users_data[login] = int(user_id)
            except Exception as e:
                print("Error: ", e)
        else:
            print("File not found or not readable")
            exit()
    elif option == "3":
        users_data = get_users_data(token)
        exit()
    else:
        print("Invalid option")
        exit()

    if users_data:
        get_xp_data(token, users_data)
    
