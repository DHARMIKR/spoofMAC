#!/usr/bin/env python

import subprocess
import optparse
import re

def get_arguments():
    parser = optparse.OptionParser()

    parser.add_option("-i", "--interface", dest="interface", help="Interface to changer its MAC Address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC Address")
    (values, arguments) = parser.parse_args()
    return values.interface,values.new_mac


def change_mac(interface,new_mac):
    print("[+] Changing MAC Address for " + interface + " to " + new_mac)

    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])

def display_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])

    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)

    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[-] we could not find mac address")

def main(interface,new_mac):
    current_mac = display_current_mac(interface)
    print("current mac = " + current_mac)

    change_mac(interface, new_mac)

    current_mac = display_current_mac(interface)

    if current_mac == new_mac:
        print("[+] Your MAC Address has been change successfully to " + new_mac)
    else:
        print("[-] Your MAC Address did not change")


print(''' ____  _                          _ _ 
|  _ \| |__   __ _ _ __ _ __ ___ (_) | __ 
| | | | '_ \ / _` | '__| '_ ` _ \| | |/ / 
| |_| | | | | (_| | |  | | | | | | |   < 
|____/|_| |_|\__,_|_|  |_| |_| |_|_|_|\_\ 
''')

(interface, new_mac) = get_arguments()

if interface and new_mac is not None:
    main(interface,new_mac)

else:
    interface = raw_input("interface >")
    new_mac = raw_input("new mac >")
    main(interface,new_mac)