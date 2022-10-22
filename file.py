import os
import tarfile
import config
import re


def check_folder_write_access(path):
    if os.access(path, os.W_OK) is not True:
        print(f'Error: {path} does not exist or is not writeable.')
        exit(1)


def create_folder_if_not_existing(path):
    os.makedirs(path, exist_ok=True)


def check_ip_exists_in_file(file):
    try:
        directory = os.path.dirname(__file__)
        filename = os.path.join(directory, file)
        with open(filename, 'r', encoding='utf-8') as fin:
            lines = fin.read().splitlines()
    except Exception as infile:
        print(f"Input file read error: {infile}")
        exit(1)

    for line in lines:
        ipreturn = re.search(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', line)  # mask IP format
        if ipreturn:  # return if IP is found
            return
    print(f"Error: No IP found in {config.clientfile}. Please enter hostname + IP (or mount an external client file).")
    exit(1)


def get_clients():
    try:
        directory = os.path.dirname(__file__)
        filename = os.path.join(directory, config.clientfile)
        with open(filename, 'r', encoding='utf-8') as fin:
            lines = fin.read().splitlines()
    except Exception as infile:
        print(f"Input file read error: {infile}")
        exit(1)

    # create clients dict
    print("converting to dict")
    clients = {}
    for line in lines:
        line = line.strip()
        if line[:1] != '#' and line:  # ignore comment lines and blank lines
            host, ip = line.split(' ', 1)
            clients.update({host: ip})
    return clients


def create_db_backup(client):
    with tarfile.open(f'{config.persistence_path}/{client}.tar.bz2', "w:bz2") as tar:
        tar.add(f'{config.db_path}/{client}.db', arcname=f'{client}.db')


def restore_db_backup(client):
    with tarfile.open(f'{config.persistence_path}/{client}.tar.bz2') as tar:
        tar.extractall(path=config.db_path)


def write_content_to_file(content, file, writetype):
    try:
        directory = os.path.dirname(__file__)
        filename = os.path.join(directory, file)
        with open(filename, writetype, encoding='utf-8') as fout:
            fout.write(content)
    except Exception as fe:
        print(f"Content writing to file error: {fe}")


def file_exists(filepath):
    if os.path.exists(filepath):
        return True
    else:
        return False
