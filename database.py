import sqlite3
import os
import config
import sql
import file

db_date_span = {
    'hour': '-60 minutes',
    'day': '-1 day',
    'week': '-7 days',
    'month': '-1 month',
    'year': '-1 year'}


def create_connection(client):

    # restore db backup if db file is missing and backup exists
    if not os.path.isfile(f'{config.db_path}/{client}.db') and os.path.isfile(f'{config.persistence_path}/{client}.tar.bz2'):
        print(f'{client} db not found, but backup found. Restoring backup.')
        file.restore_db_backup(client)

    # create db connection and create new db if both db and backup are missing
    conn = None
    try:
        conn = sqlite3.connect(f'{config.db_path}/{client}.db', timeout=12)
        return conn
    except Exception as e:
        print(e)
        conn.close()
    return conn


def create_tables(conn):
    try:
        c = conn.cursor()

        # create value tables
        c.execute(sql.cpu_table)
        c.execute(sql.ram_table)
        c.execute(sql.swap_table)
        c.execute(sql.disk_table)
        c.execute(sql.network_table)
        c.execute(sql.uptime_table)

        # create device name tables
        c.execute(sql.disk_path_table)
        c.execute(sql.network_name_table)
    except Exception as creation_e:
        print(creation_e)


def store_values(conn, client, clients_data_parsed):

    # grab all values from dict
    if 'cpu' in clients_data_parsed[client]:
        cpu_usage = clients_data_parsed[client]['cpu']
    if 'ram' in clients_data_parsed[client]:
        mem_total = clients_data_parsed[client]['ram']['mem_total']
        mem_usage = clients_data_parsed[client]['ram']['mem_usage']
    if 'swap' in clients_data_parsed[client]:
        swap_total = clients_data_parsed[client]['swap']['swap_total']
        swap_usage = clients_data_parsed[client]['swap']['swap_usage']
    if 'disk' in clients_data_parsed[client]:
        vol1_total = clients_data_parsed[client]['disk']['vol1']['disk_total']
        vol1_used = clients_data_parsed[client]['disk']['vol1']['disk_used']
        vol2_total = clients_data_parsed[client]['disk']['vol2']['disk_total']
        vol2_used = clients_data_parsed[client]['disk']['vol2']['disk_used']
        vol3_total = clients_data_parsed[client]['disk']['vol3']['disk_total']
        vol3_used = clients_data_parsed[client]['disk']['vol3']['disk_used']
        vol4_total = clients_data_parsed[client]['disk']['vol4']['disk_total']
        vol4_used = clients_data_parsed[client]['disk']['vol4']['disk_used']
        vol5_total = clients_data_parsed[client]['disk']['vol5']['disk_total']
        vol5_used = clients_data_parsed[client]['disk']['vol5']['disk_used']
    if 'network' in clients_data_parsed[client]:
        device1_rx_bytes = clients_data_parsed[client]['network']['device1']['rx_bytes']
        device1_tx_bytes = clients_data_parsed[client]['network']['device1']['tx_bytes']
        device2_rx_bytes = clients_data_parsed[client]['network']['device2']['rx_bytes']
        device2_tx_bytes = clients_data_parsed[client]['network']['device2']['tx_bytes']
        device3_rx_bytes = clients_data_parsed[client]['network']['device3']['rx_bytes']
        device3_tx_bytes = clients_data_parsed[client]['network']['device3']['tx_bytes']
        device4_rx_bytes = clients_data_parsed[client]['network']['device4']['rx_bytes']
        device4_tx_bytes = clients_data_parsed[client]['network']['device4']['tx_bytes']
        device5_rx_bytes = clients_data_parsed[client]['network']['device5']['rx_bytes']
        device5_tx_bytes = clients_data_parsed[client]['network']['device5']['tx_bytes']
    if 'uptime' in clients_data_parsed[client]:
        uptime = format(float(clients_data_parsed[client]['uptime']) / 86400, '.2f')  # grab and convert from seconds  to days

    # connect and save all available values
    try:
        c = conn.cursor()
        if 'cpu' in clients_data_parsed[client]:
            c.execute(sql.cpu_value.format(cpu_usage))
        if 'ram' in clients_data_parsed[client]:
            c.execute(sql.ram_value.format(mem_total, mem_usage))
        if 'swap' in clients_data_parsed[client]:
            c.execute(sql.swap_value.format(swap_total, swap_usage))
        if 'disk' in clients_data_parsed[client]:
            c.execute(sql.disk_value.format(vol1_total, vol1_used,
                vol2_total, vol2_used, vol3_total, vol3_used,
                vol4_total, vol4_used, vol5_total, vol5_used))
        if 'network' in clients_data_parsed[client]:
            c.execute(sql.network_value.format(device1_rx_bytes,
                device1_tx_bytes, device2_rx_bytes,
                device2_tx_bytes, device3_rx_bytes,
                device3_tx_bytes, device4_rx_bytes,
                device4_tx_bytes, device5_rx_bytes,
                device5_tx_bytes))
        if 'uptime' in clients_data_parsed[client]:
            c.execute(sql.uptime_value.format(uptime))
    except Exception as store_e:
        print(f'DB storage error: {store_e}')


def store_device_names(conn, client, clients_data_parsed):

    # grab all values from dict
    if 'disk' in clients_data_parsed[client]:
        # grab all disk paths from dict
        vol1 = clients_data_parsed[client]['disk']['vol1']['path']
        vol2 = clients_data_parsed[client]['disk']['vol2']['path']
        vol3 = clients_data_parsed[client]['disk']['vol3']['path']
        vol4 = clients_data_parsed[client]['disk']['vol4']['path']
        vol5 = clients_data_parsed[client]['disk']['vol5']['path']

    if 'network' in clients_data_parsed[client]:
        device1 = clients_data_parsed[client]['network']['device1']['name']
        device2 = clients_data_parsed[client]['network']['device2']['name']
        device3 = clients_data_parsed[client]['network']['device3']['name']
        device4 = clients_data_parsed[client]['network']['device4']['name']
        device5 = clients_data_parsed[client]['network']['device5']['name']

    # connect and save all available values
    try:
        c = conn.cursor()
        if 'disk' in clients_data_parsed[client]:
            c.execute(sql.disk_path_value.format(vol1, vol2, vol3, vol4, vol5))
        if 'network' in clients_data_parsed[client]:
            c.execute(sql.network_name_value.format(device1, device2, device3, device4, device5))

    except Exception as store_e:
        print(f'DB storage error: {store_e}')

def table_exists(conn, table):
    c = conn.cursor()
    with conn:
        c.execute(f"SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = '{table}';")
        return c.fetchone()

def read_data(conn, table):
    c = conn.cursor()
    with conn:
        c.execute(f"SELECT * FROM {table}")
        return c.fetchall()

def get_value_column_name(conn, table, columnNbr):
    c = conn.cursor()
    c.execute(f"PRAGMA table_info({table})")
    tableinfo = c.fetchall()
    columnname = tableinfo[columnNbr][1]
    return columnname

def nbr_of_cols(conn, table):
    c = conn.cursor()
    with conn:
        c.execute(f"pragma table_info({table})")
        tableinfo = c.fetchall()
        nbrOfCols = tableinfo[-1][0]
        return nbrOfCols

def db_records_in_timespan_exist(conn, table, interval):
    timespan = db_date_span.get(interval)
    c = conn.cursor()
    with conn:
        if table_exists(conn, table):
            c.execute(f"SELECT * FROM {table} WHERE ts >= datetime('now', '{timespan}', 'localtime')")
            result = c.fetchall()
            if len(result) == 0:
                return False
            else:
                return True
        else:
            return False

def get_device_label(conn, table, deviceNbr):  # value table
    c = conn.cursor()
    with conn:
        c.execute(f"pragma table_info({table})")
        tableinfo = c.fetchall()
        colname = tableinfo[round(deviceNbr/2)-1][1]
        c.execute(f"select MAX({colname}) from {table}")
        return c.fetchone()[0]

def get_device_enumeration(conn, table, deviceNbr):  # path/nw_device table
    c = conn.cursor()
    with conn:
        c.execute(f"pragma table_info({table})")
        tableinfo = c.fetchall()
        colname = tableinfo[deviceNbr][1]
        return colname.split("_", 1)[0]

def get_minimum_value(conn, column, table, interval):
    timespan = db_date_span.get(interval)
    c = conn.cursor()
    with conn:
        c.execute(f"SELECT min({column}) FROM {table} WHERE ts >= datetime('now', '{timespan}', 'localtime')")
        result = int(round(float(format(c.fetchone()[0]))))
        return result

def get_maximum_value(conn, column, table, interval):
    timespan = db_date_span.get(interval)
    c = conn.cursor()
    with conn:
        c.execute(f"SELECT max({column}) FROM {table} WHERE ts >= datetime('now', '{timespan}', 'localtime')")
        result = int(round(float(format(c.fetchone()[0]))))
        return result

def get_average_value(conn, column, table, interval):
    timespan = db_date_span.get(interval)
    c = conn.cursor()
    with conn:
        c.execute(f"SELECT avg({column}) FROM {table} WHERE ts >= datetime('now', '{timespan}', 'localtime')")
        result = int(round(float(format(c.fetchone()[0]))))
        return result

def get_current_value(conn, column, table):
    c = conn.cursor()
    with conn:
        c.execute(f"SELECT {column} FROM {table} WHERE ts= (SELECT max (ts) FROM {table})")
        result = int(round(float(format(c.fetchone()[0]))))
        return result

def get_minimum_value_float(conn, column, table, interval):
    timespan = db_date_span.get(interval)
    c = conn.cursor()
    with conn:
        c.execute(f"SELECT min({column}) FROM {table} WHERE ts >= datetime('now', '{timespan}', 'localtime')")
        result = float(format(c.fetchone()[0]))
        return result

def get_maximum_value_float(conn, column, table, interval):
    timespan = db_date_span.get(interval)
    c = conn.cursor()
    with conn:
        c.execute(f"SELECT max({column}) FROM {table} WHERE ts >= datetime('now', '{timespan}', 'localtime')")
        result = float(format(c.fetchone()[0]))
        return result

def get_average_value_float(conn, column, table, interval):
    timespan = db_date_span.get(interval)
    c = conn.cursor()
    with conn:
        c.execute(f"SELECT avg({column}) FROM {table} WHERE ts >= datetime('now', '{timespan}', 'localtime')")
        result = float(format(c.fetchone()[0]))
        return result

def get_current_value_float(conn, column, table):
    c = conn.cursor()
    with conn:
        c.execute(f"SELECT {column} FROM {table} WHERE ts= (SELECT max (ts) FROM {table})")
        result = float(format(c.fetchone()[0]))
        return result

def delete_old_values(conn, table):
    try:
        c = conn.cursor()
        c.execute(f"DELETE FROM {table} WHERE ts < DATE('now','-1 year')")
    except Exception as deleteold_e:
        print(deleteold_e)

def close_connection(conn):
    conn.commit()
    conn.close()