import socket
import config


def fetch_clients_values(clients):
    clients_data = {}
    for client_host, client_ip in clients.items():
        data = retreive_client_value(client_ip)
        clients_data.update({client_host: data})
    return clients_data


def retreive_client_value(client_ip):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as err:
        print("socket creation failed with error %s" % (err))

    try:
        host_ip = socket.gethostbyname(client_ip)
        print(host_ip)
    except socket.gaierror:
        print(f"there was an error resolving client {client_ip}")

    # connecting to the server
    try:
        s.connect((client_ip, config.client_port))
        data = s.recv(4096).decode()
        return data
    except socket.error as err:
        print("socket creation failed with error %s" % (err))
        return None
