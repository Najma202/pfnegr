# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 11:44:51 2024

@author: najma
"""

from netmiko import ConnectHandler
import tkinter as tk
from tkinter import messagebox
import logging

logging.basicConfig(filename='network_config.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

router = {
    'device_type': 'cisco_ios',
    'ip': '192.168.56.101',
    'username': 'cisco',
    'password': 'cisco123!',
}

interface_commands = [
    'interface loopback0',
    'ip address 192.168.1.1 255.255.255.0',
    'no shutdown',
    'description Loopback Interface',
    'interface loopback1',
    'ip address 192.168.2.1 255.255.255.0',
    'no shutdown',
    'description Second Loopback Interface',
    'interface gigabitEthernet0/1',
    'ip address 192.168.3.1 255.255.255.0',
    'no shutdown',
    'description Main GigabitEthernet Interface',
]

ospf_commands = [
    'router ospf 1',
    'network 192.168.1.0 0.0.0.255 area 0',
    'network 192.168.2.0 0.0.0.255 area 0',
    'network 192.168.3.0 0.0.0.255 area 0',
]

ping_targets = ['192.168.1.1', '192.168.2.1', '192.168.3.1']

def configure_interfaces():
    try:
        connection = ConnectHandler(**router)
        connection.send_config_set(interface_commands)
        connection.disconnect()
        messagebox.showinfo("Success", "Interfaces configured successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to configure interfaces: {e}")

def configure_ospf():
    try:
        connection = ConnectHandler(**router)
        connection.send_config_set(ospf_commands)
        connection.disconnect()
        messagebox.showinfo("Success", "OSPF configured successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to configure OSPF: {e}")

def test_ping():
    try:
        connection = ConnectHandler(**router)
        results = []
        for ip in ping_targets:
            result = connection.send_command(f"ping {ip}")
            results.append(f"Ping {ip}: {result}")
        connection.disconnect()
        result_text = "\n".join(results)
        messagebox.showinfo("Ping Results", result_text)
    except Exception as e:
        messagebox.showerror("Error", f"Ping test failed: {e}")

root = tk.Tk()
root.title("Network Configuration Tool")

tk.Label(root, text="Simple Network Configuration").pack(pady=10)

tk.Button(root, text="Configure Interfaces", command=configure_interfaces, width=25).pack(pady=5)
tk.Button(root, text="Configure OSPF", command=configure_ospf, width=25).pack(pady=5)
tk.Button(root, text="Test Ping", command=test_ping, width=25).pack(pady=5)

root.mainloop()
