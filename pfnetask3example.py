
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
    'description Loopback Interface',
    'interface Loopback1',
    'ip address 192.168.2.1 255.255.255.0',
    'no shutdown',
    'description Second Loopback Interface',
    'interface gigabitEthernet0/1',
    'ip address 192.168.2.1 255.255.255.0',
    'no shutdown',
    'description Main Interface'
]

ospf_commands = [
    'router ospf 1',
    'network 192.168.1.0 0.0.0.255 area 0', 
    'network 192.168.2.0 0.0.0.255 area 0',
    'exit'
]

def backup_config(connection, router_ip):
    """ Backs up the router's running configuration """
    print("Backing up running configuration...")
    try:
        output = connection.send_command("show running-config")
        with open(f"backup_{router_ip}.txt", "w") as backup_file:
            backup_file.write(output)
        logging.info(f"Backup saved for {router_ip}")
        print(f"Running configuration backed up to backup_{router_ip}.txt")
    except Exception as e:
        logging.error(f"Failed to back up config for {router_ip}: {e}")
        print(f"Error backing up configuration: {e}")

def verify_ospf_neighbors(connection, router_ip):
    """ Verifies OSPF neighbor relationships """
    print("Verifying OSPF neighbors...")
    try:
        output = connection.send_command("show ip ospf neighbor")
        print(f"OSPF Neighbors for {router_ip}:\n{output}")
        logging.info(f"OSPF neighbors verification for {router_ip}:\n{output}")
    except Exception as e:
        logging.error(f"Failed to verify OSPF neighbors on {router_ip}: {e}")
        print(f"Error verifying OSPF neighbors: {e}")

def configure_router(router):
    try:
        print(f"Connecting to {router['ip']}...")
        connection = ConnectHandler(**router)
        logging.info(f"Connected to {router['ip']}.")
        print(f"Connected to {router['ip']}!")

        print("Configuring interfaces...")
        interface_output = connection.send_config_set(interface_commands)
        print("Interfaces configured!")
        logging.info(f"Interface commands for {router['ip']}:\n{interface_output}")

        print("Verifying interfaces...")
        interface_verification = connection.send_command("show ip interface brief")
        print(f"Interfaces on {router['ip']}:\n{interface_verification}")
        logging.info(f"Interface verification for {router['ip']}:\n{interface_verification}")

        print("Configuring OSPF...")
        ospf_output = connection.send_config_set(ospf_commands)
        print("OSPF configured!")
        logging.info(f"OSPF commands for {router['ip']}:\n{ospf_output}")

        print("Verifying OSPF...")
        ospf_verification = connection.send_command("show ip protocols")
        print(f"OSPF on {router['ip']}:\n{ospf_verification}")
        logging.info(f"OSPF verification for {router['ip']}:\n{ospf_verification}")

        connection.disconnect()
        logging.info(f"Disconnected from {router['ip']}.")
        print(f"Disconnected from {router['ip']}.")

    except Exception as e:
        logging.error(f"Error with {router['ip']}: {e}")
        print(f"Error with {router['ip']}: {e}")

if __name__ == "__main__":
    for router in routers:
        configure_router(router)
