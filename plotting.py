import config
import database
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from dateutil import parser
from matplotlib import style
from matplotlib import ticker
import datetime
import bitmath


style.use('fivethirtyeight')

intervals = {'hour': {'timestring': 'hours', 'value': 1},
             'day': {'timestring': 'hours', 'value': 24},
             'week': {'timestring': 'weeks', 'value': 1},
             'month': {'timestring': 'days', 'value': 30},
             'year': {'timestring': 'weeks', 'value': 52}}


def plot_single_graph(conn, client, table, interval):

    print(f"Plotting {client} {table} {interval} graph.")

    column = database.get_value_column_name(conn, table, 2)
    data = database.read_data(conn, table)
    now = datetime.datetime.now()

    dates = []
    values = []

    maxvalue = data[0][1]

    if data[-1][2] is not None:  # if last row contains valid data

        for row in data:
            if parser.parse(row[0]) > now - datetime.timedelta(**{intervals[interval]['timestring']: intervals[interval]['value']}):

                # put gap in graph if over a minute has passed
                if len(dates) > 1:
                    if parser.parse(row[0]) > dates[-1] + datetime.timedelta(minutes=1):
                        dates.append(dates[-1] + datetime.timedelta(seconds=1))
                        values.append(float('NaN'))

                dates.append(parser.parse(row[0]))
                values.append(row[2])  # use col 2 as gauge for all single value graphs

        # set font size for scales
        font = {'size': 10, 'family': 'monospace'}
        plt.rc('font', **font)

        plt.figure(num=None, figsize=(13, 10), dpi=100, facecolor='w')

        plt.gcf().autofmt_xdate()

        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))

        plt.plot_date(dates, values, '-', color='#00EE00')  # graph color

        # set title text
        plt.title(interval, pad=18, fontsize=32, color='w')

        # rotate x-axis labels
        plt.xticks(rotation=45, color='w')

        # set y-axis label text color
        plt.yticks(color='w')

        # disable exponent formatting
        plt.ticklabel_format(useOffset=False, axis='y')

        # get min, max and avg values
        if table != 'uptime':
            min_value = database.get_minimum_value(conn, column, table, interval)
            max_value = database.get_maximum_value(conn, column, table, interval)
            avg_value = database.get_average_value(conn, column, table, interval)
            current_value = database.get_current_value(conn, column, table)
        else:
            min_value = "{:.2f}".format(database.get_minimum_value_float(conn, column, table, interval))
            max_value = "{:.2f}".format(database.get_maximum_value_float(conn, column, table, interval))
            avg_value = "{:.2f}".format(database.get_average_value_float(conn, column, table, interval))
            current_value = "{:.2f}".format(database.get_current_value_float(conn, column, table))

        # set unit for ram and swap
        if table == 'ram' or table == 'swap':
            min_value = bitmath.kB(min_value).best_prefix()
            max_value = bitmath.kB(max_value).best_prefix()
            avg_value = bitmath.kB(avg_value).best_prefix()
            current_value = bitmath.kB(current_value).best_prefix()

        # place text annotations
        with bitmath.format(fmt_str="{value:.3f} {unit}"):
            annotationstr = '\n\n'.join((
                f' min:  {min_value}',
                f' max:  {max_value}',
                f' avg:  {avg_value}',
                f' last: {current_value}'
            ))

        plt.annotate(
            annotationstr,
            xy=(0.85, 1.15),
            xytext=(0, 0),
            va='top',
            xycoords='axes fraction',
            textcoords='offset points',
            size=8.0, family='monospace',
            color='w'
        )

        yaxislabel = None

        # set ylabel
        if table == 'cpu':
            yaxislabel = '%'
        elif table == 'uptime':
            yaxislabel = 'days'

        if yaxislabel is not None:
            plt.annotate(
                yaxislabel,
                xy=(-0.03, 1.06),
                xytext=(0, 0),
                va='top',
                xycoords='axes fraction',
                textcoords='offset points',
                size=15.0, family='Sans',
                color='w'
            )

        ax = plt.gca()

        if table != 'cpu' and table != 'uptime':
            mkfunc = lambda x, pos: '%1.1fG' % (x * 1e-6) if x >= 1e6 else '%1.1fM' % (x * 1e-3) if x >= 1e3 else '%1.1fK' % (x * 1e-1) if x >= 1e1 else '%1.1f' % x
            mkformatter = ticker.FuncFormatter(mkfunc)
            ax.yaxis.set_major_formatter(mkformatter)

        ax.set_facecolor('#000000')

        # set max value on y axis
        if maxvalue != 0:
            ax.set_ylim([0, maxvalue])

        # set graph edge line
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_linewidth(0.5)
        ax.spines['left'].set_linewidth(False)

        plt.savefig(f"{config.html_path}/{client}-{table}-{interval}.png", facecolor='black')

        plt.close()


def plot_multi_graph(conn, client, table, interval):

    print(f"Plotting {client} {table} {interval} graphs.")

    for deviceNbr in range(2, 12, 2):  # every other col in DB (5 double values)

        column = database.get_value_column_name(conn, table, deviceNbr)
        data = database.read_data(conn, table)
        now = datetime.datetime.now()
        devicelabel = ''
        deviceenum = ''

        if table == 'disk':
            devicelabel = database.get_device_label(conn, 'disk_path', deviceNbr)
            deviceenum = database.get_device_enumeration(conn, table, deviceNbr)
        elif table == 'network':
            devicelabel = database.get_device_label(conn, 'network_name', deviceNbr)
            deviceenum = database.get_device_enumeration(conn, table, deviceNbr)

        dates = []
        values = []
        rxvalues = []
        txvalues = []
        prevrxvalue = 0
        prevtxvalue = 0

        if data[-1][deviceNbr] is not None:  # if last row contains valid data
            for row in data:

                # limit to last period
                if parser.parse(row[0]) > now - datetime.timedelta(**{intervals[interval]['timestring']: intervals[interval]['value']}):

                    # always put gap in graph if over a minute has passed
                    if table != 'network' and len(dates) > 0:
                        if parser.parse(row[0]) > dates[-1] + datetime.timedelta(minutes=1):
                            dates.append(dates[-1] + datetime.timedelta(seconds=1))
                            values.append(float('NaN'))

                    # graph data generating section except network
                    if table != 'network':
                        dates.append(parser.parse(row[0]))
                        values.append(row[deviceNbr])  # use col 2 as gauge for all single value graphs

                    # network graph data generating section
                    elif table == 'network':
                        if len(dates) == 0:  # put first date record
                            dates.append(parser.parse(row[0]))
                            rxvalues.append(float('NaN'))
                            txvalues.append(float('NaN'))

                        else:
                            # always put gap in graph if over two cycletimes have passed
                            if parser.parse(row[0]) > dates[-1] + datetime.timedelta(float(config.scancycletime)+float(config.scancycletime)):
                                dates.append(dates[-1] + datetime.timedelta(seconds=1))
                                rxvalues.append(float('NaN'))
                                txvalues.append(float('NaN'))

                            # normal cycle gap iteration
                            if parser.parse(row[0]) > dates[-1] + datetime.timedelta(seconds=(float(config.scancycletime) - 1)) and parser.parse(row[0]) < dates[-1] + datetime.timedelta(seconds=(float(config.scancycletime) + 1)):
                                dates.append(parser.parse(row[0]))
                                rxvalues.append((row[deviceNbr-1]-prevrxvalue)/float(config.scancycletime))
                                txvalues.append((row[deviceNbr]-prevtxvalue)/float(config.scancycletime))

                            # place NaN iteration if timing requirements for bitrate calculation failed
                            elif parser.parse(row[0]) > dates[-1]:
                                dates.append(parser.parse(row[0]))
                                rxvalues.append(float('NaN'))
                                txvalues.append(float('NaN'))

                        # store rx and tx values for next iteration
                        prevrxvalue = row[deviceNbr-1]
                        prevtxvalue = row[deviceNbr]

            # set font size for scales
            font = {'size': 10, 'family': 'monospace'}
            plt.rc('font', **font)

            plt.figure(num=None, figsize=(13, 10), dpi=100, facecolor='w')

            plt.gcf().autofmt_xdate()

            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))

            if table != 'network':
                plt.plot_date(dates, values, '-', color='#00EE00')  # graph plotter
            else:
                plt.plot_date(dates, rxvalues, '-', color='#00CC00')  # rx graph
                plt.plot_date(dates, txvalues, '-', color='#CC0000')  # tx graph

            # set title text
            if table == 'disk' or table == 'network':
                plt.title(f"{devicelabel} - {interval}", pad=18, fontsize=32, color='w')
            else:
                plt.title(interval, pad=18, fontsize=32, color='w')

            # rotate x-axis labels
            plt.xticks(rotation=45, color='w')

            # set y-axis label text color
            plt.yticks(color='w')

            # disable exponent formatting
            plt.ticklabel_format(useOffset=False, axis='y')

            # get min, max and avg values
            min_value = database.get_minimum_value(conn, column, table, interval)
            max_value = database.get_maximum_value(conn, column, table, interval)
            avg_value = database.get_average_value(conn, column, table, interval)
            current_value = database.get_current_value(conn, column, table)

            # set unit for disk
            if table == 'disk':
                min_value = bitmath.kB(min_value).best_prefix()
                max_value = bitmath.kB(max_value).best_prefix()
                avg_value = bitmath.kB(avg_value).best_prefix()
                current_value = bitmath.kB(current_value).best_prefix()

            # place text annotations
            if table != 'network':
                with bitmath.format(fmt_str="{value:.3f} {unit}"):
                    annotationstr = '\n\n'.join((
                        f' min:  {min_value}',
                        f' max:  {max_value}',
                        f' avg:  {avg_value}',
                        f' last: {current_value}'
                    ))

                plt.annotate(
                    annotationstr,
                    xy=(0.85, 1.15),
                    xytext=(0, 0),
                    va='top',
                    xycoords='axes fraction',
                    textcoords='offset points',
                    size=8.0, family='monospace',
                    color='w'
                )

            yaxislabel = ''

            # set ylabel
            if table == 'network':
                yaxislabel = '/sec'
            plt.annotate(
                yaxislabel,
                xy=(-0.03, 1.06),
                xytext=(0, 0),
                va='top',
                xycoords='axes fraction',
                textcoords='offset points',
                size=15.0, family='Sans',
                color='w'
            )

            # get y axis max value
            if table != 'network':
                maxvalue = data[-1][deviceNbr-1]  # get max value for the current device from the last line in table
            else:
                rxmaxvalue = 0
                txmaxvalue = 0
                maxvaluelist = []
                for val in rxvalues:
                    if isinstance(val, (int, float)) and val == val:  # is number and not NaN
                        maxvaluelist.append(val)
                        rxmaxvalue = max(maxvaluelist)
                maxvaluelist = []
                for val in txvalues:
                    if isinstance(val, (int, float)) and val == val:  # is number and not NaN
                        maxvaluelist.append(val)
                        txmaxvalue = max(maxvaluelist)
                if rxmaxvalue > txmaxvalue:
                    maxvalue = rxmaxvalue
                else:
                    maxvalue = txmaxvalue

            # annotate y axis max size
            totallabel = ''
            with bitmath.format(fmt_str="{value:.3f} {unit}"):
                if table == 'disk':
                    totallabel = 'Total size: ' + str(bitmath.kB(maxvalue).best_prefix())
                plt.annotate(
                    totallabel,
                    xy=(-0.05, 1.1),
                    xytext=(0, 0),
                    va='top',
                    xycoords='axes fraction',
                    textcoords='offset points',
                    size=8.0, family='Sans',
                    color='w'
                )

            ax = plt.gca()

            if table != 'cpu' and table != 'uptime':
                if table != 'network':
                    mkfunc = lambda x, pos: '%1.1fG' % (x * 1e-6) if x >= 1e6 else '%1.1fM' % (x * 1e-3) if x >= 1e3 else '%1.1fK' % (x * 1e-1) if x >= 1e1 else '%1.1f' % x
                else:
                    mkfunc = lambda x, pos: '%1.1fGB' % (x * 1e-9) if x >= 1e9 else '%1.1fMB' % (x * 1e-6) if x >= 1e6 else '%1.1fkB' % (x * 1e-3) if x >= 1e3 else '%1.1f' % x
                mkformatter = ticker.FuncFormatter(mkfunc)
                ax.yaxis.set_major_formatter(mkformatter)

            ax.set_facecolor('#000000')

            # set max value on y axis
            if maxvalue != 0:
                ax.set_ylim([0, maxvalue])

            # set graph edge line
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['bottom'].set_linewidth(0.5)
            ax.spines['left'].set_linewidth(False)

            plt.savefig(f"{config.html_path}/{client}-{table}-{deviceenum}-{interval}.png", facecolor='black')

            plt.close()
