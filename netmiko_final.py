import os
from netmiko import ConnectHandler
from dotenv import load_dotenv
import re # Import the regular expression module

load_dotenv()
ROUTER_USER = os.environ.get("ROUTER_USER")
ROUTER_PASS = os.environ.get("ROUTER_PASS")

def get_motd(host_ip):

    device_params = {
        "device_type": "cisco_ios", "host": host_ip,
        "username": ROUTER_USER, "password": ROUTER_PASS,
    }
    try:
        with ConnectHandler(**device_params) as connection:
            # Fetch the entire running configuration for reliable parsing
            running_config = connection.send_command("show running-config", use_textfsm=False)
            
            match = re.search(r"banner motd (.)(.*?)\1", running_config, re.DOTALL)
            
            if match:
                # The actual message is the second captured group
                return match.group(2)
            else:
                return "Error: No MOTD Configured"
            
    except Exception as e:
        return f"Error connecting or reading MOTD: {e}"