import psutil
import webbrowser
import os
import urllib.request
import sys
import zipfile
import subprocess
import shutil
import json
import time
import fileinput
def progressbar(prcnt, title):
    print("\n" * 9001)
    print("\n")
    print(title)
    print("\n")
    print("--------------------------------------------------------------------------------------------------------------------")
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    print('['+('=' * prcnt)+']' + '(' + str(prcnt) + '%)')
def restart_script():
    python_executable = sys.executable
    script_path = os.path.abspath(__file__)
    subprocess.call([python_executable, script_path])
def aroma_inst():
    print("\nInstalling Aroma\n\n--------------------------------------------------------------------------------------------------------------------\n")
    time.sleep(1)
    # "We have ttk.Progressbar at home" ttk.Progressbar at home:
    progressbar(0, "Installing Aroma")

    release_url = "https://api.github.com/repos/wiiu-env/Aroma/releases/latest"
    response = urllib.request.urlopen(release_url)
    release_data = response.json()

    download_url = release_data["assets"][0]["browser_download_url"]

    print(download_url)

    zip_filename = "aroma.zip"
    urllib.request.urlretrieve(download_url, zip_filename)

    with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
        total_files = len(zip_ref.namelist())
        for index, file in enumerate(zip_ref.namelist(), start=1):
            progressbar(((index / total_files) * 100), "Installing Aroma")
            zip_ref.extract(file, sd_path)

    updater_path = os.path.join(sd_path, 'wiiu', 'apps', 'AromaUpdater.wuhb')
    if not os.path.exists(updater_path):
        print("\nAroma Installation Unsuccessful\n--------------------------------------------------------------------------------------------------------------------")
        print()
        retry = input("Either there is no WiFi connection, the aroma repository is down, or the SD card is corrupted. Retry the process? [y or n]")
        if retry == 'y':
            aroma_inst()
        if retry == 'n':
            manual = input("Would you like to install Aroma manually, instead of doing it automatically? [y or n]")
            if manual == 'y':
                webbrowser.open("https://aroma.foryour.cafe/")
            if manual == 'n':
                sys.exit
    else:
        print("\n" * 9001)
        print("The automated process was successful. AromaPy will now restart.")
        time.sleep(10)
        python = sys.executable
        os.execl(python, python, *sys.argv)
def appstore_inst():
    print("\nInstalling Appstore\n\n--------------------------------------------------------------------------------------------------------------------\n")
    time.sleep(1)
    progressbar(0, "Installing Appstore")

    release_url = "https://api.github.com/repos/fortheusers/hb-appstore/releases/latest"
    response = urllib.request.urlopen(release_url)
    
    response_content = response.read()  # Read the response content
    release_data = json.loads(response_content)  # Parse the JSON content

    download_url = release_data["assets"][2]["browser_download_url"]  # Third package contains .wuhb file as of now

    print(download_url)

    wuhb_filename = "appstore.wuhb"
    urllib.request.urlretrieve(download_url, wuhb_filename)

    # Move appstore.wuhb to sd:/wiiu/apps/appstore/appstore.wuhb
    appstore_dir = os.path.join(sd_path, 'wiiu', 'apps', 'appstore')
    os.makedirs(appstore_dir, exist_ok=True)  # Create directory if it doesn't exist
    destination_path = os.path.join(appstore_dir, 'appstore.wuhb')
    shutil.move(wuhb_filename, destination_path)

    appstore_path = os.path.join(sd_path, 'wiiu', 'apps', 'appstore', 'appstore.wuhb')
    if not os.path.exists(appstore_path):
        print("\nApp Store Installation Unsuccessful\n--------------------------------------------------------------------------------------------------------------------")
        print()
        retry = input("Either there is no WiFi connection, the appstore repository is down, or the SD card is corrupted. Retry the process? [y or n]")
        if retry == 'yes':
            appstore_inst()
        if retry == 'no':
            manual = input("Would you like to install the app store manually, instead of doing it automatically? (You will have to manually download appstore.wuhb from the latest version and move it to /wiiu/apps/appstore/)")
            if manual == 'yes':
                webbrowser.open("https://github.com/fortheusers/hb-appstore/releases/")
            if manual == 'no':
                restart_script()
    else:
        print("\n" * 9001)
        print("The automated process was successful. AromaPy will now restart.")
        time.sleep(10)
        python = sys.executable
        os.execl(python, python, *sys.argv)

print("\nSD Card Drive Selection\n\n--------------------------------------------------------------------------------------------------------------------")
print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
drives = psutil.disk_partitions()
other_drives = [drive.device for drive in drives if drive.device != 'C:\\']
if len(other_drives) == 1: 
    sd_path = str(other_drives[0])
else:    
    index = -1
    for drv in other_drives:
        index = index + 1
        print(other_drives[index])
    sd_path = str((input("Please input drive letter for SD card.\n>>>")).upper() + ":\\")

aroma_path = os.path.join(sd_path, 'wiiu', 'environments', 'aroma')
payload_path = os.path.join(sd_path, 'wiiu', 'payloads', 'default')
tiramisu_path = os.path.join(sd_path, 'wiiu', 'environments', 'tiramisu')

if os.path.exists(aroma_path):
    pass
elif os.path.exists(payload_path) or os.path.exists(tiramisu_path):
    result = input("\nAroma Not Installed\n\n--------------------------------------------------------------------------------------------------------------------\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nAroma is not installed on the Wii U. Do you want to install it? [y or n]\n>>>")
    if result == 'y':
        subresult = input("\nAutomated Process\n\n--------------------------------------------------------------------------------------------------------------------\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nWould you like to use the automated process to install basic Aroma features onto the SD card? [y or n]\n>>>")
        if subresult == 'y':
            aroma_inst()  # Start the installation process
        if subresult == 'n':
            webbrowser.open("https://aroma.foryour.cafe/")
    if result == 'n':
        sys.exit()
else:
    result = input("\nSD Card Issue\n\n--------------------------------------------------------------------------------------------------------------------\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nEither the SD card is corrupted or softmods are not installed on the Wii U. Do you want to follow a modding tutorial and install Aroma? [y or n]\n>>>")
    if result == 'yes':
        webbrowser.open("https://aroma.foryour.cafe/")
        webbrowser.open("https://wiiu.hacks.guide/")
print(f"\nMain Menu\n")
print("--------------------------------------------------------------------------------------------------------------------")
mainmenuvalues = [
    "(Re)Install App Store",
    "Plugin Installer"
]

num = 0
for _ in range(len(mainmenuvalues)):
    num += 1
    item = mainmenuvalues[num - 1]
    print(f"{num}: {item}")
for dummy in range(24 - len(mainmenuvalues)):
    print("")
optsel = input("Enter your choice\n>>>")
if optsel == "1":
    appstore_path = os.path.join(sd_path, 'wiiu', 'apps', 'appstore', 'appstore.wuhb')
    if os.path.exists(appstore_path):
        os.remove(appstore_path)
    else:
        result = input("\nInstall Appstore?\n\n--------------------------------------------------------------------------------------------------------------------\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nWould you like to install the app store onto the Wii U? [y or n]\n>>>")
        if result == 'y':
            appstore_inst()
if optsel == '2':
    print("\nHAIIIIII :3\n\n--------------------------------------------------------------------------------------------------------------------\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nyeah so normally this would let you open file explorer get a wps wms whatever file and it would move it to its corresponding location\ni suck at coding so i didnt have time to implement this")
    time.sleep(999)
