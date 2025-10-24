import os
import json
import requests
from dotenv import load_dotenv

requests.packages.urllib3.disable_warnings()
load_dotenv()

ROUTER_USER = os.environ.get("ROUTER_USER", "admin")
ROUTER_PASS = os.environ.get("ROUTER_PASS", "cisco")
STUDENT_ID = "66070216"
INTERFACE_NAME = f"Loopback{STUDENT_ID}"
HEADERS = {"Accept": "application/yang-data+json", "Content-Type": "application/yang-data+json"}

# Helper to generate URLs dynamically based on the target IP
def _get_urls(host_ip):
    base_url = f"https://{host_ip}/restconf/data/ietf-interfaces:interfaces"
    interface_url = f"{base_url}/interface={INTERFACE_NAME}"
    state_url = f"https://{host_ip}/restconf/data/ietf-interfaces:interfaces-state/interface={INTERFACE_NAME}"
    return interface_url, state_url

def create_interface(host_ip):
    interface_url, _ = _get_urls(host_ip)
    payload = { "ietf-interfaces:interface": { "name": INTERFACE_NAME, "type": "iana-if-type:softwareLoopback", "enabled": True, "ietf-ip:ipv4": { "address": [{"ip": "172.2.16.1", "netmask": "255.255.255.0"}] } } }
    try:
        response = requests.put(interface_url, data=json.dumps(payload), auth=(ROUTER_USER, ROUTER_PASS), headers=HEADERS, verify=False, timeout=10)
        if response.status_code == 201: return f"Interface loopback {STUDENT_ID} is created successfully using Restconf"
        return f"Cannot create: Interface loopback {STUDENT_ID}"
    except: return f"Cannot create: Interface loopback {STUDENT_ID}"

def delete_interface(host_ip):
    interface_url, _ = _get_urls(host_ip)
    try:
        response = requests.delete(interface_url, auth=(ROUTER_USER, ROUTER_PASS), headers=HEADERS, verify=False, timeout=10)
        if response.status_code == 204: return f"Interface loopback {STUDENT_ID} is deleted successfully using Restconf"
        return f"Cannot delete: Interface loopback {STUDENT_ID}"
    except: return f"Cannot delete: Interface loopback {STUDENT_ID}"

def enable_interface(host_ip):
    interface_url, _ = _get_urls(host_ip)
    payload = {"ietf-interfaces:interface": {"name": INTERFACE_NAME, "enabled": True}}
    try:
        response = requests.patch(interface_url, data=json.dumps(payload), auth=(ROUTER_USER, ROUTER_PASS), headers=HEADERS, verify=False, timeout=10)
        if response.status_code == 204: return f"Interface loopback {STUDENT_ID} is enabled successfully using Restconf"
        return f"Cannot enable: Interface loopback {STUDENT_ID}"
    except: return f"Cannot enable: Interface loopback {STUDENT_ID}"

def disable_interface(host_ip):
    interface_url, _ = _get_urls(host_ip)
    payload = {"ietf-interfaces:interface": {"name": INTERFACE_NAME, "enabled": False}}
    try:
        response = requests.patch(interface_url, data=json.dumps(payload), auth=(ROUTER_USER, ROUTER_PASS), headers=HEADERS, verify=False, timeout=10)
        if response.status_code == 204: return f"Interface loopback {STUDENT_ID} is shutdowned successfully using Restconf"
        return f"Cannot shutdown: Interface loopback {STUDENT_ID}"
    except: return f"Cannot shutdown: Interface loopback {STUDENT_ID}"

def get_interface_status(host_ip):
    _, state_url = _get_urls(host_ip)
    try:
        response = requests.get(state_url, auth=(ROUTER_USER, ROUTER_PASS), headers=HEADERS, verify=False, timeout=10)
        if response.status_code == 200:
            status = "enabled" if response.json().get("ietf-interfaces:interface", {}).get("admin-status") == 'up' else "disabled"
            return f"Interface loopback {STUDENT_ID} is {status} (checked by Restconf)"
        return f"No Interface loopback {STUDENT_ID} (checked by Restconf)"
    except: return f"No Interface loopback {STUDENT_ID} (checked by Restconf)"