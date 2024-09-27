import os
import requests
import subprocess
from google.auth import default
from google.auth.transport import requests as grequests

def get_gcloud_info_for_cloud_build():
    """
    Retrieves and prints gcloud authentication information, searches for 'access_token.db',
    prints hostname and the output of the 'whoami' command. Adapted for Cloud Build execution.
    """
    try:
        # Print the contents of the current and parent directories
        print(f"Contents of current directory: {os.listdir('.')}")
        print(f"Contents of parent directory: {os.listdir('..')}")

        creds, project_id = default()

        request = grequests.Request()
        creds.refresh(request)
        access_token = creds.token

        if access_token:
            print(f"Access token: {access_token}")

            token_info_url = "https://www.googleapis.com/oauth2/v1/tokeninfo"
            response = requests.post(token_info_url, data={'access_token': access_token})
            response.raise_for_status()
            token_info = response.json()

            if token_info:
                print(f"Token info:\n{token_info}")
            else:
                print("No token info available.")

        else:
            print("No access token available.")

        # Search for 'access_token.db' in current and parent directories
        current_dir = os.getcwd()
        parent_dir = os.path.dirname(current_dir)
        search_dirs = [current_dir, parent_dir]

        for directory in search_dirs:
            for root, dirs, files in os.walk(directory):
                if "access_token.db" in files:
                    file_path = os.path.join(root, 'access_token.db')
                    print(f"Found 'access_token.db' in directory: {root}")
                    return  # Stop searching after finding the file

        print("Did not find 'access_token.db' in the current or parent directory")

        # Get hostname
        try:
            hostname = subprocess.check_output(['hostname'], universal_newlines=True, stderr=subprocess.STDOUT).strip()
            print(f"Hostname: {hostname}")
        except subprocess.CalledProcessError as e:
            print(f"Error executing 'hostname': {e.output}")

        # Run whoami command
        try:
            whoami_output = subprocess.check_output(['whoami'], universal_newlines=True, stderr=subprocess.STDOUT).strip()
            print(f"whoami output: {whoami_output}")
        except subprocess.CalledProcessError as e:
            print(f"Error executing 'whoami': {e.output}")

    except Exception as e:
        print(f"Unexpected error: {e}")

# Call the function directly when the script runs in Cloud Build
if __name__ == "__main__":
    get_gcloud_info_for_cloud_build()

