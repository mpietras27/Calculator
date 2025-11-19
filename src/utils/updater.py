"""import requests
import subprocess
import sys
from packaging import version

# UPDATE THIS AFTER CREATING YOUR GITHUB REPO
GITHUB_REPO = "mpiet/Calculator"
CURRENT_VERSION = "1.0.0"

def get_latest_release():
    #Fetch latest version tag + download URL from GitHub Releases.
    url = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
    
    try:
        r = requests.get(url, timeout=4)
    except:
        return None, None

    if r.status_code != 200:
        return None, None

    data = r.json()
    latest_version = data["tag_name"]

    # Look for an .exe asset
    download_url = None
    for asset in data.get("assets", []):
        if asset["name"].endswith(".exe"):
            download_url = asset["browser_download_url"]
            break

    return latest_version, download_url

def check_for_update():
    #Check if a GitHub Release version is newer than CURRENT_VERSION.
    latest_version, download_url = get_latest_release()
    if not latest_version:
        return False, None

    if version.parse(latest_version) > version.parse(CURRENT_VERSION):
        return True, download_url

    return False, None

def apply_update(download_url):
    #Download new EXE, replace current EXE, and relaunch.
    exe_path = sys.argv[0]
    new_path = exe_path + ".new"

    r = requests.get(download_url)
    with open(new_path, "wb") as f:
        f.write(r.content)

    # Replace EXE after closing
    subprocess.Popen([
        "cmd", "/c",
        f"ping 127.0.0.1 -n 2 > nul & move /Y \"{new_path}\" \"{exe_path}\" & start \"\" \"{exe_path}\""
    ])

    sys.exit()"""


import os
import requests
import shutil
from pathlib import Path
from utils.version import APP_VERSION

# --- GitHub Repo Info ---
GITHUB_OWNER = "YOUR_GITHUB_USERNAME"   # <-- REPLACE THIS
GITHUB_REPO = "Calculator"              # <-- REPLACE THIS EXACTLY

LATEST_RELEASE_URL = (
    f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/releases/latest"
)


def check_for_update():
    """
    Returns (True, download_url) if a newer version exists, otherwise (False, None).
    Always fails silently on network error.
    """
    try:
        response = requests.get(LATEST_RELEASE_URL, timeout=5)
        if response.status_code != 200:
            return False, None

        data = response.json()
        latest_version = data["tag_name"].lstrip("v")

        if latest_version == APP_VERSION:
            return False, None  # Already up-to-date

        # Look for a .exe file in the release assets
        for asset in data["assets"]:
            if asset["name"].endswith(".exe"):
                return True, asset["browser_download_url"]

        return False, None

    except Exception:
        return False, None  # Silent fail (offline, timeout, etc.)


def apply_update(download_url):
    """
    Downloads the new .exe into ./updates/ folder.
    Does not replace running EXE — replacement occurs at next launch.
    """
    try:
        updates_dir = Path("updates")
        updates_dir.mkdir(exist_ok=True)

        exe_name = os.path.basename(download_url)
        download_path = updates_dir / exe_name

        print(f"Downloading update → {download_path}")

        with requests.get(download_url, stream=True) as req:
            req.raise_for_status()
            with open(download_path, "wb") as f:
                shutil.copyfileobj(req.raw, f)

        print("Update downloaded. It will be applied on next launch.")

    except Exception as e:
        print(f"Update failed: {e}")