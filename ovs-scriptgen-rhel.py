__author__ = "Miguel Cabrerizo"
__copyright__ = "Copyright 2015, Miguel Cabrerizo - ArtemIT Labs"
__license__ = "GPLv3"
__version__ = "1.0.1"
__maintainer__ = "Miguel Cabrerizo"
__email__ = "mcabrerizo@artemit.com.es"

import socket
import argparse

DEVICE_NAME = 0
BRIDGE_NAME = 1
PATCH_PEER_NAME = 2
WARNING_NAMES_DUPLICATED = 'WARNING: The name of the device and the Open vSwitch\'s bridge are the same!'
DESCRIPTION = ''' This simple script will generate network configuration scripts integrating Open vSwitch
for RHEL-based Linux distributions like CentOS. Note that the Open vSwitch integration is optional but is quite useful.
Bugs, suggestions...: mcabrerizo@artemit.com.es
'''

def ask_for_boot():
    option_ask = '?'
    while option_ask not in ['yes', 'no']:
        option_ask = raw_input('Do you want the interface to start at boot ([y]/n)?\n')
        if not option_ask or option_ask == 'y':
            option_ask = 'yes'
        if option_ask == 'n':
            option_ask = 'no'

    return option_ask


def ask_for_name(asked_name):
    name = ''
    while not name:
        if asked_name == BRIDGE_NAME:
            name = raw_input('What\'s the name of the Open vSwitch bridge associated to the interface?\n')
        if asked_name == DEVICE_NAME:
            name = raw_input('What will be the name of the network interface?\n')
        if asked_name == PATCH_PEER_NAME:
            name = raw_input('What\'s the name of the Open vSwitch Patch Port peer?\n')

    return name


def ask_for_tunnel_type():

    option_ask = '?'
    tunnel_option = ''
    while option_ask not in ['1', '2']:
        print 'What type of Open vSwitch tunnel interface are you configuring?\n'
        print '\t1) GRE'
        print '\t2) VXLAN\n'
        option_ask = raw_input('Please specify the number to select an Open vSwitch type: \n')
        if option_ask == '1':
            tunnel_option = 'gre'
        if option_ask == '2':
            tunnel_option = 'vxlan'
    return tunnel_option


def get_bridge_name(arg_nic_name):

    repeat_bridge_name = True
    bridge_name = ''
    while repeat_bridge_name:
        bridge_name = ask_for_name(BRIDGE_NAME)
        if bridge_name == arg_nic_name:
            print WARNING_NAMES_DUPLICATED
            bridge_name_dup_option = raw_input('Are you sure this is what you want? (y/[n])?\n')
            if bridge_name_dup_option == 'y':
                repeat_bridge_name = False
        else:
            repeat_bridge_name = False

    return bridge_name

def ask_for_remote_ip_tunnel():

    repeat_ip = True

    while repeat_ip:

        remote_ip = ''
        while not remote_ip:
            remote_ip = raw_input('Specify the remote IPv4 address for the tunnel end in dot-decimal notation A.B.C.D (e.g 192.168.1.1):\n')
            try:
                socket.inet_aton(remote_ip)
            except socket.error:
                print 'Wrong format. Please, try again'
                remote_ip = ''

            option_ask = '?'
            while option_ask not in ['y','n']:
                option_ask = raw_input('Are you happy with the remote ip ([y]/n)?\n')
                if not option_ask or option_ask == 'y':
                    option_ask = 'y'
                    repeat_ip = False
                if option_ask == 'n':
                    repeat_ip = True

    print 'Optional - Specify other options for tunnel interfaces as a space separated list of '
    print 'column[:key]=value options, e.g the encryption key.'
    print 'Use the man page for ovs-vswitchd.conf.db.5 for more information about Tunnel Configuration'

    option_ask = raw_input('press Enter when finished \n')
    return remote_ip + ' ' + option_ask


def ask_for_type():
    option_ask = 0
    while option_ask not in range(1, 7):
        print 'What type of Open vSwitch network interface do you want to create?\n'
        print '\t1) Bridge'
        print '\t2) Physical or Virtual port'
        print '\t3) Internal port (e.g a tagged VLAN)'
        print '\t4) Bond'
        print '\t5) Tunnel'
        print '\t6) Patch port\n'

        try:
            option_ask = int(raw_input('Please specify the number to select an Open vSwitch type: \n'))
        except ValueError:
            print 'Select a number between 1 and 6 to select an Open vSwitch valid type\n'
            option_ask = 0

    return option_ask


def ask_for_dhcp():

    print 'Specify the name of all the interfaces that can reach the DHCP server as a space separated list e.g eth0 eth1'
    dhcp_ask = raw_input('press Enter when finished \n')
    return dhcp_ask


def ask_for_port_options():

    print 'Optional - Specify the options for the port interface as a space separated list of '
    print 'column[:key]=value options, e.g tag=100 to configure the port as an access port for VLAN 100).'
    print 'Use the man page for ovs-vswitchd.conf.db.5 for more information about VLAN Configuration'

    option_ask = raw_input('press Enter when finished \n')

    return option_ask


def ask_for_bonding():

    print 'Specify the name of all the interfaces that will be bonded as a space '
    print 'separated list, e.g gige-1b-0 gige-1b-1 gige-21-0 gige-21-1'
    bonded_interfaces = raw_input('press Enter when finished \n')

    print 'Optional - Specify the options for the bonded interface as a space separated list of '
    print 'column[:key]=value options, e.g bond_mode=balance-tcp lacp=active). '
    print 'Use the man page for ovs-vswitchd.conf.db.5 for more information about Bonding Configuration'
    bonded_options = raw_input('press Enter when finished \n')

    return bonded_interfaces, bonded_options


def ask_for_static_ip_and_mask():

    repeat_ip = True
    while repeat_ip:

        ip = ''
        while not ip:
            ip = raw_input('Specify the static IPv4 address in dot-decimal notation A.B.C.D (e.g 192.168.1.1):\n')
            try:
                socket.inet_aton(ip)
            except socket.error:
                print 'Wrong format. Please, try again'
                ip = ''

        mask = ''
        while not mask:
            mask = raw_input('Specify the network mask in dot-decimal notation A.B.C.D (e.g 255.255.255.192):\n')
            try:
                socket.inet_aton(mask)
            except socket.error:
                print 'Wrong format. Please, try again'
                mask = ''

        option_gateway = '?'
        gateway = ''
        while option_gateway not in ['y', 'n']:
            option_gateway = raw_input('Do you want to add a gateway? (y/[n])?\n')
            if not option_gateway or option_gateway == 'n':
                option_gateway = 'n'
            if option_gateway == 'y':
                gateway = ''
                while not gateway:
                    gateway = raw_input('Specify the gateway in dot-decimal notation A.B.C.D (e.g 192.168.1.1):\n')
                try:
                    socket.inet_aton(gateway)
                except socket.error:
                    print 'Wrong format. Please, try again'
                    gateway = ''

        option_dns1 = '?'
        dns1 = ''
        dns2 = ''
        while option_dns1 not in ['y', 'n']:
            option_dns1 = raw_input('Do you want to add a DNS server? (y/[n])?\n')
            if not option_dns1 or option_dns1 == 'n':
                option_dns1 = 'n'
            if option_dns1 == 'y':
                dns1 = ''
                while not dns1:
                    dns1 = raw_input('Specify the DNS server address in dot-decimal notation ' +
                                     'A.B.C.D (e.g 192.168.1.1):\n')
                try:
                    socket.inet_aton(dns1)
                    option_dns2 = '?'
                    while option_dns2 not in ['y', 'n']:
                        option_dns2 = raw_input('Do you want to add another DNS server? (y/[n])?\n')
                        if not option_dns2 or option_dns2 == 'n':
                            option_dns2 = 'n'
                        if option_dns2 == 'y':
                            dns2 = ''
                            while not dns2:
                                dns2 = raw_input(
                                    'Specify the DNS server address in dot-decimal notation ' +
                                    'A.B.C.D (e.g 192.168.1.1):\n')
                            try:
                                socket.inet_aton(dns2)
                            except socket.error:
                                print 'Wrong format. Please, try again'
                                dns2 = ''

                except socket.error:
                    print 'Wrong format. Please, try again'
                    dns1 = ''

        option_ip = '?'
        while option_ip not in ['y','n']:
            option_ip = raw_input('Are you happy with your settings ([y]/n)?\n')
            if not option_ip or option_ip == 'y':
                option_ip = 'y'
                repeat_ip = False
            if option_ip == 'n':
                repeat_ip = True

    return ip, mask, gateway, dns1, dns2


def ask_for_extra():
    extra = raw_input('If you want to add extra optional ovs-vsctl commands, separated by \"--\", enter them now,'
                      ' otherwise please Enter to continue:\n')

    return extra

def generate_port_config(arg_ovs_type,arg_nic_name):

    set_ip = '?'
    port_options = None
    bridge_name = None

    if arg_ovs_type != 'OVSBridge':
        bridge_name = get_bridge_name(arg_nic_name)

    while set_ip not in ['y','n']:
        set_ip = raw_input('Do you want to configure IPv4 addressing for this interface? ([y]/n )?\n')
        if not set_ip or set_ip == 'y':

            set_ip = 'y'
            option = '?'

            while option not in ['y','n']:
                option = raw_input('Do you want to use a dynamic IPv4 address? ([y]/n )?\n')
                if not option or option == 'y':
                    option = 'y'
                    dhcp = ask_for_dhcp()
                    if arg_ovs_type != 'OVSBridge':
                        port_options = ask_for_port_options()
                    extra_options = ask_for_extra()
                    generate_config(nic_name, arg_ovs_type, boot_option, extra_options,
                                        arg_port_options=port_options,arg_dhcp=dhcp,
                                        arg_bridge=bridge_name, arg_hotplug=True)

                if option == 'n':
                    address = ask_for_static_ip_and_mask()
                    if arg_ovs_type != 'OVSBridge':
                        port_options = ask_for_port_options()
                    extra_options = ask_for_extra()
                    generate_config(nic_name, arg_ovs_type, boot_option, extra_options,
                                    arg_port_options=port_options,arg_ip_address=address,
                                    arg_bridge=bridge_name, arg_hotplug=True)
        else:
            if arg_ovs_type != 'OVSBridge':
                        port_options = ask_for_port_options()
            extra_options = ask_for_extra()
            generate_config(nic_name, arg_ovs_type, boot_option, extra_options,
                            arg_port_options=port_options,arg_bridge=bridge_name, arg_hotplug=True)


def generate_config(arg_name, arg_type, arg_boot, arg_extra,
                    arg_dhcp=None,arg_ip_address=None,arg_bridge=None,arg_port_options=None,
                    arg_bonding=None, arg_tunnel=None, arg_patch=None,arg_hotplug=None):

    print '\nFinished!'
    print 'Please copy the following content in a file named ifcfg-' + arg_name
    print 'inside the /etc/sysconfig/network-scripts directory.'
    print '\n'+'='*20

    print 'DEVICE='+arg_name
    print 'ONBOOT='+arg_boot
    print 'DEVICETYPE=ovs'
    print 'TYPE='+arg_type

    if arg_ip_address is not None:
        print 'BOOTPROTO=static'
        print 'IPADDR='+arg_ip_address[0]
        print 'NETMASK='+arg_ip_address[1]
        if arg_ip_address[2]:
            print 'GATEWAY='+arg_ip_address[2]
        if arg_ip_address[3]:
            print 'DNS1='+arg_ip_address[3]
        if arg_ip_address[4]:
            print 'DNS2='+arg_ip_address[4]

    if arg_dhcp is not None:
        print 'OVSBOOTPROTO="dhcp"'
        if arg_dhcp:
            print 'OVSDHCPINTERFACES="'+arg_dhcp+'"'

    if arg_bridge is not None:
        print 'OVS_BRIDGE='+arg_bridge

    if arg_dhcp is None and arg_ip_address is None:
        print 'BOOTPROTO=none'

    if arg_tunnel is not None:
        print 'OVS_TUNNEL_TYPE='+arg_tunnel[0]
        print 'OVS_TUNNEL_OPTIONS=options:remote_ip='+arg_tunnel[1]

    if arg_patch is not None:
        print 'OVS_PATCH_PEER='+arg_patch

    if arg_port_options is not None:
        if arg_port_options:
            print 'OVS_OPTIONS="' + arg_port_options +'"'

    if arg_extra:
        print 'OVS_EXTRA="'+arg_extra + '"'

    if arg_bonding is not None:
        print 'BOND_IFACES="' + arg_bonding[0] +'"'
        if arg_bonding[1]:
            print 'OVS_OPTIONS="' + arg_bonding[1] +'"'

    if arg_hotplug is not None:
        print 'HOTPLUG=no'

    print '='*20+'\n'
    print 'Once the file has been created load your new network configuration using:\n'
    print 'For RHEL/CentOS 7: nmcli conn reload'
    print 'For RHEL/CentOS 6: service network restart'
    print ''


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.parse_args()

    repeat = True

    while repeat:

        welcome = '\n\nWelcome! Let\'s start'
        print welcome
        print '-'*len(welcome)

        nic_name = ask_for_name(DEVICE_NAME)
        boot_option = ask_for_boot()
        type_option = ask_for_type()

        if type_option == 1:
            ovs_type = 'OVSBridge'
            generate_port_config(ovs_type,nic_name)

        if type_option == 2:
            ovs_type = 'OVSPort'
            generate_port_config(ovs_type,nic_name)

        if type_option == 3:
            ovs_type = 'OVSIntPort'
            generate_port_config(ovs_type,nic_name)

        if type_option == 4:
            ovs_type = 'OVSBond'
            bonding = ask_for_bonding()
            bond_bridge_name = get_bridge_name(nic_name)
            bond_extra_options = ask_for_extra()
            generate_config(nic_name, ovs_type, boot_option, bond_extra_options,
                            arg_bonding=bonding, arg_bridge=bond_bridge_name,arg_hotplug=True)

        if type_option == 5:
            ovs_type = 'OVSTunnel'
            tunnel_type = ask_for_tunnel_type()
            tunnel_remote_ip = ask_for_remote_ip_tunnel()
            tunnel_bridge_name = get_bridge_name(nic_name)
            tunnel_extra_options = ask_for_extra()
            generate_config(nic_name, ovs_type, boot_option, tunnel_extra_options,
                            arg_bridge=tunnel_bridge_name,
                            arg_tunnel=(tunnel_type, tunnel_remote_ip))

        if type_option == 6:
            ovs_type = 'OVSPatchPort'
            patch_bridge_name = get_bridge_name(nic_name)
            patch_peer_name = ask_for_name(PATCH_PEER_NAME)
            patch_extra_options = ask_for_extra()
            generate_config(nic_name, ovs_type, boot_option, patch_extra_options,
                            arg_bridge=patch_bridge_name,
                            arg_patch=patch_peer_name)

        repeat_option = raw_input('Do you want to create another configuration? (y/[n])')

        if not repeat_option or repeat_option == 'n':
            repeat = False
            print 'Bye!'
        if repeat_option == 'y':
            repeat = True