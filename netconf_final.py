from ncclient import manager
import os
from dotenv import load_dotenv
import xml.etree.ElementTree as ET

load_dotenv()
ROUTER_USER = os.environ.get("ROUTER_USER")
ROUTER_PASS = os.environ.get("ROUTER_PASS")
STUDENT_ID = "66070216"
INTERFACE_NAME = f"Loopback{STUDENT_ID}"

# Helper to connect to the specified router IP
def _connect(host_ip):
    return manager.connect(host=host_ip, port=830, username=ROUTER_USER, password=ROUTER_PASS, hostkey_verify=False, timeout=10)

def create_interface(host_ip):
    config_xml = f"""<config><interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces"><interface><name>{INTERFACE_NAME}</name><type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">ianaift:softwareLoopback</type><enabled>true</enabled><ipv4 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip"><address><ip>172.2.16.1</ip><netmask>255.255.255.0</netmask></address></ipv4></interface></interfaces></config>"""
    try:
        with _connect(host_ip) as m:
            reply = m.edit_config(target="running", config=config_xml)
            if "<ok/>" in str(reply): return f"Interface loopback {STUDENT_ID} is created successfully using Netconf"
        return f"Cannot create: Interface loopback {STUDENT_ID}"
    except: return f"Cannot create: Interface loopback {STUDENT_ID}"

def delete_interface(host_ip):
    config_xml = f"""<config><interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces"><interface operation="delete"><name>{INTERFACE_NAME}</name></interface></interfaces></config>"""
    try:
        with _connect(host_ip) as m:
            reply = m.edit_config(target="running", config=config_xml)
            if "<ok/>" in str(reply): return f"Interface loopback {STUDENT_ID} is deleted successfully using Netconf"
        return f"Cannot delete: Interface loopback {STUDENT_ID}"
    except: return f"Cannot delete: Interface loopback {STUDENT_ID}"

def enable_interface(host_ip):
    config_xml = f"""<config><interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces"><interface><name>{INTERFACE_NAME}</name><enabled>true</enabled></interface></interfaces></config>"""
    try:
        with _connect(host_ip) as m:
            reply = m.edit_config(target="running", config=config_xml)
            if "<ok/>" in str(reply): return f"Interface loopback {STUDENT_ID} is enabled successfully using Netconf"
        return f"Cannot enable: Interface loopback {STUDENT_ID}"
    except: return f"Cannot enable: Interface loopback {STUDENT_ID}"

def disable_interface(host_ip):
    config_xml = f"""<config><interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces"><interface><name>{INTERFACE_NAME}</name><enabled>false</enabled></interface></interfaces></config>"""
    try:
        with _connect(host_ip) as m:
            reply = m.edit_config(target="running", config=config_xml)
            if "<ok/>" in str(reply): return f"Interface loopback {STUDENT_ID} is shutdowned successfully using Netconf"
        return f"Cannot shutdown: Interface loopback {STUDENT_ID}"
    except: return f"Cannot shutdown: Interface loopback {STUDENT_ID}"

def get_interface_status(host_ip):
    filter_xml = f"""<filter><interfaces-state xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces"><interface><name>{INTERFACE_NAME}</name></interface></interfaces-state></filter>"""
    try:
        with _connect(host_ip) as m:
            reply = m.get(filter=filter_xml)
            root = ET.fromstring(reply.xml)
            ns = {'if-state': 'urn:ietf:params:xml:ns:yang:ietf-interfaces'}
            admin_status = root.find('.//if-state:admin-status', ns)
            if admin_status is not None:
                status = "enabled" if admin_status.text == 'up' else "disabled"
                return f"Interface loopback {STUDENT_ID} is {status} (checked by Netconf)"
        return f"No Interface loopback {STUDENT_ID} (checked by Netconf)"
    except: return f"No Interface loopback {STUDENT_ID} (checked by Netconf)"