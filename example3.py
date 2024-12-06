# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 12:08:44 2024

@author: najma
"""
from netmiko import ConnectHandler
import logging

logging.basicConfig(filename='network_config.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

routers = [
    {
        'device_type': 'cisco_ios',
        'ip': '192.168.56.101',
        'username': 'cisco',
        'password': 'cisco123!'
    },
]

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

def configure_router(router):
    try:
        print(f"Connecting to router {router['ip']}...")
        connection = ConnectHandler(**router)
        logging.info(f"Connection established {router['ip']}.")
        print(f"Connected to router {router['ip']} successfully!")

        print("Configuring interfaces...")
        interface_output = connection.send_config_set(interface_commands)
        print("Interface configured successfully!")
        logging.info(f"Interface configuration commands sent for {router['ip']}:\n{interface_output}")

        print("Verifying interface configuration...")
        interface_verification = connection.send_command("show ip interface brief")
        print(f"Current Interface Configuration for {router['ip']}:\n{interface_verification}")
        logging.info(f"Interface Verification Output for {router['ip']}:\n{interface_verification}")

        print("Configuring OSPF...")
        ospf_output = connection.send_config_set(ospf_commands)
        print("OSPF configuration applied successfully!")
        logging.info(f"OSPF configuration commands sent for {router['ip']}:\n{ospf_output}")

        print("Verifying OSPF configuration...")
        ospf_verification = connection.send_command("show ip protocols")
        print(f"OSPF Protocol Details for {router['ip']}:\n{ospf_verification}")
        logging.info(f"OSPF Protocol Verification Output for {router['ip']}:\n{ospf_verification}")

        connection.disconnect()
        logging.info(f"Disconnected from router {router['ip']}.")
        print(f"Disconnected from router {router['ip']} successfully.")

    except Exception as e:
        logging.error(f"An error occurred with router {router['ip']}: {e}")
        print(f"An error occurred with router {router['ip']}: {e}")

if __name__ == "__main__":
    for router in routers:
        configure_router(router)
