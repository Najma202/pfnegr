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

# New function to verify OSPF routing table
def verify_ospf_routing_table(connection):
    try:
        print("Verifying OSPF routing table...")
        output = connection.send_command("show ip ospf route")
        print(f"OSPF routing table:\n{output}")
        logging.info(f"OSPF routing table:\n{output}")
    except Exception as e:
        logging.error(f"Error verifying OSPF routing table: {e}")
        print(f"Error verifying OSPF routing table: {e}")

# New function to save configuration to startup
def save_configuration(connection):
    try:
        print("Saving configuration to startup...")
        output = connection.send_command("write memory")
        print(f"Configuration saved: {output}")
        logging.info(f"Configuration saved: {output}")
    except Exception as e:
        logging.error(f"Error saving configuration: {e}")
        print(f"Error saving configuration: {e}")

# New function to check interface status
def check_interface_status(connection, interface):
    try:
        print(f"Checking status of {interface}...")
        output = connection.send_command(f"show interface {interface} status")
        print(f"Interface {interface} status:\n{output}")
        logging.info(f"Interface {interface} status:\n{output}")
        return output
    except Exception as e:
        logging.error(f"Error checking interface {interface} status: {e}")
        print(f"Error checking interface {interface} status: {e}")
        return None

def configure_router(router):
    try:
        print(f"Connecting to {router['ip']}...")
        connection = ConnectHandler(**router)
        logging.info(f"Connected to {router['ip']}.")
        print(f"Connected to {router['ip']}!")

        # Check and configure interfaces
        for interface in ['Loopback0', 'Loopback1', 'GigabitEthernet0/1']:
            interface_status = check_interface_status(connection, interface)
            if interface_status and "notconnect" not in interface_status.lower():
                print(f"{interface} is already configured or in use. Skipping configuration.")
                logging.info(f"{interface} is already configured or in use. Skipping configuration.")
            else:
                print(f"Configuring {interface}...")
                interface_output = connection.send_config_set(interface_commands)
                print(f"{interface} configured!")
                logging.info(f"{interface} configuration:\n{interface_output}")

        # Configuring OSPF
        print("Configuring OSPF...")
        ospf_output = connection.send_config_set(ospf_commands)
        print("OSPF configured!")
        logging.info(f"OSPF commands for {router['ip']}:\n{ospf_output}")

        # Verify OSPF routing table
        verify_ospf_routing_table(connection)

        # Save the configuration
        save_configuration(connection)

        connection.disconnect()
        logging.info(f"Disconnected from {router['ip']}.")
        print(f"Disconnected from {router['ip']}.")

    except Exception as e:
        logging.error(f"Error with {router['ip']}: {e}")
        print(f"Error with {router['ip']}: {e}")

if __name__ == "__main__":
    for router in routers:
        configure_router(router)

        configure_router(router)

