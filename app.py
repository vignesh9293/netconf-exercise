import logging
from flask import Flask, request, jsonify
from ncclient import manager
import argparse

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

USERNAME = 'admin'
PASSWORD = 'C1sco12345'
EMULATOR_IP = 'sandbox-iosxr-1.cisco.com'
EMULATOR_PORT = 830

# NETCONF config for creating loopback interface
CREATE_LOOPBACK_INTERFACE_PAYLOAD = '''
<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
    <interface-configurations xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ifmgr-cfg">
        <interface-configuration>
            <interface-name>{}</interface-name>
            <description>{}</description>
            <active>{}</active>
        </interface-configuration>
    </interface-configurations>
</config>
'''

# NETCONF config for deleting loopback interface
DELETE_LOOPBACK_INTERFACE_PAYLOAD = '''
<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
    <interface-configurations xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ifmgr-cfg">
        <interface-configuration operation="delete">
            <interface-name>{}</interface-name>
        </interface-configuration>
    </interface-configurations>
</config>
'''

# function definition to perform the intended netconf operation
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
            return response
        except Exception as e:
            return str(e)

# POST api implementation for creating loopback interface
@app.route('/create_loopback', methods=['POST'])
def create_loopback():
    data = request.json
    interface_name = data.get('name')
    interface_description = data.get('description')
    interface_state = data.get('state')

    if not all([interface_name, interface_description, interface_state]):
        return jsonify({'error': 'Missing required parameters'}), 400

    payload = CREATE_LOOPBACK_INTERFACE_PAYLOAD.format(interface_name, interface_description, interface_state)
    if config['dry_run']:
        print(f'payload to be sent to device : {payload}')
        return jsonify({'result': 'Loopback interface created successfully'}), 200
    else:
        response = perform_netconf_operation(payload)
        if "ok" in response.lower():
            return jsonify({'result': 'Loopback interface created successfully'}), 200
        else:
            return jsonify({'error': f'Failed to create loopback interface. Error: {response}'}), 500

# DELETE method for deleting loopback interface
@app.route('/delete_loopback', methods=['DELETE'])
def delete_loopback():
    data = request.json
    interface_name = data.get('name')

    if not interface_name:
        return jsonify({'error': 'Missing required parameter: name'}), 400

    payload = DELETE_LOOPBACK_INTERFACE_PAYLOAD.format(interface_name)
    if config['dry_run']:
        print(f'payload to be sent to device : {payload}')
        return jsonify({'result': 'Loopback interface deleted successfully'}), 200
    else:
        response = perform_netconf_operation(payload)
        if "ok" in response.lower():
            return jsonify({'result': 'Loopback interface deleted successfully'}), 200
        else:
            return jsonify({'error': f'Failed to delete loopback interface. Error: {response}'}), 500

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Argument parser",
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--dry_run", action="store_true", help="Dry_run")
    args = parser.parse_args()
    config = vars(args)

    app.run(debug=True)
