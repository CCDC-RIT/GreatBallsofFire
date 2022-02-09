# /usr/bin/env python3

"""
    builder.py is a tool to build network topologies
    Authors:
        Jason Howe
        Zach Price
"""
import json
import sys

try:
    from termcolor import colored as c
except:
    def c(text, *ars, **kwargs):
        return text

COLOR = 'blue'


def prompt(text="", color=COLOR):
    '''
    Generate a prompt with the given color and return the output
    '''
    return input(c(text, color, attrs=('bold',)))


def addRemoting():
    # add a remoting protocol
    pass


def addService():
    pass


def addHost(network):
    '''
    Get the input information for a host on the network
    '''
    data = {}
    while True:
        ip = input(c('IP: ', COLOR, attrs=('bold',))+network+".")
        hostname = prompt("Hostname: ")
        os = prompt("OS: ")
        data['remoting'] = []
        while True:
            newRemoting = prompt("Add a remoting to this host? [Y/n]", "green")
            if newRemoting not in ("", "y", "yes"):
                break
            data['remoting'] += [addRemoting()]
        while True:
            newService = prompt("Add a service to this host? [Y/n]", "green")
            if newService not in ("", "y", "yes"):
                break
            data['service'] += [addService()]
        isGood = prompt("Correct? [Y/n]", "green")
        if isGood in ("", "y", "yes"):
            # If its right, return the host info
            return {'ip': ip, 'name': hostname, 'os': os}


def addNetwork():
    '''
    Add a network to the config. add hosts to each network
    '''
    data = {}
    # Get the network ip. Keep trying until it is right
    while True:
        try:
            ip = prompt(
                'Network IP (e.g. "10.2.x.0"): ')
            ip = ".".join(ip.split(".")[:3]).lower()
            data['ip'] = ip
            # Make sure there is an 'x' in the ip
            ip.index("x")
            break
        except Exception as E:
            print("Invalid Network Name")
    # get the network name
    data['name'] = prompt('Network name (e.g. "cloud"): ')
    # Add hosts to the network
    data['hosts'] = []
    while True:
        # Keep adding hosts until we are done
        newHost = prompt("Add a host to this network? [Y/n]", "green")
        if newHost not in ("", "y", "yes"):
            break
        # Create a new host and add it to the dataset
        data['hosts'] += [addHost(ip)]
    return data


def addNetworks():
    data = []
    while True:
        # Keep adding networks until we are done
        newNetwork = prompt("Add network? [Y/n]", "green")
        if newNetwork not in ("", "y", "yes"):
            break
        # Create a new network and add it to the dataset
        data += [addNetwork()]
    return data


def main():
    '''
    Call all the generate functions and build a json config
    '''
    config = {}
    # Get the teams
    config['teams'] = getTeamRange()
    # Get the networks
    config['networks'] = addNetworks()
    print(json.dumps(config, indent=4))
    with open("newtopology.json", "w") as fil:
        fil.write(json.dumps(config, indent=2))
        fil.write("\n")
    print("topology saved to newtopology.json", file=sys.stderr)


if __name__ == '__main__':
    main()