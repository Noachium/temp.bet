import os
import sys
import shutil
import subprocess
import winreg
import ctypes
import time

# ---- Logging ----
log_file = os.path.join(os.environ.get('LOCALAPPDATA', os.path.expanduser('~')), 'EAC_Bypass.log')
def log(msg):
    try:
        with open(log_file, 'a') as f:
            f.write(time.strftime('%H:%M:%S') + ' ' + msg + '\n')
    except:
        pass

log('=== EAC Bypass started ===')
try:
    import psutil
except ImportError:
    log('Installing psutil...')
    subprocess.check_call([sys.executable, "-m", "pip", "install", "psutil"])
    import psutil
    log('psutil installed')

def get_steam_libraries():
    try:
        steam_path = winreg.QueryValueEx(
            winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam"),
            "SteamPath"
        )[0]
    except:
        log('Steam path not found in registry')
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
    log('Steam libraries: ' + str(libs))
    return libs

GAME_DIR = None
for lib in get_steam_libraries():
    path = os.path.join(lib, "steamapps", "common", "Animal Company")
    if os.path.isdir(path):
        GAME_DIR = path
        break

log('GAME_DIR = ' + str(GAME_DIR))
if not GAME_DIR:
    log('Game directory not found – exiting')
    sys.exit(0)

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
    log('Injecting: frida -l ' + bridge_path + ' -l ' + script_path + ' EACLauncher.exe')
    try:
        subprocess.Popen(
            [
                "frida",
                "-l", bridge_path,
                "-l", script_path,
                "EACLauncher.exe"
            ],
            creationflags=subprocess.CREATE_NO_WINDOW,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return True
    except Exception as e:
        log('Inject failed: ' + str(e))
        return False

def main():
    eac_exe = os.path.join(GAME_DIR, "EACLauncher.exe")
    game_exe = os.path.join(GAME_DIR, "AnimalCompany.exe")
    eac_data = os.path.join(GAME_DIR, "EACLauncher_Data")
    game_data = os.path.join(GAME_DIR, "AnimalCompany_Data")

    log('Checking files...')
    if os.path.exists(game_exe):
        if os.path.exists(eac_exe):
            try:
                os.remove(eac_exe)
                log('Removed existing EACLauncher.exe')
            except Exception as e:
                log('Failed to remove EACLauncher.exe: ' + str(e))
        if os.path.exists(game_exe) and not os.path.exists(eac_exe):
            os.rename(game_exe, eac_exe)
            log('Renamed AnimalCompany.exe -> EACLauncher.exe')
        if os.path.exists(game_data) and not os.path.exists(eac_data):
            os.rename(game_data, eac_data)
            log('Renamed AnimalCompany_Data -> EACLauncher_Data')
    else:
        log('AnimalCompany.exe not found, skipping rename')

    injected = False
    while True:
        if not injected and is_process_running("EACLauncher.exe"):
            log('EACLauncher.exe detected, injecting...')
            time.sleep(1)
            if inject_frida():
                injected = True
                log('Injection successful')
                break
        time.sleep(0.5)

if __name__ == "__main__":
    main()
