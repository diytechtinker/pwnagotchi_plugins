import logging
import os
import subprocess
import json
import re
import time
from pwnagotchi import plugins, ui

class BluetoothSniffer(plugins.Plugin):
    __author__ = 'diytechtinker'
    __version__ = '0.1.0'
    __license__ = 'GPL3'
    __description__ = 'A plugin that sniffs Bluetooth devices and saves their MAC addresses, name and counts to a JSON file'

    def __init__(self):
        # Defining the instance variables
        self.options = {
            'timer': 15,
            'devices_file': '/root/handshakes/bluetooth_devices.json',
            'count_interval': 86400
        }
        self.devices = {}
        self.last_scan_time = 0

    def on_loaded(self):
        logging.info("bluetoothsniffer plugin loaded.")
        logging.info("Bluetoot devices file location: %s", self.options['devices_file'])
        # Creating the device file path if it does not exist
        if not os.path.exists(os.path.dirname(self.options['devices_file'])):
            os.makedirs(os.path.dirname(self.options['devices_file']))

        # Creating the device file if it does not exist
        if not os.path.exists(self.options['devices_file']):
            with open(self.options['devices_file'], 'w') as f:
                json.dump({}, f)

        # Loading the data from the device file
        with open(self.options['devices_file'], 'r') as f:
            self.devices = json.load(f)


    def on_ui_update(self, agent):
        current_time = time.time()
        # Checking the time elapsed since last scan
        if current_time - self.last_scan_time >= self.options['timer']:
            self.last_scan_time = current_time
            self.scan()

    # Method for scanning the nearby bluetooth devices
    def scan(self):
        logging.info("Scanning for bluetooths...")
        current_time = time.time()
        # Running the system command hcitool to scan nearby bluetooth devices
        cmd_inq = "sudo hcitool inq --flush"
        inq_output = subprocess.check_output(cmd_inq.split())
        changed = False
        for line in inq_output.splitlines()[1:]:
            fields = line.split()
            mac_address = fields[0].decode()
            for i in range(len(fields)):
                if fields[i].decode() == "class:" and i+1 < len(fields):
                    device_class = fields[i+1].decode()
            logging.info("Found bluetooth %s", mac_address)
            name = self.get_device_name(mac_address)
            manufacturer = self.get_device_manufacturer(mac_address)

            # Update the count, first_seen, and last_seen time of the device
            if mac_address in self.devices:
                if name != 'Unknown' and name != self.devices[mac_address]['name']:
                    self.devices[mac_address]['name'] = name
                    self.devices[mac_address]['new_info'] = True
                    logging.info("Updated bluetooth name: %s", name)
                    changed = True

                if manufacturer != 'Unknown' and manufacturer != self.devices[mac_address]['manufacturer']:
                    self.devices[mac_address]['manufacturer'] = manufacturer
                    self.devices[mac_address]['new_info'] = True
                    logging.info("Updated bluetooth manufacturer: %s", manufacturer)
                    changed = True

                if device_class != self.devices[mac_address]['class']:
                    self.devices[mac_address]['class'] = device_class
                    self.devices[mac_address]['new_info'] = True
                    logging.info("Updated bluetooth class: %s", device_class)
                    changed = True

                if current_time - self.last_seen_time >= self.options['count_interval']:
                    self.devices[mac_address]['count'] += 1
                    self.last_seen_time = current_time
                    self.devices[mac_address]['last_seen'] = time.strftime('%H:%M:%S %d-%m-%Y', time.localtime(current_time))
                    self.devices[mac_address]['new_info'] = True
                    logging.info("Updated bluetooth count.")
                    changed = True
            else:
                self.devices[mac_address] = {'name': name, 'count': 1, 'class': device_class, 'manufacturer': manufacturer, 'first_seen': time.strftime('%H:%M:%S %d-%m-%Y', time.localtime(current_time)), 'last_seen': time.strftime('%H:%M:%S %d-%m-%Y', time.localtime(current_time)), 'new_info': True}
                self.last_seen_time = current_time
                logging.info("Added new bluetooth device %s with MAC: %s", name, mac_address)
                changed = True

        # Save the updated devices to the JSON file
        if changed:
            with open(self.options['devices_file'], 'w') as f:
                logging.info("Saving bluetooths %s in to json.", name)
                json.dump(self.devices, f)

    # Method to get the device name
    def get_device_name(self, mac_address):
        logging.info("Trying to get name for %s", mac_address)
        name = 'Unknown'
        hcitool_process = subprocess.Popen(["hcitool", "name", mac_address], stdout=subprocess.PIPE)
        output, error = hcitool_process.communicate()
        if output.decode().strip() != '':
            name = output.decode().strip()
        logging.info("Got name %s for %s", name, mac_address)
        return name

    def get_device_manufacturer(self, mac_address):
        manufacturer = 'Unknown'
        cmd_info = f"sudo hcitool info {mac_address} | grep 'Manufacturer:' | cut -d ' ' -f 2-"
        try:
            logging.info("Trying to get manufacturer for %s", mac_address)
            start_time = time.time()
            process = subprocess.Popen(cmd_info, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            while process.poll() is None:
                time.sleep(0.1)
                if time.time() - start_time > 7:
                    logging.info("Timeout while trying to get manufacturer for %s", mac_address)
                    process.kill()
                    return manufacturer
            output, error = process.communicate(timeout=1)
            if output.decode().strip() != '':
                manufacturer = output.decode().strip()
            logging.info("Got manufacturer %s for %s", manufacturer, mac_address)
        except Exception as e:
            logging.info("Error while trying to get manufacturer for %s: %s", mac_address, str(e))
        return manufacturer