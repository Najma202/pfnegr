# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 12:08:44 2024

@author: najma
"""
from netmiko import ConnectHandler
import logging

# Logging setup
logging.basicConfig(filename='network_config.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Define multiple routers
routers = [
    {
        'device_type': 'cisco_ios',
        'ip': '192.168.56.101',
        'username': 'cisco',
        'password': 'cisco123!',
        'interfaces': [
            ('loopback0', '192.168.1.1 255.255.255.0', 'Primary Loopback'),
            ('gigabitEthernet0/1', '192.168.3.1 255.255.255.0', 'Primary Interface')
        ],
        'ospf_networks': ['192.168.1.0 0.0.0.255', '192.168.3.0 0.0.0.255']
    },
    {
        'device_type': 'cisco_ios',
        'ip': '192.168.56.102',
        'username': 'cisco',
        'password': 'cisco123!',
        'interfaces': [
            ('loopback0', '192.168.4.1 255.255.255.0', 'Secondary Loopback'),
            ('gigabitEthernet0/2', '192.168.5.1 255.255.255.0', 'Secondary Interface')
        ],
        'ospf_networks': ['192.168.4.0 0.0.0.255', '192.168.5.0 0.0.0.255']
    }
]

# Function to configure a router
def configure_router(router):
    try:
        print(f"Connecting to router {router['ip']}...")
        connection = ConnectHandler(**router)
        logging.info(f"Connection established with router {router['ip']}.")

        # Configure interfaces
        print(f"Configuring interfaces for router {router['ip']}...")
        for interface, ip, description in router['interfaces']:
            commands = [
                f"interface {interface}",
                f"ip address {ip}",
                "no shutdown",
                f"description {description}"
            ]
            interface_output = connection.send_config_set(commands)
            logging.info(f"Interface configuration output for {router['ip']}:\n{interface_output}")

        # Configure OSPF
        print(f"Configuring OSPF for router {router['ip']}...")
        ospf_commands = ['router ospf 1'] + [
            f"network {network} area 0" for network in router['ospf_networks']
        ]
        ospf_output = connection.send_config_set(ospf_commands)
        logging.info(f"OSPF configuration output for {router['ip']}:\n{ospf_output}")

        # Verify OSPF
        print(f"Verifying OSPF configuration for router {router['ip']}...")
        ospf_verification = connection.send_command("show ip protocols")
        print(f"OSPF Verification Output for {router['ip']}:\n{ospf_verification}")
        logging.info(f"OSPF Verification Output for {router['ip']}:\n{ospf_verification}")

        connection.disconnect()
        logging.info(f"Disconnected from router {router['ip']}.")
        print(f"Disconnected from router {router['ip']} successfully.")

    except Exception as e:
        logging.error(f"An error occurred with router {router['ip']}: {e}")
        print(f"An error occurred with router {router['ip']}: {e}")

# Main script to configure all routers
if __name__ == "__main__":
    for router in routers:
        configure_router(router)

