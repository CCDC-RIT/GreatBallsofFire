# /usr/bin/env python3

"""
    Parser.py is a tool to parse network topologies and create a list of firewall rules for the router
    Authors:
        Jason Howe
        Zach Price
    
"""

from enum import Enum

# Lists of Rules to build
zonerules = []
hostrules = []
remotingrules = []

# Lists of Bad Rules to not build
badzonerules = []
badhostrules = []
badremotingrules = []

Zone = ["WAN", "LAN", "DMZ"]
Action = ["ALLOW", "DENY"]

def buildzonerule(source, dest, action):
    # build zone rule will take in a source zone, a destination zone, and an action and add the rule to the zone rules list
    # 
    # badzonerules.append(badzonerule)
    if source not in Zone:
        # log Invalid source error
        error  = "Invalid Source: " + source + " to " + dest + ": " + action
        badzonerules.append(error)
    elif dest not in Zone:
        # log Invalid Destination error
        error  = "Invalid Destination: " + source + " to " + dest + ": " + action
        badzonerules.append(error)
    elif action not in Action:
        # log Invalid Action error
        error  = "Invalid Action: " + source + " to " + dest + ": " + action
        badzonerules.append(error)
    elif source == dest: 
        # log Source and Destination Equal error
        error  = "Source and Destination Equal: " + source + " to " + dest + ": " + action
        badzonerules.append(error)
    else:
        # If the rule passes through all the checks
        # It is created
        zonerule = source + " to " + dest + ": " + action
        # and added into the zonerules list to be stored
        zonerules.append(zonerule)

def buildhostrules(source, host, servicename, serviceports, dest, action):
    # build host rule will take in a source zone, a host ip, and a service a destination zone, and an action and add the rule to the host rules list
    if source not in Zone:
        # log Invalid source error
        error  = "Invalid Source: " + source + " to " + dest + ": " + action
        badhostrules.append(error)
    elif dest not in Zone:
        # log Invalid Destination error
        error  = "Invalid Destination: " + source + " to " + dest + ": " + action
        badhostrules.append(error)
    elif action not in Action:
        # log Invalid Action error
        error  = "Invalid Action: " + source + " to " + dest + ": " + action
        badhostrules.append(error)
    elif source == dest: 
        # log Source and Destination Equal error
        error  = "Source and Destination Equal: " + source + " to " + dest + ": " + action
        badhostrules.append(error)
    else:
        # If the rule passes through all the checks 
        #It starts by creating the string wiht the basic information
        hostrule = source + " (Host: " + host + " | Service: " +  servicename + " ["
        # Splits the service ports
        ports = serviceports.split(",")
        # Interates through the split strings
        # Done this way to make them appear better after created 
        for i in range(len(ports)):
            # Checks if the port is the last in the list (purely for visual)
            if i == len(ports) - 1:
                # Adds it to the rule
                hostrule +=  ports[i]
            else:
                # Otherwise adds the port to the rule and moves on to the next port  
                hostrule +=  ports[i] + ", "
        # Finishes creting the hostrule string
        hostrule += "]) to " + dest + ": " + action
        # Adds the hostrule to the hostrules list
        hostrules.append(hostrule)

def test():
    # Basic Test function that does error checking and prints the lists
    buildzonerule("WAN", "LAN", "ALLOW")
    buildzonerule("TEST", "WAN", "ALLOW")
    buildzonerule("WAN", "TEST", "ALLOW")
    buildzonerule("WAN", "LAN", "PROCEED")
    buildzonerule("WAN", "WAN", "ALLOW")

    buildhostrules("WAN", "10.150.17.3", "https", "80, 443", "LAN", "ALLOW")
    buildhostrules("TEST", "10.150.17.3", "https", "80, 443", "LAN", "ALLOW")
    buildhostrules("WAN", "10.150.17.3", "https", "80, 443", "TEST", "ALLOW")
    buildhostrules("WAN", "10.150.17.3", "https", "80, 443", "LAN", "PROCEED")
    buildhostrules("WAN", "10.150.17.3", "https", "80,443", "WAN", "ALLOW")

    
    print("Zone rules:")
    print(zonerules)
    print("Bad Zone rules: ")
    print(badzonerules)
    print("Host rules: ")
    print(hostrules)
    print("Bad Host rules: ") 
    print(badhostrules)

test()