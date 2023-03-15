# pwnagotchi-plugins

# Custom Plugin Setup
If you have not set up a directory for custom plugins, create the directory:
```bash
sudo mkdir -p /usr/local/share/pwnagotchi/custom-plugins/
```

then add its path to your config.toml file located at `/etc/pwnagotchi/config.toml`:
`main.custom_plugins = "/usr/local/share/pwnagotchi/custom-plugins/"`

# BluetoothSniffer
A plugin for [pwnagotchi](https://github.com/evilsocket/pwnagotchi) that sniffs Bluetooth devices and saves their MAC addresses, name and counts to a JSON file.

## Requirements
- hcitools installed `sudo apt install -y bluez`

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
main.plugins.bluetoothsniffer.timer = 15 # On how may seconds to scan for bluetooth devices
main.plugins.bluetoothsniffer.devices_file = "/root/handshakes/bluetooth_devices.json"  # Path to the JSON file with bluetooth devices
main.plugins.bluetoothsniffer.devices_file = 86400 # On how may seconds to update count bluetooth devices
```
3. Restart your pwnagotchi to load the plugin.