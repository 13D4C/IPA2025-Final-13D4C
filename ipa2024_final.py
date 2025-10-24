import os
import time
import json
import requests
from dotenv import load_dotenv

# Import functions from other modules with aliases to avoid name conflicts
from restconf_final import create_interface as restconf_create, delete_interface as restconf_delete, enable_interface as restconf_enable, disable_interface as restconf_disable, get_interface_status as restconf_status
from netconf_final import create_interface as netconf_create, delete_interface as netconf_delete, enable_interface as netconf_enable, disable_interface as netconf_disable, get_interface_status as netconf_status

load_dotenv()
ACCESS_TOKEN = os.environ.get("WEBX_ACCESS_TOKEN")
ROOM_ID = os.environ.get("ROOM_ID")
STUDENT_ID = "66070216" # <-- Change this to your student ID
VALID_IPS = ["10.0.15.61", "10.0.15.62", "10.0.15.63", "10.0.15.64", "10.0.15.65"]

# A dictionary to store the last selected method for each user
user_states = {}

print("Bot is running... Waiting for commands.")
while True:
    time.sleep(1)
    get_parameters = {"roomId": ROOM_ID, "max": 1}
    http_headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

    try:
        response = requests.get("https://webexapis.com/v1/messages", params=get_parameters, headers=http_headers)
        response.raise_for_status()
        json_data = response.json()
        if not json_data.get("items"):
            continue

        latest_message = json_data["items"][0]
        person_id = latest_message.get("personId")
        
        # Ignore messages sent by the bot itself
        if latest_message.get("personEmail", "").endswith("@webex.bot"):
            continue

        message_text = latest_message.get("text", "")
        if not message_text.startswith(f"/{STUDENT_ID}"):
            continue

        print(f"Received command: {message_text}")
        parts = message_text.split()
        response_message = ""
        
        # --- Command Parsing Logic ---
        if len(parts) == 2:
            command = parts[1].lower()
            if command == "netconf":
                user_states[person_id] = "netconf"
                response_message = "Ok: Netconf"
            else:
                if not user_states.get(person_id):
                    response_message = "Error: No method specified"
                else:
                    response_message = "Error: No IP specified"
        
        elif len(parts) >= 3:
            target_ip, command = parts[1], parts[2].lower()
            selected_method = user_states.get(person_id)

            if target_ip not in VALID_IPS:
                response_message = f"Error: Invalid IP address {target_ip}"
            elif not selected_method and command not in ["motd"]:
                response_message = "Error: No method specified"
            else:
                if command in ["create", "delete", "enable", "disable", "status"]:
                    if selected_method == "netconf":
                        if command == "create": response_message = netconf_create(target_ip)
                        elif command == "delete": response_message = netconf_delete(target_ip)
                        elif command == "enable": response_message = netconf_enable(target_ip)
                        elif command == "disable": response_message = netconf_disable(target_ip)
                        elif command == "status": response_message = netconf_status(target_ip)
        else:
            response_message = "Error: No command specified"

        # Send the response back to the Webex room
        if response_message:
            post_headers = {"Authorization": f"Bearer {ACCESS_TOKEN}", "Content-Type": "application/json"}
            post_data = json.dumps({"roomId": ROOM_ID, "text": response_message})
            requests.post("https://webexapis.com/v1/messages", data=post_data, headers=post_headers).raise_for_status()
            print(f"Sent response: {response_message}")

    except Exception as e:
        print(f"An error occurred: {e}")