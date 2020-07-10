# Voltorb: Basic Undervolting GUI for Linux
<img src="https://raw.githubusercontent.com/egeoz/Voltorb/master/Screenshot.png" alt="Main window of Voltorb" width="480" height="500">

#### Features:
- Profile and general modes.
- Automatic undervolting at boot and battery/AC depending on the profile settings.

#### Requirements
- An Intel CPU that is 4th generation and newer(Haswell).
- PyQt5
- acpi
- [undervolt](https://github.com/georgewhewell/undervolt) (The installation script automatically installs undervolt)

#### Installation
```
chmod +x install.sh
sudo ./install.sh
```

#### Uninstallation
```
chmod +x uninstall.sh
sudo ./uninstall.sh
```

#### TODO
- Support for init systems other than systemd
- Stress test
- setup.py
- Ubuntu and AUR packagee
