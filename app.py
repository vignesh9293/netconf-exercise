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
    <interface-configurations xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ifmgr-cfg">
        <interface-configuration>
            <active>act</active>
            <interface-name>{}</interface-name>
            <description>{}</description>
            <bandwidth>100000</bandwidth>
        </interface-configuration>
    </interface-configurations>
</config>
'''

DELETE_LOOPBACK_INTERFACE_PAYLOAD = '''
<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
    <interface-configurations xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ifmgr-cfg">
        <interface-configuration operation="delete">
            <interface-name>{}</interface-name>
        </interface-configuration>
    </interface-configurations>
</config>
'''

def perform_netconf_operation(xml_content):
    with manager.connect(
        host=EMULATOR_IP,
        port=EMULATOR_PORT,
        username=USERNAME,
        password=PASSWORD,
        hostkey_verify=False,
        allow_agent=False,
        look_for_keys=False,
        device_params={'name': 'iosxr'},
    ) as m:
        try:
            response = m.edit_config(target='running', config=xml_content)
            return response.ok
        except RPCError as e:
            print(f"NETCONF RPC Error: {e}")
            return False

def create_loopback_interface(interface_name, description):
    xml_content = CREATE_LOOPBACK_INTERFACE_PAYLOAD.format(
        interface_name, description
    )
    return perform_netconf_operation(xml_content)

def delete_loopback_interface(interface_name):
    xml_content = DELETE_LOOPBACK_INTERFACE_PAYLOAD.format(interface_name)
    return perform_netconf_operation(xml_content)

if __name__ == '__main__':
    interface_name = 'Loopback986'
    description = 'Test Loopback'

    if create_loopback_interface(interface_name, description):
        print(f'Interface {interface_name} created successfully')

    if delete_loopback_interface(interface_name):
        print(f'Interface {interface_name} deleted successfully')
