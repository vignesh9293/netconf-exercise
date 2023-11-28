import logging
from ncclient import manager
from ncclient.operations import RPCError

logging.basicConfig(level=logging.DEBUG)

USERNAME = 'admin'
PASSWORD = 'C1sco12345'
EMULATOR_IP = 'sandbox-iosxr-1.cisco.com'
EMULATOR_PORT = 830

CREATE_LOOPBACK_INTERFACE_PAYLOAD = '''
<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
    <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
        <interface>
            <name>{}</name>
            <description>{}</description>
            <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">{}</type>
            <enabled>true</enabled>
            <ipv4 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip">
                <address>
                    <ip>{}</ip>
                    <netmask>{}</netmask>
                </address>
            </ipv4>
        </interface>
    </interfaces>
</config>
'''

DELETE_LOOPBACK_INTERFACE_PAYLOAD = '''
<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
    <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
        <interface operation="delete">
            <name>{}</name>
        </interface>
    </interfaces>
</config>
'''

def perform_netconf_operation(xml_content):
    with manager.connect(
        host=EMULATOR_IP,
        port=EMULATOR_PORT,
        username=USERNAME,
        password=PASSWORD,
        hostkey_verify=False,
    ) as m:
        try:
            response = m.edit_config(target='running', config=xml_content)
            return response.ok
        except RPCError as e:
            print(f"NETCONF RPC Error: {e}")
            return False

def create_loopback_interface(interface_name, description, interface_type='ianaift:softwareLoopback', ip_address=None, netmask=None):
    xml_content = CREATE_LOOPBACK_INTERFACE_PAYLOAD.format(
        interface_name, description, interface_type, ip_address, netmask
    )
    return perform_netconf_operation(xml_content)

def delete_loopback_interface(interface_name):
    xml_content = DELETE_LOOPBACK_INTERFACE_PAYLOAD.format(interface_name)
    return perform_netconf_operation(xml_content)

if __name__ == '__main__':
    interface_name = 'Loopback10'
    description = 'Test Loopback'
    ip_address = '192.168.1.1'
    netmask = '255.255.255.0'

    if create_loopback_interface(interface_name, description, ip_address=ip_address, netmask=netmask):
        print(f'Interface {interface_name} created successfully')

    if delete_loopback_interface(interface_name):
        print(f'Interface {interface_name} deleted successfully')
