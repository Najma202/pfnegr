# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 09:50:09 2024

@author: najma
"""

from netmiko import ConnectHandler
import difflib

device = {
    "device_type": "cisco_ios",  
    "host": "192.168.56.101",       
    "username": "cisco",        
    "password": "cisco123!",      
    "secret": "class123!", 
}
 
try:
    print("Connecting to the device...")
    connection = ConnectHandler(**device)
    connection.enable()
 
    print("Retrieving running and startup configurations...")
    running_config = connection.send_command("show running-config")
    startup_config = connection.send_command("show startup-config")
 
    running_config_lines = running_config.splitlines()
    startup_config_lines = startup_config.splitlines()
 
    print("Comparing configurations...")
    diff = difflib.unified_diff(
    (startup_config_lines()),
    running_config_lines(), 
    fromfile="Startup Config", 
    tofile="Running Config", 
    lineterm=''
    )
    diff_output = '\n'.join(diff)
 
    if diff_output:
        print("Differences between startup-config and running-config:")
        print(diff_output)
    else:
        print("No differences between startup-config and running-config.")
 
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    connection.disconnect()