cpu_table = '''
    CREATE TABLE IF NOT EXISTS cpu (
    ts DATE DEFAULT (datetime('now','localtime')),
    cpu_max FLOAT DEFAULT 100, cpu_usage FLOAT
);'''

ram_table = '''
    CREATE TABLE IF NOT EXISTS ram (
    ts DATE DEFAULT (datetime('now','localtime')),
    mem_total INTEGER, mem_usage INTEGER
);'''

swap_table = '''
    CREATE TABLE IF NOT EXISTS swap (
    ts DATE DEFAULT (datetime('now','localtime')),
    swap_total INTEGER, swap_usage INTEGER
);'''

disk_table = '''
    CREATE TABLE IF NOT EXISTS disk (
    ts DATE DEFAULT (datetime('now','localtime')),
    vol1_total INTEGER, vol1_used INTEGER,
    vol2_total INTEGER, vol2_used INTEGER,
    vol3_total INTEGER, vol3_used INTEGER,
    vol4_total INTEGER, vol4_used INTEGER,
    vol5_total INTEGER, vol5_used INTEGER
);'''

network_table = '''
    CREATE TABLE IF NOT EXISTS network (
    ts DATE DEFAULT (datetime('now','localtime')),
    device1_rx_bytes INTEGER, device1_tx_bytes INTEGER,
    device2_rx_bytes INTEGER, device2_tx_bytes INTEGER,
    device3_rx_bytes INTEGER, device3_tx_bytes INTEGER,
    device4_rx_bytes INTEGER, device4_tx_bytes INTEGER,
    device5_rx_bytes INTEGER, device5_tx_bytes INTEGER
);'''

uptime_table = '''
    CREATE TABLE IF NOT EXISTS uptime (
    ts DATE DEFAULT (datetime('now','localtime')),
    max_uptime float DEFAULT 0, uptime float
);'''

disk_path_table = '''
    CREATE TABLE IF NOT EXISTS disk_path (
    vol1 TEXT PRIMARY KEY, vol2 TEXT,
    vol3 TEXT, vol4 TEXT,
    vol5 TEXT
);'''

network_name_table = '''
    CREATE TABLE IF NOT EXISTS network_name (
    device1 TEXT PRIMARY KEY, device2 TEXT,
    device3 TEXT, device4 TEXT,
    device5 TEXT
);'''

cpu_value = 'INSERT INTO cpu (cpu_usage) VALUES ({});'

ram_value = 'INSERT INTO ram (mem_total, mem_usage) VALUES ({}, {});'

swap_value = 'INSERT INTO swap (swap_total, swap_usage) VALUES ({}, {});'

disk_value = '''INSERT INTO disk (vol1_total, vol1_used,
             vol2_total, vol2_used,
             vol3_total, vol3_used,
             vol4_total, vol4_used,
             vol5_total, vol5_used)
             VALUES ({}, {}, {}, {}, {}, {}, {}, {}, {}, {});
'''

network_value = '''
    INSERT INTO network (
    device1_rx_bytes, device1_tx_bytes,
    device2_rx_bytes, device2_tx_bytes,
    device3_rx_bytes, device3_tx_bytes,
    device4_rx_bytes, device4_tx_bytes,
    device5_rx_bytes, device5_tx_bytes)
    VALUES ({}, {}, {}, {}, {}, {}, {}, {}, {}, {});
'''

uptime_value = 'INSERT INTO uptime (uptime) VALUES ({});'

disk_path_value = '''REPLACE INTO disk_path (
    vol1, vol2, vol3, vol4, vol5)
    VALUES ('{}', '{}', '{}', '{}', '{}');
'''

network_name_value = '''REPLACE INTO network_name (
    device1, device2, device3, device4, device5)
    VALUES ('{}', '{}', '{}', '{}', '{}');
'''
