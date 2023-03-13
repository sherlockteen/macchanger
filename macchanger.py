#!/usr/bin/env python
import subprocess
import optparse
import re


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface, for more info use --help")
    if not options.new_mac:
        parser.error("[-] Please specify a MAC address, for more info use --help")
    return options


def change_mac(interface, new_mac):
    print(f"[+] Changing MAC address for {interface} to {new_mac}")
    subprocess.call(["sudo", "ifconfig", interface, "down"])
    subprocess.call(["sudo", "ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["sudo", "ifconfig", interface, "up"])


def get_current_mac(interface):
    try:
        ifconfig_result = subprocess.check_output(["ifconfig", interface])
        mac_address_search_result = re.search(r"([0-9a-f]{2}:){5}[0-9a-f]{2}", ifconfig_result.decode("utf-8"))
        if mac_address_search_result is None:
            print("[-] Could not read mac address")
            exit()
        return mac_address_search_result.group(0)
    except (AttributeError, subprocess.CalledProcessError):
        print("[-] Could not read mac address")


options = get_arguments()

current_mac = get_current_mac(options.interface)
print(f"your current MAC = {current_mac}")
change_mac(options.interface, options.new_mac)

current_mac = get_current_mac(options.interface)

if current_mac == options.new_mac:
    print(f"[+] MAC address was successfully changed to {current_mac}")
else:
    print(f"[-] MAC address did not get changed.")
