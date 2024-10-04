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
d-i netcfg/choose_interface select auto
d-i netcfg/disable_autoconfig boolean false
d-i netcfg/confirm_static boolean false
d-i mirror/country string manual
d-i mirror/http/directory string /debian
d-i pkgsel/install-language-support boolean false
d-i tasksel/first multiselect xfce-desktop
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
in-target rm -rf /etc/apt/sources.list && echo "deb http://deb.debian.org/debian/ stable main contrib non-free" >> /etc/apt/sources.list
in-target dpkg --add-architecture i386
in-target apt update
in-target apt install mesa-vulkan-drivers libglx-mesa0:i386 mesa-vulkan-drivers:i386 libgl1-mesa-dri:i386
in-target apt install steam-installer
in-target echo "done"
"""

with open("/mnt/usb/late_command.sh", "w") as f:
    f.write(late_command)

# Copy the custom Neofetch file and wallpaper to the USB drive
subprocess.run(["cp", neofetch_file, "/mnt/usb/neofetch.txt"])
subprocess.run(["cp", wallpaper_file, "/mnt/usb/batarong.png"])
subprocess.run(["cp", "batarong", "/mnt/usb/batarong"])

# Unmount the USB drive
subprocess.run(["umount", "/mnt/usb"])
