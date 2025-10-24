import subprocess
import shutil

def set_motd(host_ip, message):
    playbook_path = 'motd_playbook.yaml'
    inventory_path = 'hosts' # Define the path to the inventory file
    ansible_executable = shutil.which('ansible-playbook')
    
    if not ansible_executable:
        return "Error: 'ansible-playbook' command not found."

    command_args = [
        ansible_executable,
        "-i", inventory_path,
        playbook_path,
        "--limit", host_ip,
        "-e", f"motd_message='{message}'"
    ]
    