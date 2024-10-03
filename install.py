import subprocess
import os
import requests

# Set the url
url = 'https://cdimage.debian.org/debian-cd/current/amd64/iso-cd/debian-12.7.0-amd64-netinst.iso'

# Check iso
if os.path.exists("debian.iso"):
    print("okay continuing...")
else:
  print("downloading the things...")
  # Get the iso
  response = requests.get(url)

  # Write to file
  with open('debian.iso', 'wb') as file:
      file.write(response.content)


# Prompt the user for the device name
usb_device = input("Enter device name (eg. /dev/sdx): ")

# Set the Debian ISO file path
debian_iso = "debian.iso"

# Set the custom Neofetch file path
neofetch_file = "neofetch.txt"

# Set the custom wallpaper file path
wallpaper_file = "batarong.png"

# Create a bootable USB drive
subprocess.run(["dd", "if=" + debian_iso, "of=" + usb_device, "bs=4M", "status=progress"])

# Mount the USB drive
subprocess.run(["mkdir", "/mnt/usb"])
subprocess.run(["mount", usb_device + "1", "/mnt/usb"])

# Create a custom preseed file for auto-installation
preseed_file = """
d-i debian-installer/locale string en_US
d-i console-setup/ask_detect boolean false
d-i console-setup/layout string us
d-i netcfg/choose_interface select auto
d-i netcfg/disable_autoconfig boolean true
d-i netcfg/get_ipaddress string 192.168.1.100
d-i netcfg/get_netmask string 255.255.255.0
d-i netcfg/get_gateway string 192.168.1.1
d-i netcfg/get_nameservers string 8.8.8.8
d-i netcfg/confirm_static boolean true
d-i mirror/country string manual
d-i mirror/http/hostname string http.us.debian.org
d-i mirror/http/directory string /debian
d-i mirror/http/proxy string
d-i pkgsel/install-language-support boolean false
d-i tasksel/first multiselect xfce-desktop
d-i grub-installer/bootdev  string /dev/sda
d-i finish-install/reboot_required  boolean true
"""

with open("/mnt/usb/preseed.cfg", "w") as f:
    f.write(preseed_file)

# Create a custom late_command script to set the wallpaper and copy the Neofetch file
late_command = """
in-target sed -i 's|^wallpaper=.*|wallpaper=/batarong.png|' /etc/xdg/xfce4/xfconf/xfce-perchannel-xml/xfce4-desktop.xml
in-target cp /cdrom/neofetch.txt /root/.config/neofetch/config.conf
in-target chmod 777 /root/.config/neofetch/config.conf
in-target cp /cdrom/batarong /batarong
in-target chmod 777 /batarong
"""

with open("/mnt/usb/late_command.sh", "w") as f:
    f.write(late_command)

# Copy the custom Neofetch file and wallpaper to the USB drive
subprocess.run(["cp", neofetch_file, "/mnt/usb/neofetch.txt"])
subprocess.run(["cp", wallpaper_file, "/mnt/usb/batarong.png"])
subprocess.run(["cp", "batarong", "/mnt/usb/batarong"])

# Unmount the USB drive
subprocess.run(["umount", "/mnt/usb"])
