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
    
    try:
        process = subprocess.run(command_args, capture_output=True, text=True, check=True, timeout=90)
        
        # We only care that the command succeeded (failed=0).
        if 'failed=0' in process.stdout:
            print("Ansible MOTD command successful.")
            return "Ok: success"
        else:
            print(f"Ansible MOTD command failed. Output:\n{process.stdout}\n{process.stderr}")
            return "Error: Failed to set MOTD via Ansible."
            
    except subprocess.CalledProcessError as e:
        print(f"Ansible execution failed:\nSTDOUT: {e.stdout}\nSTDERR: {e.stderr}")
        return f"Error: Ansible execution failed. Check logs."
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return f"An unexpected error occurred: {e}"
