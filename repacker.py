from helper import *
import argparse
import sys
import random
import json
import re

def print_logo():
    print("""
    ____       ____             __            
   / __ \___  / __ \____ ______/ /_____  _____
  / /_/ / _ \/ /_/ / __ `/ ___/ //_/ _ \/ ___/
 / _, _/  __/ ____/ /_/ / /__/ ,< /  __/ /    
/_/ |_|\___/_/    \__,_/\___/_/|_|\___/_/  V0.1   
                                              
""")

def prepare_args():
    parser = argparse.ArgumentParser(description='RePacker is a utility designed to reconstruct Cordova applications that incorporate RASP or other protective measures within their native code, resulting in a sanitized application devoid of any such security measures.')
    parser.add_argument('application_file', type=str,
                    help='a path of application that you want to rebuild (ipa or apk file)')
    return parser.parse_args()

def main():
    print_logo()
    args = prepare_args()

    if not check_cordova():
        print("[-] Cordova not installed.")
        sys.exit()

    platform = input("[*] Platform (ios, android): ")
    if not platform in ["ios", "android"]:
        print("[-] Enter valid platform.")
        sys.exit()
    
    temp_out = 'temp_' + ''.join(random.choices(string.ascii_lowercase, k=12))

    new_out = "".join(re.findall("[a-zA-Z]+", args.application_file.split(".")[0])) + "_" + ''.join(random.choices(string.ascii_lowercase, k=5))

    newapp = rebuilder(args.application_file, platform, temp_out, new_out)

    print("[+] Extracting your app...")
    newapp.unpack()

    print("[+] Getting app plugins...")
    plugins = newapp.get_plugins().to_dict()

    print("[+] Creating new cordova application...")
    newapp.new_cordova()

    print("[+] Moving original application source code...")
    newapp.move_files()

    print("[+] Cleaning...")
    newapp.clean_tmp()

    input(f"[*] Edit config.xml in {new_out}/ReApp/config.xml then press Enter to continue. (If you don't know just press Enter :D)")

    print(f"[+] Adding {platform} platform...")
    newapp.add_platform()

    iap = input("[*] Do you want to install all plugins? (Y, n): ")
    if iap == "n":
        print("[+] All plugins:")
        for plugin in plugins:
            print(f"\t- {plugin}")

        unwanted_plugins = input("[*] Choose plugins that you don't want to install (support multi-choice by sperating them by comma ','): ")
        for p in unwanted_plugins.split(","):
            p = p.strip()
            del plugins[p]

    print("[+] Installing plugins...")
    for plugin in plugins:
        print(f"\t- Installing {plugin}@{plugins[plugin]}")
        newapp.install_plugin(f"{plugin}@{plugins[plugin]}")

    print("[+] Preparing new application...")
    newapp.cordova_prepare()

    if platform == "ios":
        print("[+] Xcode will open to select signing profile")
        print("\t - Steps:")
        print("\t\t 1- Select ReApp from left panel")
        print("\t\t 2- Select Signing & Capabilities")
        print("\t\t 3- In debug section, select your account in Team")
        print("\t\t 4- close Xcode")
        newapp.open_project()
        input("[*] Press Enter when you finish.")

    print("[+] Building the new application...")
    newapp.cordova_build()
    

if __name__ == "__main__":
    main()