#!/bin/bash

#
# Client for the linux-monitor application.
# Run with init parameter to create the necessary configuration:
# $ ./linux-monitor-client.sh init
# No parameters for client start.
#

######################### main variables ##############################

CONFIGJSON="/etc/linux-monitor.conf"
VALUEJSONTMP="/run/.linux-monitor.tmp"
VALUEJSON="/run/.linux-monitor"
LISTENERPORT="12345"

######################### configuring #################################

function init ()
{
	# initialize config json file
	echo "{}" > $CONFIGJSON

	# add CPU category
	echo ; read -p "Add CPU load monitoring? " -n 1 -r
	if [[ $REPLY =~ ^[Yy]$ ]]; then
		echo $(jq '. + { "cpu": "1" }' <<<"$(cat $CONFIGJSON)") > $CONFIGJSON
	else
		echo $(jq '. + { "cpu": "0" }' <<<"$(cat $CONFIGJSON)") > $CONFIGJSON
	fi

	# add RAM category
	echo ; read -p "Add RAM usage monitoring? " -n 1 -r
	if [[ $REPLY =~ ^[Yy]$ ]]; then
		echo $(jq '. + { "ram": "1" }' <<<"$(cat $CONFIGJSON)") > $CONFIGJSON
	else
		echo $(jq '. + { "ram": "0" }' <<<"$(cat $CONFIGJSON)") > $CONFIGJSON
	fi

	# add swap category
	echo ; read -p "Add swap space monitoring? " -n 1 -r
	if [[ $REPLY =~ ^[Yy]$ ]]; then
		echo $(jq '. + { "swap": "1" }' <<<"$(cat $CONFIGJSON)") > $CONFIGJSON
	else
		echo $(jq '. + { "swap": "0" }' <<<"$(cat $CONFIGJSON)") > $CONFIGJSON
	fi

	# add disk category
	echo ; read -p "Add disk monitoring? " -n 1 -r
	if [[ $REPLY =~ ^[Yy]$ ]]; then
		for i in {1..5}; do
			echo ; read -p 'Volume path: ' volumepath

			if [ -z "$volumepath" ]; then
				break
			fi

			case $i in
				1)
					vol1=$volumepath
					echo $(jq --arg vol1 "$vol1" '. + { "disk": {"vol1": $vol1 }}' <<<$(cat $CONFIGJSON)) > $CONFIGJSON
					;;
				2)
					vol2=$volumepath
					echo $(jq --arg vol1 "$vol1" --arg vol2 "$vol2" '. + { "disk": {"vol1": $vol1, "vol2": $vol2 }}' <<<$(cat $CONFIGJSON)) > $CONFIGJSON
					;;
				3)
					vol3=$volumepath
					echo $(jq --arg vol1 "$vol1" --arg vol2 "$vol2" --arg vol3 "$vol3" '. + { "disk": {"vol1": $vol1, "vol2": $vol2, "vol3": $vol3 }}' <<<$(cat $CONFIGJSON)) > $CONFIGJSON
					;;
				4)
					vol4=$volumepath
					echo $(jq --arg vol1 "$vol1" --arg vol2 "$vol2" --arg vol3 "$vol3" --arg vol4 "$vol4" '. + { "disk": {"vol1": $vol1, "vol2": $vol2, "vol3": $vol3, "vol4": $vol4 }}' <<<$(cat $CONFIGJSON)) > $CONFIGJSON
					;;
				5)
					vol5=$volumepath
					echo $(jq --arg vol1 "$vol1" --arg vol2 "$vol2" --arg vol3 "$vol3" --arg vol4 "$vol4" --arg vol5 "$vol5" '. + { "disk": {"vol1": $vol1, "vol2": $vol2, "vol3": $vol3, "vol4": $vol4, "vol5": $vol5 }}' <<<$(cat $CONFIGJSON)) > $CONFIGJSON
					;;
			esac
			if [ "$i" -lt 5 ]; then
				echo ; read -p "Add another volume? " -n 1 -r
				if [[ ! $REPLY =~ ^[Yy]$ ]]; then
					break
				fi
			fi
		done
	else
		echo $(jq '. + { "disk": "0" }' <<<"$(cat $CONFIGJSON)") > $CONFIGJSON
	fi

	# add network devices
	noOfEthDevices=0
	echo ; read -p "Add network monitoring? " -n 1 -r
	if [[ $REPLY =~ ^[Yy]$ ]]; then
		mapfile -t arrEthDevices < <(ls /sys/class/net)  # get all eth devices

		firstCharInEthDevice="ew"

		for element in "${arrEthDevices[@]}"; do
			match="false"
			firstCharInElement=${element:0:1}
			for (( i=0; i<${#firstCharInEthDevice}; i++ )); do
				if [ "${firstCharInEthDevice:$i:1}" == "$firstCharInElement" ]; then
					match="true"
					break
				fi
			done
			if [ $match == "true" ]; then  # ask to add device if there is a matching first char
				echo ; echo "Add device:"
				echo -n "$element "
				read -p "Y/N?" -n 1 -r
				if [[ $REPLY =~ ^[Yy]$ ]]; then
					let "noOfEthDevices++"
					case $noOfEthDevices in
						1)
							device1=$element
							echo $(jq --arg device1 "$device1" '. + { "network": {"device1": $device1 }}' <<<$(cat $CONFIGJSON)) > $CONFIGJSON
							;;
						2)
							device2=$element
							echo $(jq --arg device1 "$device1" --arg device2 "$device2" '. + { "network": {"device1": $device1, "device2": $device2 }}' <<<$(cat $CONFIGJSON)) > $CONFIGJSON
							;;
						3)
							device3=$element
							echo $(jq --arg device1 "$device1" --arg device2 "$device2" --arg device3 "$device3" '. + { "network": {"device1": $device1, "device2": $device2, "device3": $device3 }}' <<<$(cat $CONFIGJSON)) > $CONFIGJSON
							;;
						4)
							device4=$element
							echo $(jq --arg device1 "$device1" --arg device2 "$device2" --arg device3 --arg device4 "$device4" '. + { "network": {"device1": $device1, "device2": $device2, "device3": $device3, "device4": $device4 }}' <<<$(cat $CONFIGJSON)) > $CONFIGJSON
							;;
						5)
							device5=$element
							echo $(jq --arg device1 "$device1" --arg device2 "$device2" --arg device3 --arg device4 "$device4" --arg device5 "$device5" '. + { "network": {"device1": $device1, "device2": $device2, "device3": $device3, "device4": $device4, "device5": $device5 }}' <<<$(cat $CONFIGJSON)) > $CONFIGJSON
							;;
					esac
					if [ "$noOfEthDevices" -gt 4 ]; then
						break
					fi
				fi
			fi
		done
	else
		echo $(jq '. + { "network": "0" }' <<<"$(cat $CONFIGJSON)") > $CONFIGJSON
	fi

	# add uptime category
	echo ; read -p "Add uptime monitoring? " -n 1 -r
	if [[ $REPLY =~ ^[Yy]$ ]]; then
		echo $(jq '. + { "uptime": "1" }' <<<"$(cat $CONFIGJSON)") > $CONFIGJSON
	else
		echo $(jq '. + { "uptime": "0" }' <<<"$(cat $CONFIGJSON)") > $CONFIGJSON
	fi

	echo ; echo "Configuration created."; exit 0
}


######################### measuring #################################

function cpu ()
{
	if [[ "$(cat $CONFIGJSON | jq -r .cpu)" != "null" ]] && [[ "$(cat $CONFIGJSON | jq -r .cpu)" != "0" ]]; then
		idleAvgLine=$(mpstat 10 1 | tail -n 1)
		idleAvg=$(echo ${idleAvgLine##* } | tr , .)
		cpuUsage=$(bc <<< "scale=2; 100-$idleAvg")
		echo $(jq --arg cpuUsage "$cpuUsage" '. + { "cpu": $cpuUsage }' <<<"$(cat $VALUEJSONTMP)") > $VALUEJSONTMP
		echo "CPU usage updated."
	else
		sleep 10
	fi
}

function mem ()
{
	if [[ "$(cat $CONFIGJSON | jq -r .ram)" != "null" ]] && [[ "$(cat $CONFIGJSON | jq -r .ram)" != "0" ]]; then
		memTotal=$(grep MemTotal /proc/meminfo | awk '{print $2}')
		memAvailable=$(grep MemAvailable /proc/meminfo | awk '{print $2}')
		memUsage=$((memTotal-memAvailable))
		echo $(jq --arg memTotal "$memTotal" --arg memUsage "$memUsage" \
			'. + { "ram": { "mem_total": $memTotal, "mem_usage": $memUsage }}' <<<$(cat $VALUEJSONTMP)) > $VALUEJSONTMP
		echo "RAM usage updated."
	fi
}

function swap ()
{
	if [[ "$(cat $CONFIGJSON | jq -r .swap)" != "null" ]] && [[ "$(cat $CONFIGJSON | jq -r .swap)" != "0" ]]; then
		if [ $(cat /proc/swaps | wc -l) -gt 1 ]; then
			swapTotal=$(tail -n 1 /proc/swaps | xargs | cut -d ' ' -f 3)
			swapUsage=$(tail -n 1 /proc/swaps | xargs | cut -d ' ' -f 4)
			echo $(jq --arg swapTotal "$swapTotal" --arg swapUsage "$swapUsage" \
				'. + { "swap": { "swap_total": $swapTotal, "swap_usage": $swapUsage }}' <<<$(cat $VALUEJSONTMP)) > $VALUEJSONTMP
			echo "Swap usage update."
		fi
	fi
}

function disk ()
{
	if [[ "$(cat $CONFIGJSON | jq -r .disk)" != "null" ]] && [[ "$(cat $CONFIGJSON | jq -r .disk)" != "0" ]]; then
		for i in {1..5}; do
			if [[ "$(cat $CONFIGJSON | jq -r .disk.vol$i)" != "null" ]] && [[ "$(cat $CONFIGJSON | jq -r .disk.vol$i)" != "0" ]]; then
				diskUsed=$(df -Pk $(cat $CONFIGJSON | jq -r .disk.vol$i) | sed 1d | awk '{ print $3 "\t" }' | xargs)
				diskAvailable=$(df -Pk $(cat $CONFIGJSON | jq -r .disk.vol$i) | sed 1d | awk '{ print $4 "\t" }' | xargs)
				diskTotal=$(df -Pk $(cat $CONFIGJSON | jq -r .disk.vol$i) | sed 1d | awk '{ print $2 "\t" }' | xargs)
				case $i in
					1)
						vol1Path=$(cat $CONFIGJSON | jq -r .disk.vol$i)
						vol1DiskUsed=$diskUsed
						vol1DiskTotal=$diskTotal
						echo $(jq --arg vol1Path "$vol1Path" --arg vol1DiskUsed "$vol1DiskUsed" --arg vol1DiskTotal "$vol1DiskTotal" '. + { "disk": { "vol1": { "path": $vol1Path, "disk_used": $vol1DiskUsed, "disk_total": $vol1DiskTotal }}}' <<<$(cat $VALUEJSONTMP)) > $VALUEJSONTMP
						;;
					2)
						vol2Path=$(cat $CONFIGJSON | jq -r .disk.vol$i)
						vol2DiskUsed=$diskUsed
						vol2DiskTotal=$diskTotal
						echo $(jq --arg vol1Path "$vol1Path" --arg vol1DiskUsed "$vol1DiskUsed" --arg vol1DiskTotal "$vol1DiskTotal" --arg vol2Path "$vol2Path" --arg vol2DiskUsed "$vol2DiskUsed" --arg vol2DiskTotal "$vol2DiskTotal" \
							'. + { "disk": { "vol1": { "path": $vol1Path, "disk_used": $vol1DiskUsed, "disk_total": $vol1DiskTotal}, "vol2": { "path": $vol2Path, "disk_used": $vol2DiskUsed, "disk_total": $vol2DiskTotal }}}' <<<$(cat $VALUEJSONTMP)) > $VALUEJSONTMP
						;;
					3)
						vol3Path=$(cat $CONFIGJSON | jq -r .disk.vol$i)
						vol3DiskUsed=$diskUsed
						vol3DiskTotal=$diskTotal
						echo $(jq --arg vol1Path "$vol1Path" --arg vol1DiskUsed "$vol1DiskUsed" --arg vol1DiskTotal "$vol1DiskTotal" --arg vol2Path "$vol2Path" --arg vol2DiskUsed "$vol2DiskUsed" --arg vol2DiskTotal "$vol2DiskTotal" --arg vol3Path "$vol3Path" --arg vol3DiskUsed "$vol3DiskUsed" --arg vol3DiskTotal "$vol3DiskTotal" \
							'. + { "disk": { "vol1": { "path": $vol1Path, "disk_used": $vol1DiskUsed, "disk_total": $vol1DiskTotal}, "vol2": { "path": $vol2Path, "disk_used": $vol2DiskUsed, "disk_total": $vol2DiskTotal }, "vol3": { "path": $vol3Path, "disk_used": $vol3DiskUsed, "disk_total": $vol3DiskTotal }}}' <<<$(cat $VALUEJSONTMP)) > $VALUEJSONTMP
						;;
					4)
						vol4Path=$(cat $CONFIGJSON | jq -r .disk.vol$i)
						vol4DiskUsed=$diskUsed
						vol4DiskTotal=$diskTotal
						echo $(jq --arg vol1Path "$vol1Path" --arg vol1DiskUsed "$vol1DiskUsed" --arg vol1DiskTotal "$vol1DiskTotal" --arg vol2Path "$vol2Path" --arg vol2DiskUsed "$vol2DiskUsed" --arg vol2DiskTotal "$vol2DiskTotal" --arg vol3Path "$vol3Path" --arg vol3DiskUsed "$vol3DiskUsed" --arg vol3DiskTotal "$vol3DiskTotal" --arg vol4Path "$vol4Path" --arg vol4DiskUsed "$vol4DiskUsed" --arg vol4DiskTotal "$vol4DiskTotal" \
							'. + { "disk": { "vol1": { "path": $vol1Path, "disk_used": $vol1DiskUsed, "disk_total": $vol1DiskTotal}, "vol2": { "path": $vol2Path, "disk_used": $vol2DiskUsed, "disk_total": $vol2DiskTotal }, "vol3": { "path": $vol3Path, "disk_used": $vol3DiskUsed, "disk_total": $vol3DiskTotal }, "vol4": { "path": $vol4Path, "disk_used": $vol4DiskUsed, "disk_total": $vol4DiskTotal }}}' <<<$(cat $VALUEJSONTMP)) > $VALUEJSONTMP
						;;
					5)
						vol5Path=$(cat $CONFIGJSON | jq -r .disk.vol$i)
						vol5DiskUsed=$diskUsed
						vol5DiskTotal=$diskTotal
						echo $(jq --arg vol1Path "$vol1Path" --arg vol1DiskUsed "$vol1DiskUsed" --arg vol1DiskTotal "$vol1DiskTotal" --arg vol2Path "$vol2Path" --arg vol2DiskUsed "$vol2DiskUsed" --arg vol2DiskTotal "$vol2DiskTotal" --arg vol3Path "$vol3Path" --arg vol3DiskUsed "$vol3DiskUsed" --arg vol3DiskTotal "$vol3DiskTotal" --arg vol4Path "$vol4Path" --arg vol4DiskUsed "$vol4DiskUsed" --arg vol4DiskTotal "$vol4DiskTotal" --arg vol5Path "$vol5Path" --arg vol5DiskUsed "$vol5DiskUsed" --arg vol5DiskTotal "$vol5DiskTotal" \
							'. + { "disk": { "vol1": { "path": $vol1Path, "disk_used": $vol1DiskUsed, "disk_total": $vol1DiskTotal}, "vol2": { "path": $vol2Path, "disk_used": $vol2DiskUsed, "disk_total": $vol2DiskTotal }, "vol3": { "path": $vol3Path, "disk_used": $vol3DiskUsed, "disk_total": $vol3DiskTotal }, "vol4": { "path": $vol4Path, "disk_used": $vol4DiskUsed, "disk_total": $vol4DiskTotal }, "vol5": { "path": $vol5Path, "disk_used": $vol5DiskUsed, "disk_total": $vol5DiskTotal }}}' <<<$(cat $VALUEJSONTMP)) > $VALUEJSONTMP
						;;
				esac

			fi
		done
		echo "Disk volumes usage updated."
	fi
}

function network ()
{
	if [[ "$(cat $CONFIGJSON | jq -r .network)" != "null" ]] && [[ "$(cat $CONFIGJSON | jq -r .network)" != "0" ]]; then
		for i in {1..5}; do
			if [[ "$(cat $CONFIGJSON | jq -r .network.device$i)" != "null" ]] && [[ "$(cat $CONFIGJSON | jq -r .network.device$i)" != "0" ]]; then
				case $i in
					1)
						device1=$(cat $CONFIGJSON | jq -r .network.device$i)
						device1RxBytes=$(cat /sys/class/net/$device1/statistics/rx_bytes)
						device1TxBytes=$(cat /sys/class/net/$device1/statistics/tx_bytes)
						echo $(jq --arg device1 "$device1" --arg device1RxBytes "$device1RxBytes" --arg device1TxBytes "$device1TxBytes" \
							'. + { "network": { "device1": { "name": $device1, "rx_bytes": $device1RxBytes, "tx_bytes": $device1TxBytes }}}' <<<$(cat $VALUEJSONTMP)) > $VALUEJSONTMP
						;;
					2)
						device2=$(cat $CONFIGJSON | jq -r .network.device$i)
						device2RxBytes=$(cat /sys/class/net/$device2/statistics/rx_bytes)
						device2TxBytes=$(cat /sys/class/net/$device2/statistics/tx_bytes)
						echo $(jq --arg device1 "$device1" --arg device1RxBytes "$device1RxBytes" --arg device1TxBytes "$device1TxBytes" \
							--arg device2 "$device2" --arg device2RxBytes "$device2RxBytes" --arg device2TxBytes "$device2TxBytes" \
							'. + { "network": { "device1": { "name": $device1, "rx_bytes": $device1RxBytes, "tx_bytes": $device1TxBytes }, "device2": { "name": $device2, "rx_bytes": $device2RxBytes, "tx_bytes": $device2TxBytes } }}' <<<$(cat $VALUEJSONTMP)) > $VALUEJSONTMP
						;;
					3)
						device3=$(cat $CONFIGJSON | jq -r .network.device$i)
						device3RxBytes=$(cat /sys/class/net/$device3/statistics/rx_bytes)
						device3TxBytes=$(cat /sys/class/net/$device3/statistics/tx_bytes)
						echo $(jq --arg device1 "$device1" --arg device1RxBytes "$device1RxBytes" --arg device1TxBytes "$device1TxBytes" \
							--arg device2 "$device2" --arg device2RxBytes "$device2RxBytes" --arg device2TxBytes "$device2TxBytes" \
							--arg device3 "$device3" --arg device3RxBytes "$device3RxBytes" --arg device3TxBytes "$device3TxBytes" \
							'. + { "network": { "device1": { "name": $device1, "rx_bytes": $device1RxBytes, "tx_bytes": $device1TxBytes }, "device2": { "name": $device2, "rx_bytes": $device2RxBytes, "tx_bytes": $device2TxBytes }, "device3": { "name": $device3, "rx_bytes": $device3RxBytes, "tx_bytes": $device3TxBytes } }}' <<<$(cat $VALUEJSONTMP)) > $VALUEJSONTMP
						;;
					4)
						device4=$(cat $CONFIGJSON | jq -r .network.device$i)
						device4RxBytes=$(cat /sys/class/net/$device4/statistics/rx_bytes)
						device4TxBytes=$(cat /sys/class/net/$device4/statistics/tx_bytes)
						echo $(jq --arg device1 "$device1" --arg device1RxBytes "$device1RxBytes" --arg device1TxBytes "$device1TxBytes" \
							--arg device2 "$device2" --arg device2RxBytes "$device2RxBytes" --arg device2TxBytes "$device2TxBytes" \
							--arg device3 "$device3" --arg device3RxBytes "$device3RxBytes" --arg device3TxBytes "$device3TxBytes" \
							--arg device4 "$device4" --arg device4RxBytes "$device4RxBytes" --arg device4TxBytes "$device4TxBytes" \
							'. + { "network": { "device1": { "name": $device1, "rx_bytes": $device1RxBytes, "tx_bytes": $device1TxBytes }, "device2": { "name": $device2, "rx_bytes": $device2RxBytes, "tx_bytes": $device2TxBytes }, "device3": { "name": $device3, "rx_bytes": $device3RxBytes, "tx_bytes": $device3TxBytes }, "device4": { "name": $device4, "rx_bytes": $device4RxBytes, "tx_bytes": $device4TxBytes } }}' <<<$(cat $VALUEJSONTMP)) > $VALUEJSONTMP
						;;
					5)
						device5=$(cat $CONFIGJSON | jq -r .network.device$i)
						device5RxBytes=$(cat /sys/class/net/$device5/statistics/rx_bytes)
						device5TxBytes=$(cat /sys/class/net/$device5/statistics/tx_bytes)
						echo $(jq --arg device1 "$device1" --arg device1RxBytes "$device1RxBytes" --arg device1TxBytes "$device1TxBytes" \
							--arg device2 "$device2" --arg device2RxBytes "$device2RxBytes" --arg device2TxBytes "$device2TxBytes" \
							--arg device3 "$device3" --arg device3RxBytes "$device3RxBytes" --arg device3TxBytes "$device3TxBytes" \
							--arg device4 "$device4" --arg device4RxBytes "$device4RxBytes" --arg device4TxBytes "$device4TxBytes" \
							--arg device5 "$device5" --arg device5RxBytes "$device5RxBytes" --arg device5TxBytes "$device5TxBytes" \
							'. + { "network": { "device1": { "name": $device1, "rx_bytes": $device1RxBytes, "tx_bytes": $device1TxBytes }, "device2": { "name": $device2, "rx_bytes": $device2RxBytes, "tx_bytes": $device2TxBytes }, "device3": { "name": $device3, "rx_bytes": $device3RxBytes, "tx_bytes": $device3TxBytes }, "device4": { "name": $device4, "rx_bytes": $device4RxBytes, "tx_bytes": $device4TxBytes }, "device5": { "name": $device5, "rx_bytes": $device5RxBytes, "tx_bytes": $device5TxBytes } }}' <<<$(cat $VALUEJSONTMP)) > $VALUEJSONTMP
						;;
				esac
			fi
		done
		echo "Network usage updated."
	fi
}

function uptime ()
{
	if [[ "$(cat $CONFIGJSON | jq -r .uptime)" != "null" ]] && [[ "$(cat $CONFIGJSON | jq -r .uptime)" != "0" ]]; then
		uptimeEpoch=$(cut -d '.' -f 1 /proc/uptime)
		echo $(jq --arg uptimeEpoch "$uptimeEpoch" '. + { "uptime": $uptimeEpoch }' <<<"$(cat $VALUEJSONTMP)") > $VALUEJSONTMP
		echo "Uptime updated."
	fi
}

############################ TCP server ########################################

function listener ()
{
		echo "$(base64 $VALUEJSON)" | nc -w 10 -l -p $LISTENERPORT >/dev/null 2>&1
}

################################################################################

# run as root
if [ $(whoami) != "root" ]; then
	echo "Please run as root"
	exit
fi

# check if jq is installed
if [ -z "$(which jq)" ] ; then
	echo "jq not found. Please install jq package."
	exit 1
fi

# check if netcat is installed
if [ -z "$(which nc)" ] ; then
	echo "nc not found. Please install netcat."
	exit 1
fi

# check if bc is installed
if [ -z "$(which bc)" ] ; then
	echo "bc not found. Please install bc package."
	exit 1
fi

# check if sysstat is installed
if [ -z "$(which mpstat)" ] ; then
	echo "mpstat not found. Please install sysstat package."
	exit 1
fi

# check if init parameter is started - run init procedure
if [ "$1" == "init" ]; then
	init
fi

# check if conf file exists
if [ ! -f $CONFIGJSON ]; then
	echo "Configuration file not found. Please run init first."; exit 0
fi


# main loop
while true; do

	# initialize value json tmp file if it is not created yet or is empty
	if [ ! -f "$VALUEJSONTMP" ] || ! [[ "$(cat $VALUEJSONTMP)" =~ [^a-zA-Z ]]; then
		echo "{}" > $VALUEJSONTMP
	fi
	if [ ! -f "$VALUEJSON" ]; then
		touch $VALUEJSON
	fi

	# run listener
	set -m
	listener &
	set +m
	trap "kill -- -$!" EXIT

	cpu &

	(mem; swap; disk; network; uptime) &
	echo $(jobs -p)
	echo "$(jobs -p | head -n 2 | tail -n 1) $(jobs -p | head -n 3 | tail -n 1)"

	wait
	cp $VALUEJSONTMP $VALUEJSON

done
