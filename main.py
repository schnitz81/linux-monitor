import config
import file
import comms
import html_generation
import valueparse
import database
import plotting
import time
from multiprocessing import Process
import sys


def main():

    # check that an IP is entered in client file
    file.check_ip_exists_in_file(config.clientfile)

    # check folders writeability
    file.check_folder_write_access(config.db_path)
    file.check_folder_write_access(config.persistence_path)

    # create plot path if non-existing
    file.create_folder_if_not_existing(config.html_path)

    # start processes
    p_shorttermgraph = Process(target=shorttermgraph)
    p_longtermgraph = Process(target=longtermgraph)

    p_shorttermgraph.start()
    p_longtermgraph.start()

    # create timer for running code cyclic
    timer = time.time()

    # infinite loop
    while True:
        print(f"\n-= {config.scancycletime} sec interval client scan wait... =-\n")
        time.sleep(float(config.scancycletime) - ((time.time() - timer) % float(config.scancycletime)))

        # start client data handling timer
        value_update_timer_start = time.perf_counter()

        # scrape all clients
        clients = file.get_clients()
        clients_data_unparsed = comms.fetch_clients_values(clients)

        # parse values
        clients_data_parsed = valueparse.parse_clients_data(clients_data_unparsed)
        # save values to DB
        for client in clients.keys():

            try:
                if clients_data_parsed[client] is None:
                    print(f"Data for {client} not received. Skipping.")
                    continue
            except KeyError as keyerror:
                print(f"Key error: {keyerror}")
                print(f"Data likely not received from client {client}. Skipping. +n")
                continue

            # connect to database
            print(f"Connecting to {client} db.")
            conn = database.create_connection(client)

            # create tables if db is empty
            if conn is not None:
                print(f"Aligning {client} tables in DB.")
                database.create_tables(conn)
                print(f"Aligning {client} device names in DB.")
                database.store_device_names(conn, client, clients_data_parsed)
            else:
                print("Error! cannot create db.")
                exit(1)

            # store values into DB
            print(f"Storing {client} records in db.")
            database.store_values(conn, client, clients_data_parsed)

            # close database connection
            print(f"Closing {client} db connection.")
            database.close_connection(conn)

        value_update_timer_stop = time.perf_counter()
        print(f"Clients scan + value handling in {value_update_timer_stop - value_update_timer_start:0.2f} seconds\n")

        # render html
        html_generation.generate_webgui(clients, clients_data_parsed)


def shorttermgraph():

    # create timer for running code cyclic every minute
    timer = time.time()

    # infinite loop
    while True:
        print("\n-= 15 sec chart plotting wait... =-\n")
        time.sleep(15.0 - ((time.time() - timer) % 15.0))

        print("\n-= Executing short-term loop. =-")

        # start client data handling timer
        shorttermtimer_start = time.perf_counter()

        # get all clients
        clients = file.get_clients()

        for client in clients.keys():

            # connect to db
            print(f"Connecting to {client} db.")
            conn = database.create_connection(client)

            print("Plotting hour and day graphs.")

            # plot cpu
            if database.db_records_in_timespan_exist(conn, 'cpu', 'hour'):
                plotting.plot_single_graph(conn, client, 'cpu', 'hour')
                plotting.plot_single_graph(conn, client, 'cpu', 'day')

            # plot ram
            if database.db_records_in_timespan_exist(conn, 'ram', 'hour'):
                plotting.plot_single_graph(conn, client, 'ram', 'hour')
                plotting.plot_single_graph(conn, client, 'ram', 'day')

            # plot swap
            if database.db_records_in_timespan_exist(conn, 'swap', 'hour'):
                plotting.plot_single_graph(conn, client, 'swap', 'hour')
                plotting.plot_single_graph(conn, client, 'swap', 'day')

            # plot uptime
            if database.db_records_in_timespan_exist(conn, 'uptime', 'hour'):
                plotting.plot_single_graph(conn, client, 'uptime', 'hour')
                plotting.plot_single_graph(conn, client, 'uptime', 'day')

            # plot disk
            if database.db_records_in_timespan_exist(conn, 'disk', 'hour'):
                plotting.plot_multi_graph(conn, client, 'disk', 'hour')
                plotting.plot_multi_graph(conn, client, 'disk', 'day')

            # plot network
            if database.db_records_in_timespan_exist(conn, 'network', 'hour'):
                plotting.plot_multi_graph(conn, client, 'network', 'hour')
                plotting.plot_multi_graph(conn, client, 'network', 'day')

            print("Hour and day graphs plotted.")

            # close database connection
            print(f"Closing {client} db connection.")
            database.close_connection(conn)

        shorttermtimer_stop = time.perf_counter()
        print(f"\nPlotted short term graphs in {shorttermtimer_stop - shorttermtimer_start:0.2f} seconds\n")


def longtermgraph():

    # create timer for running code cyclic every minute
    timer = time.time()

    # infinite loop
    while True:
        print("\n-= 3600 sec chart plotting wait... =-\n")
        time.sleep(3600.0 - ((time.time() - timer) % 3600.0))

        print("\n---==== Executing long-term loop. ====---")

        # start client data handling timer
        longtermgraphtimer_start = time.perf_counter()

        # get all clients
        clients = file.get_clients()

        for client in clients.keys():

            # connect to db
            print(f"Connecting to {client} db.")
            conn = database.create_connection(client)

            # plot cpu
            if database.db_records_in_timespan_exist(conn, 'cpu', 'week'):
                print(f'Plotting longterm graphs for {client} cpu.')
                plotting.plot_single_graph(conn, client, 'cpu', 'week')
                plotting.plot_single_graph(conn, client, 'cpu', 'month')
                plotting.plot_single_graph(conn, client, 'cpu', 'year')
                print(f'Deleting old {client} cpu records.')
                database.delete_old_values(conn, 'cpu')

            # plot ram
            if database.db_records_in_timespan_exist(conn, 'ram', 'week'):
                print(f'Plotting longterm graphs for {client} ram.')
                plotting.plot_single_graph(conn, client, 'ram', 'week')
                plotting.plot_single_graph(conn, client, 'ram', 'month')
                plotting.plot_single_graph(conn, client, 'ram', 'year')
                print(f'Deleting old {client} ram records.')
                database.delete_old_values(conn, 'ram')

            # plot swap
            if database.db_records_in_timespan_exist(conn, 'swap', 'week'):
                print(f'Plotting longterm graphs for {client} swap.')
                plotting.plot_single_graph(conn, client, 'swap', 'week')
                plotting.plot_single_graph(conn, client, 'swap', 'month')
                plotting.plot_single_graph(conn, client, 'swap', 'year')
                print(f'Deleting old {client} swap records.')
                database.delete_old_values(conn, 'swap')

            # plot uptime
            if database.db_records_in_timespan_exist(conn, 'uptime', 'week'):
                print(f'Plotting longterm graphs for {client} uptime.')
                plotting.plot_single_graph(conn, client, 'uptime', 'week')
                plotting.plot_single_graph(conn, client, 'uptime', 'month')
                plotting.plot_single_graph(conn, client, 'uptime', 'year')
                print(f'Deleting old {client} uptime records.')
                database.delete_old_values(conn, 'uptime')

            # plot disk
            if database.db_records_in_timespan_exist(conn, 'disk', 'week'):
                print(f'Plotting longterm graphs for {client} disk.')
                plotting.plot_multi_graph(conn, client, 'disk', 'week')
                plotting.plot_multi_graph(conn, client, 'disk', 'month')
                plotting.plot_multi_graph(conn, client, 'disk', 'year')
                print(f'Deleting old {client} disk records.')
                database.delete_old_values(conn, 'disk')

            # plot network
            if database.db_records_in_timespan_exist(conn, 'network', 'week'):
                print(f'Plotting longterm graphs for {client} network.')
                plotting.plot_multi_graph(conn, client, 'network', 'week')
                plotting.plot_multi_graph(conn, client, 'network', 'month')
                plotting.plot_multi_graph(conn, client, 'network', 'year')
                print(f'Deleting old {client} network records.')
                database.delete_old_values(conn, 'network')

            # close database connection
            print(f"Closing {client} db connection.")
            database.close_connection(conn)

            # backup db
            print(f"Backuping {client} db.\n")
            file.create_db_backup(client)

        longtermgraphtimer_stop = time.perf_counter()
        print(f"\nPlotted short term graphs in {longtermgraphtimer_stop - longtermgraphtimer_start:0.2f} seconds\n")
        print("---==== Long-term loop finished. ====---\n")


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        crashmsg = ["Error on line {}".format(sys.exc_info()[-1].tb_lineno), "\n", e]
        print(crashmsg)
        crashtime = str(time.time())
        with open("/tmp/pythoncrash-" + crashtime + ".log", "w") as crashlog:
            for i in crashmsg:
                i = str(i) + '\n'
                crashlog.write(i)
