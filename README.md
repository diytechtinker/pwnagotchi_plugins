# pwnagotchi-plugins

# Custom Plugin Setup
If you have not set up a directory for custom plugins, create the directory:
```bash
sudo mkdir -p /usr/local/share/pwnagotchi/custom-plugins/
```

then add its path to your config.toml file located at `/etc/pwnagotchi/config.toml`:
```toml
main.custom_plugins = "/usr/local/share/pwnagotchi/custom-plugins/"
```

# BluetoothSniffer
![Alt text](https://github.com/diytechtinker/pwnagotchi_plugins/blob/main/Pwnagotchi_ha-pwny.jpg)

A plugin for [pwnagotchi](https://github.com/evilsocket/pwnagotchi) that sniffs Bluetooth devices and saves their MAC addresses, name and counts to a JSON file.

## Requirements
- Make sure hcitool is installed:
```bash
sudo apt install -y bluez
```

## Setup
1. Clone this repo onto your pwnagotchi and move to the repo directory
```bash
git clone https://github.com/diytechtinker/pwnagotchi_plugins.git
cd pwnagotchi_plugins/
```

2. Copy over `bluetoothsniffer.py` into your custom plugins directory.
```bash
sudo cp bluetoothsniffer.py /usr/local/share/pwnagotchi/custom-plugins/bluetoothsniffer.py
```

3. In your `config.toml` file, add:
```toml
main.plugins.bluetoothsniffer.enabled = true
main.plugins.bluetoothsniffer.timer = 45 # On how may seconds to scan for bluetooth devices
main.plugins.bluetoothsniffer.devices_file = "/root/handshakes/bluetooth_devices.json"  # Path to the JSON file with bluetooth devices
main.plugins.bluetoothsniffer.count_interval = 86400 # On how may seconds to update count bluetooth devices
main.plugins.bluetoothsniffer.bt_x_coord = 160
main.plugins.bluetoothsniffer.bt_y_coord = 66
```
4. Restart your pwnagotchi to load the plugin.
```bash
systemctl restart pwnagotchi
```