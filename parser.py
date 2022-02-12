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
        zonerule = source + " to " + dest + ": " + action
        zonerules.append(zonerule)

def buildhostrules(source, host, servicename, serviceports, dest, action):
    # build host rule will take in a source zone, a host ip, and a service a destination zone, and an action and add the rule to the host rules list
    if source not in Zone:
        # log Invalid source error
        error  = "Invalid Source:\t" + source + " to " + dest + ": " + action
        badzonerules.append(error)
    elif dest not in Zone:
        # log Invalid Destination error
        error  = "Invalid Destination:\t" + source + " to " + dest + ": " + action
        badzonerules.append(error)
    elif action not in Action:
        # log Invalid Action error
        error  = "Invalid Action:\t" + source + " to " + dest + ": " + action
        badzonerules.append(error)
    elif source == dest: 
        # log Source and Destination Equal error
        error  = "Source and Destination Equal:\t" + source + " to " + dest + ": " + action
        badzonerules.append(error)
    else:
        zonerule = source + host + servicename + " ["
        for ports in serviceports:
            zonerule +=  ports + ", "
        zonerule += "] to " + dest + ": " + action
        zonerules.append(zonerule)

def test():
    testzone = input("Test host rules: ")
    test1 = testzone.split(",")
    buildzonerule(test1[0], test1[1], test1[2])

    badtestzone = input("Bad Test host rules: ")
    test1 = badtestzone.split(",")
    buildzonerule(test1[0], test1[1], test1[2])

    # testhost = input("Test host rules: ")
    # test1 = testhost.split(",")
    # buildhostrules(test1[0], test1[1], test1[2], test1[3], test1[4], test1[5])
    
    # badtesthost = input("Bad Test host rules: ")
    # test1 = badtesthost.split(",")
    # buildhostrules(test1[0], test1[1], test1[2], test1[3], test1[4], test1[5])

    
    print("Zone rules:")
    print(zonerules)
    print("Bad Zone rules: ")
    print(badzonerules)
    print("Host rules: ")
    print(hostrules)
    print("Bad Host rules: ") 
    print(badhostrules)

test()