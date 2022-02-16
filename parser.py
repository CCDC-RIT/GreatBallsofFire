# /usr/bin/env python3

"""
    Parser.py is a tool to parse network topologies and create a list of firewall rules for the router
    Authors:
        Jason Howe
        Zach Price
    
"""

import json

from builder import main

# Lists of Rules to build
zonerules = []
hostrules = []
remotingrules = []

# Lists of Bad Rules to not build
badzonerules = []
badhostrules = []
badremotingrules = []

Zone = ["WAN", "LAN", "DMZ", "cloud", "wan", "lan"]
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

def buildremotingrules(source, host, remotingname, remotingport, dest, action):
    # build remoting rule will take in a source zone, a host ip, and a remoting protocol, a destination zone, and an action and add the rule to the host rules list
    if source not in Zone:
        # log Invalid source error
        error  = "Invalid Source: " + source + " to " + dest + ": " + action
        badremotingrules.append(error)
    elif dest not in Zone:
        # log Invalid Destination error
        error  = "Invalid Destination: " + source + " to " + dest + ": " + action
        badremotingrules.append(error)
    elif action not in Action:
        # log Invalid Action error
        error  = "Invalid Action: " + source + " to " + dest + ": " + action
        badremotingrules.append(error)
    elif source == dest: 
        # log Source and Destination Equal error
        error  = "Source and Destination Equal: " + source + " to " + dest + ": " + action
        badremotingrules.append(error)
    else:
        # If the rule passes through all the checks 
        # Creates the rules with the parameters
        remotingrule = source + " (Host: " + host + " | Remoting Protocol: " +  remotingname + " ["
        remotingrule += remotingport + "]) to " + dest + ": " + action
        # Adds the hostrule to the hostrules list
        remotingrules.append(remotingrule)


#import/open the json file and read
#parse through the json file 

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

## Networks: Dict. Items: List Network Defintions
## Network Defintitions List. Items: Ip, Name, Hosts
## Hosts: list. Items: host IP, name, os, remoting protocol, service
## Remoting Protocol: list. Items: Name, list of ports
## Service: list. Items: Name, list of ports

def print_json():
    with open("newtopology.json", "r") as read_file:
        data = json.load(read_file)
        
        
        for netid in data['networks']:
            print("ip:", netid["ip"])
            print("name:", netid["name"])
            for host in netid['hosts']: 
                print("hosts:", host)
    # print(data)
print_json()


# parse_host will parse the host def and call buildhostrule/buildremotingrule
def parse_host(netname, firstquads, host):
    ip = firstquads + host["ip"]
    # build services
    for service in host["service"]:
        for port in service["ports"]:
            buildhostrules(netname, ip, service, port, "WAN", "ALLOW")
    # build remoting
    for remoting in host["remoting protocol"]:
        for port in remoting["ports"]:
            buildhostrules(netname, ip, remoting, port, "DMZ", "ALLOW")

# parse_networks will iterate through the list of network definitions, 
# identify the parameters, and call parse_host for each host in the network
def parse_networks(netdict):
    name = netdict["name"]
    threequads = netdict["ip"]
    hosts = netdict["hosts"]
    for host in hosts:
        parse_host(name, threequads, host)



def main():
    # open files
    # set up parameters - call parse_networks
    parse_networks()
    # print to the list

