# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 12:08:44 2024

@author: najma
"""
from netmiko import ConnectHandler
import logging

# Setup logging
logging.basicConfig(filename='network_config.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Define multiple routers
routers = [
    {
        'device_type': 'cisco_ios',
        'ip': '192.168.56.101',
        'username': 'cisco',
        'password': 'cisco123!',
        'interface_commands': [
            'interface loopback0',
            'ip address 192.168.1.1 255.255.255.0',
            'no shutdown',
            'description Loopback Interface Configured by Script',
            'interface gigabitEthernet0/1',
            'ip address 192.168.2.1 255.255.255.0',
            'no shutdown',
            'description Main Interface Configured by Script'
        ],
        'ospf_commands': [
            'router ospf 1',
            'network 192.168.1.0 0.0.0.255 area 0',
            'network 192.168.2.0 0.0.0.255 area 0',
            'exit'
        ]
    },
    {
        'device_type': 'cisco_ios',
        'ip': '192.168.56.102',
        'username': 'cisco',
        'password': 'cisco123!',
        'interface_commands': [
            'interface loopback1',
            'ip address 192.168.3.1 255.255.255.0',
            'no shutdown',
            'description Loopback Interface 1 Configured by Script',
            'interface gigabitEthernet0/2',
            'ip address 192.168.4.1 255.255.255.0',
            'no shutdown',
            'description Main Interface 2 Configured by Script'
        ],
        'ospf_commands': [
            'router ospf 1',
            'network 192.168.3.0 0.0.0.255 area 0',
            'network 192.168.4.0 0.0.0.255 area 0',
            'exit'
        ]
    }
]

# Function to configure a single router
def configure_router(router):
    try:
        print(f"Connecting to router at {router['ip']}...")
        connection = ConnectHandler(**router)
        logging.info(f"Connection established with router at {router['ip']}.")
        print("Connected successfully!")

        # Configure interfaces
        print(f"Configuring interfaces for router at {router['ip']}...")
        interface_output = connection.send_config_set(router['interface_commands'])
        print("Interface configuration applied successfully!")
        logging.info(f"Interface configuration commands sent to {router['ip']}:\n{interface_output}")

        # Verify interface configuration
        print(f"Verifying interface configuration for router at {router['ip']}...")
        interface_verification = connection.send_command("show ip interface brief")
        print(f"Current Interface Configuration for {router['ip']}:\n{interface_verification}")
        logging.info(f"Interface Verification Output for {router['ip']}:\n{interface_verification}")

        # Configure OSPF
        print(f"Configuring OSPF for router at {router['ip']}...")
        ospf_output = connection.send_config_set(router['ospf_commands'])
        print("OSPF configuration applied successfully!")
        logging.info(f"OSPF configuration commands sent to {router['ip']}:\n{ospf_output}")

        # Verify OSPF configuration
        print(f"Verifying OSPF configuration for router at {router['ip']}...")
        ospf_verification = connection.send_command("show ip protocols")
        print(f"OSPF Protocol Details for {router['ip']}:\n{ospf_verification}")
        logging.info(f"OSPF Protocol Verification Output for {router['ip']}:\n{ospf_verification}")

        # Disconnect
        connection.disconnect()
        logging.info(f"Disconnected from router at {router['ip']}.")
        print(f"Disconnected successfully from router at {router['ip']}.")
    except Exception as e:
        logging.error(f"An error occurred with router at {router['ip']}: {e}")
        print(f"An error occurred with router at {router['ip']}: {e}")

# Main script
if __name__ == "__main__":
    for router in routers:
        configure_router(router)

if __name__ == "__main__":
    for router in routers:
        configure_router(router)

