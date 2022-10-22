import base64
import json
import copy


def parse_clients_data(clients_data_unparsed):

    # decode base64
    clients_data_parsed = {}
    for client_host, unparsed_data in clients_data_unparsed.items():
        if unparsed_data is not None:
            try:
                clients_data_parsed.update({client_host: json.loads(base64.b64decode(unparsed_data))})
            except Exception as b64decodeerror:
                print(f"Error: Unable to decode json data: {b64decodeerror}")

            try:
                for i in range(1, 6):
                    if 'disk' in clients_data_parsed[client_host]:
                        if f'vol{i}' not in clients_data_parsed[client_host]['disk']:  # check if volume is missing in scraped data
                            # create non-existent disk volumes and set null values
                            clients_data_parsed[client_host]['disk'].update({f'vol{i}': {'path': 'null', 'disk_used': 'null', 'disk_total': 'null'}})

                    if 'network' in clients_data_parsed[client_host]:
                        if f'device{i}' not in clients_data_parsed[client_host]['network']:  # check if device is missing in scraped data
                            # create non-existent network devices and set null values
                            clients_data_parsed[client_host]['network'].update({f'device{i}': {'name': 'null', 'rx_bytes': 'null', 'tx_bytes': 'null'}})
            except Exception as deviceerror:
                print(f"Error: Unable to decode device data from json: {deviceerror}")
        else:
            clients_data_parsed[client_host] = None
    return clients_data_parsed


def update_clients_device_index(client, clients_data_parsed):

    clients_device_index = {}

    # get disk volumes
    if clients_data_parsed[client]['disk'] is not None:
        diskdata = copy.deepcopy(clients_data_parsed[client]['disk'])

        # strip keys that are not path
        for i in range(1, 6):
            for k in list(diskdata[f'vol{i}'].keys()):
                if k != 'path':
                    del diskdata[f'vol{i}'][k]

        # strip null volumes and strip the extra dict
        for i in range(1, 6):
            for k in list(diskdata[f'vol{i}'].values()):
                if k == 'null':
                    del diskdata[f'vol{i}']
                else:
                    diskdata[f'vol{i}'] = diskdata[f'vol{i}']['path']
    else:
        diskdata = {}

    # get network device names
    if clients_data_parsed[client]['network'] is not None:
        networkdata = copy.deepcopy(clients_data_parsed[client]['network'])

        # strip keys that are not name
        for i in range(1, 6):
            for k in list(networkdata[f'device{i}'].keys()):
                if k != 'name':
                    del networkdata[f'device{i}'][k]

        # strip null devices and strip the extra dict
        for i in range(1, 6):
            for k in list(networkdata[f'device{i}'].values()):
                if k == 'null':
                    del networkdata[f'device{i}']
                else:
                    networkdata[f'device{i}'] = networkdata[f'device{i}']['name']
    else:
        networkdata = {}

    clients_device_index.update({client: {'disk': diskdata, 'network': networkdata}})

    return clients_device_index
