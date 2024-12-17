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

# New function to backup the running configuration of the router
def backup_configuration(connection, router_ip):
    try:
        print(f"Backing up running configuration for {router_ip}...")
        output = connection.send_command("show running-config")
        backup_filename = f"backup_{router_ip}.txt"
        
        # Write the output of the running configuration to a backup file
        with open(backup_filename, 'w') as backup_file:
            backup_file.write(output)
        
        print(f"Running configuration backed up to {backup_filename}.")
        logging.info(f"Running configuration for {router_ip} backed up to {backup_filename}.")
    except Exception as e:
        logging.error(f"Error backing up configuration for {router_ip}: {e}")
        print(f"Error backing up configuration for {router_ip}: {e}")

def configure_router(router):
    try:
        print(f"Connecting to {router['ip']}...")
        connection = ConnectHandler(**router)
        logging.info(f"Connected to {router['ip']}.")
        print(f"Connected to {router['ip']}!")

        # Backup the current running configuration before making any changes
        backup_configuration(connection, router['ip'])

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

