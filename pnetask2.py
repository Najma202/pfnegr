# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 10:43:41 2024

@author: najma
"""
from netmiko import ConnectHandler
import difflib

device = {
    "device_type": "cisco_ios",  
    "host": "192.168.56.101",       
    "username": "cisco",         
    "password": "cisco123!",      
    "secret": "class123!"  
}

try:
    print("Connecting to the device...")
    connection = ConnectHandler(**device)
    connection.enable()  
    
    print("Retrieving configurations...")
    running_config = connection.send_command("show running-config")
    startup_config = connection.send_command("show startup-config")
    
    print("Comparing configurations...")
    diff = difflib.unified_diff(
        startup_config.splitlines(), 
        running_config.splitlines(), 
        fromfile="Startup Config", 
        tofile="Running Config", 
        lineterm=""
    )
    
    diff_output = '\n'.join(diff)
    if diff_output:
        print("Differences found between startup-config and running-config:")
        print(diff_output)
    else:
        print("No differences found between startup-config and running-config.")
        
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    if 'connection' in locals() and connection.is_alive():
        connection.disconnect()


