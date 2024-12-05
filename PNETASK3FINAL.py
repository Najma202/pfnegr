# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 15:05:09 2024

@author: najma
"""

from netmiko import ConnectHandler
import logging

logging.basicConfig(filename='network_config.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

router = {
    'device_type': 'cisco_ios',
    'ip': '192.168.56.103',  
    'username': 'cisco',     
    'password': 'cisco123!'  
}

interface_commands = [
    'interface loopback0',
    'ip address 192.168.1.1 255.255.255.0',
    'no shutdown',
    'description Loopback Interface Configured by Script',
    'interface gigabitEthernet0/1',
    'ip address 192.168.2.1 255.255.255.0',
    'no shutdown',
    'description Main Interface Configured by Script'
]

ospf_commands = [
    'router ospf 1',
    'network 192.168.1.0 0.0.0.255 area 0', 
    'network 192.168.2.0 0.0.0.255 area 0',
    'exit'
]

try:
    print("Connecting to the router...")
    connection = ConnectHandler(**router)
    logging.info("Connection established with the router.")
    print("Connected successfully!")

    print("Configuring interfaces...")
    interface_output = connection.send_config_set(interface_commands)
    print("Interface configuration applied successfully!")
    logging.info(f"Interface configuration commands sent:\n{interface_output}")

    print("Verifying interface configuration...")
    interface_verification = connection.send_command("show ip interface brief")
    print("Current Interface Configuration:")
    print(interface_verification)
    logging.info(f"Interface Verification Output:\n{interface_verification}")

    print("Configuring OSPF...")
    ospf_output = connection.send_config_set(ospf_commands)
    print("OSPF configuration applied successfully!")
    logging.info(f"OSPF configuration commands sent:\n{ospf_output}")

    print("Verifying OSPF configuration...")
    ospf_verification = connection.send_command("show ip protocols")
    print("OSPF Protocol Details:")
    print(ospf_verification)
    logging.info(f"OSPF Protocol Verification Output:\n{ospf_verification}")

    connection.disconnect()
    logging.info("Disconnected from the router.")
    print("Disconnected successfully.")
except Exception as e:
    logging.error(f"An error occurred: {e}")
    print(f"An error occurred: {e}")
