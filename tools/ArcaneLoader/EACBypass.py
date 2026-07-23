import os
import sys
import shutil
import subprocess
import winreg
import ctypes
import time

try:
    import psutil
except ImportError:
    print("Installing psutil...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "psutil"])
    import psutil

def get_steam_libraries():
    try:
        steam_path = winreg.QueryValueEx(
            winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam"),
            "SteamPath"
        )[0]
    except:
        return []

    libs = [steam_path]

    vdf = os.path.join(steam_path, "steamapps", "libraryfolders.vdf")
    if os.path.exists(vdf):
        with open(vdf, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                if '"path"' in line:
                    parts = line.split('"')
                    if len(parts) > 3:
                        libs.append(parts[3].replace("\\\\", "\\"))

    return libs

GAME_DIR = next(
    (
        os.path.join(lib, "steamapps", "common", "Animal Company")
        for lib in get_steam_libraries()
        if os.path.isdir(os.path.join(lib, "steamapps", "common", "Animal Company"))
    ),
    None
)

def is_process_running(name):
    for proc in psutil.process_iter(['name']):
        try:
            if proc.info['name'].lower() == name.lower():
                return True
        except:
            pass
    return False

def inject_frida():
    script_path = os.path.join(os.path.dirname(__file__), "Bypass.js")
    bridge_path = os.path.join(os.path.dirname(__file__), "frida-il2cpp-bridge.js")

    try:
        subprocess.Popen(
            [
                "frida",
                "-l", bridge_path,
                "-l", script_path,
                "EACLauncher.exe"
            ],
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        return True
    except Exception as e:
        return False

def main():
    os.system("cls")

    if not GAME_DIR:
        return

    eac_exe = os.path.join(GAME_DIR, "EACLauncher.exe")
    game_exe = os.path.join(GAME_DIR, "AnimalCompany.exe")
    eac_data = os.path.join(GAME_DIR, "EACLauncher_Data")
    game_data = os.path.join(GAME_DIR, "AnimalCompany_Data")

    if os.path.exists(game_exe):
        if os.path.exists(eac_exe):
            try:
                os.remove(eac_exe)
            except:
                pass

        if os.path.exists(game_exe) and not os.path.exists(eac_exe):
            os.rename(game_exe, eac_exe)
        
        if os.path.exists(game_data) and not os.path.exists(eac_data):
            os.rename(game_data, eac_data)
        
    injected = False
    while True:
        if not injected and is_process_running("EACLauncher.exe"):
            time.sleep(1)
            if inject_frida():
                injected = True
                break
        time.sleep(0.5)

if __name__ == "__main__":
    main()
