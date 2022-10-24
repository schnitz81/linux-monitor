# linux-monitor

Monitoring tool for Linux systems that generates graphs and web pages dynamically.

## How-to

### Server

- Choose html_path and persistence_path in `config.py`. (Please note that a lot of writing will be done to the html_path folder, so consider pointing this to a ram disk, like the default setting and the persistent_path to a disk.)
- Enter at least one client in `clients.conf` file to collect monitoring data from.

Web server not included, so you need to provide your own to present the generated web pages and graphs. Simply point it to the same folder as the html_path in the config file. If you use the Kubernetes Helm chart, nginx will be installed automatically.
If running locally, no web server is needed since the rendered html files can be browsed directly.

#### Docker

Build it with the included Dockerfile or use the prebuilt image on Docker Hub:
https://hub.docker.com/r/schnitz81/linux-monitor

Make sure to use your own, updated client file. See the comments in the Dockerfile or on Docker Hub for run command. 

#### Kubernetes Helm chart

A Helm chart for easy installation in a Kubernetes cluster is included.

- Tweak your settings and select your clients in the `values.yaml` file.
- Installation example:
``` 
kubectl create ns linux-monitor
helm install linux-monitor . -n linux-monitor
```

### Client
- netcat, jq, bc and sysstat need to be installed in client machine.
- Run with init to create a config:<br>
 `./linux-monitor-client.sh init`
- Run it in a screen or from a start script.<br>
`./linux-monitor-client.sh`



 