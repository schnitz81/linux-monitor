import html_templates
import config
import file
import distutils.log
import distutils.dir_util


def generate_webgui(clients, clients_data_parsed):
    print("Generating html...")
    # copy all static files to
    distutils.log.set_verbosity(distutils.log.DEBUG)
    distutils.dir_util.copy_tree('static/', config.html_path, update=1, verbose=1,)

    ### index page ###

    # write index head
    file.write_content_to_file(html_templates.INDEX_HEAD, f'{config.html_path}/index.html', 'w')

    # write client table rows
    for client_host, client_ip in clients.items():
        if client_host not in clients_data_parsed or clients_data_parsed[client_host] is None:
            ledcolor = 'red'
        else:
            ledcolor = 'green'

        clientrow = html_templates.INDEX_CLIENT.format(client_host, client_host, client_ip, ledcolor)
        file.write_content_to_file(clientrow, f'{config.html_path}/index.html', 'a')

    # write index tail
    file.write_content_to_file(html_templates.INDEX_TAIL, f'{config.html_path}/index.html', 'a')

    ### client pages ###

    for client_host, client_ip in clients.items():
        # only update client page if parsed data exists
        if client_host not in clients_data_parsed or clients_data_parsed[client_host] is None:
            continue


        # write client head
        file.write_content_to_file(html_templates.CLIENT_HEAD.format(client_host), f'{config.html_path}/{client_host}.html', 'w')

        # write buttons
        for item in clients_data_parsed[client_host].items():
            if item[0] == 'disk':
                for i in range(1, 6):
                    if f'vol{i}' in clients_data_parsed[client_host]['disk']:
                        if clients_data_parsed[client_host]['disk'][f'vol{i}']['path'] != 'null':
                            file.write_content_to_file(html_templates.CLIENT_BUTTON.format(f'{item[0]}_vol{i}', f'{item[0]}_vol{i}', item[0], f'vol {i}'), f'{config.html_path}/{client_host}.html', 'a')
            elif item[0] == 'network':
                for i in range(1, 6):
                    if f'device{i}' in clients_data_parsed[client_host]['network']:
                        if clients_data_parsed[client_host]['network'][f'device{i}']['name'] != 'null':
                            file.write_content_to_file(html_templates.CLIENT_BUTTON.format(f'{item[0]}_device{i}', f'{item[0]}_device{i}', item[0], clients_data_parsed[client_host]['network'][f'device{i}']['name']), f'{config.html_path}/{client_host}.html', 'a')
            else:
                file.write_content_to_file(html_templates.CLIENT_BUTTON.format(item[0], item[0], item[0], item[0]), f'{config.html_path}/{client_host}.html', 'a')

        # write data records
        for item in clients_data_parsed[client_host].items():

            if item[0] != 'disk' and item[0] != 'network':

                # write data head
                file.write_content_to_file(html_templates.DATA_HEAD.format(item[0]), f'{config.html_path}/{client_host}.html', 'a')

                # write data records
                file.write_content_to_file(html_templates.DATA_RECORD.format(client_host, item[0], 'hour', client_host, item[0], 'hour'), f'{config.html_path}/{client_host}.html', 'a')
                file.write_content_to_file(html_templates.DATA_RECORD.format(client_host, item[0], 'day', client_host, item[0], 'day'), f'{config.html_path}/{client_host}.html', 'a')
                if file.file_exists(f'{config.html_path}/{client_host}-{item[0]}-year.png'):  # only display longterm graphs in html if they are created yet
                    file.write_content_to_file(html_templates.DATA_RECORD.format(client_host, item[0], 'week', client_host, item[0], 'week'), f'{config.html_path}/{client_host}.html', 'a')
                    file.write_content_to_file(html_templates.DATA_RECORD.format(client_host, item[0], 'month', client_host, item[0], 'month'), f'{config.html_path}/{client_host}.html', 'a')
                    file.write_content_to_file(html_templates.DATA_RECORD.format(client_host, item[0], 'year', client_host, item[0], 'year'), f'{config.html_path}/{client_host}.html', 'a')

                # write data tail
                file.write_content_to_file(html_templates.DATA_TAIL.format(item[0], item[0], item[0]), f'{config.html_path}/{client_host}.html', 'a')

            elif item[0] == 'disk':
                for i in range(1, 6):
                    if f'vol{i}' in clients_data_parsed[client_host]['disk']:
                        if clients_data_parsed[client_host]['disk'][f'vol{i}']['path'] != 'null':
                            # write data head
                            file.write_content_to_file(html_templates.DATA_HEAD.format(f'{item[0]}_vol{i}'), f'{config.html_path}/{client_host}.html', 'a')

                            # write data records
                            file.write_content_to_file(html_templates.DATA_RECORD_DISK_NETWORK.format(client_host, item[0], f'vol{i}', 'hour', client_host, item[0], f'vol{i}', 'hour'), f'{config.html_path}/{client_host}.html', 'a')
                            file.write_content_to_file(html_templates.DATA_RECORD_DISK_NETWORK.format(client_host, item[0], f'vol{i}', 'day', client_host, item[0], f'vol{i}', 'day'), f'{config.html_path}/{client_host}.html', 'a')
                            if file.file_exists(f'{config.html_path}/{client_host}-{item[0]}-vol{i}-year.png'):  # only display longterm graphs in html if they are created yet
                                file.write_content_to_file(html_templates.DATA_RECORD_DISK_NETWORK.format(client_host, item[0], f'vol{i}', 'week', client_host, item[0], f'vol{i}', 'week'), f'{config.html_path}/{client_host}.html', 'a')
                                file.write_content_to_file(html_templates.DATA_RECORD_DISK_NETWORK.format(client_host, item[0], f'vol{i}', 'month', client_host, item[0], f'vol{i}', 'month'), f'{config.html_path}/{client_host}.html', 'a')
                                file.write_content_to_file(html_templates.DATA_RECORD_DISK_NETWORK.format(client_host, item[0], f'vol{i}', 'year', client_host, item[0], f'vol{i}', 'year'), f'{config.html_path}/{client_host}.html', 'a')

                            # write data tail
                            file.write_content_to_file(html_templates.DATA_TAIL.format(f'{item[0]}_vol{i}', f'{item[0]}_vol{i}', f'{item[0]}_vol{i}'), f'{config.html_path}/{client_host}.html', 'a')

            elif item[0] == 'network':
                for i in range(1, 6):
                    if f'device{i}' in clients_data_parsed[client_host]['network']:
                        if clients_data_parsed[client_host]['network'][f'device{i}']['name'] != 'null':
                            # write data head
                            file.write_content_to_file(html_templates.DATA_HEAD.format(f'{item[0]}_device{i}'), f'{config.html_path}/{client_host}.html', 'a')

                            # write data records
                            file.write_content_to_file(html_templates.DATA_RECORD_DISK_NETWORK.format(client_host, item[0], f'device{i}', 'hour', client_host, item[0], f'device{i}', 'hour'), f'{config.html_path}/{client_host}.html', 'a')
                            file.write_content_to_file(html_templates.DATA_RECORD_DISK_NETWORK.format(client_host, item[0], f'device{i}', 'day', client_host, item[0], f'device{i}', 'day'), f'{config.html_path}/{client_host}.html', 'a')
                            if file.file_exists(f'{config.html_path}/{client_host}-{item[0]}-device{i}-year.png'):  # only display longterm graphs in html if they are created yet
                                file.write_content_to_file(html_templates.DATA_RECORD_DISK_NETWORK.format(client_host, item[0], f'device{i}', 'week', client_host, item[0], f'device{i}', 'week'), f'{config.html_path}/{client_host}.html', 'a')
                                file.write_content_to_file(html_templates.DATA_RECORD_DISK_NETWORK.format(client_host, item[0], f'device{i}', 'month', client_host, item[0], f'device{i}', 'month'), f'{config.html_path}/{client_host}.html', 'a')
                                file.write_content_to_file(html_templates.DATA_RECORD_DISK_NETWORK.format(client_host, item[0], f'device{i}', 'year', client_host, item[0], f'device{i}', 'year'), f'{config.html_path}/{client_host}.html', 'a')

                            # write data tail
                            file.write_content_to_file(html_templates.DATA_TAIL.format(f'{item[0]}_device{i}', f'{item[0]}_device{i}', f'{item[0]}_device{i}'), f'{config.html_path}/{client_host}.html', 'a')


        # write client tail
        file.write_content_to_file(html_templates.CLIENT_TAIL, f'{config.html_path}/{client_host}.html', 'a')

    print("Finished html.")