# linux-monitor

Monitoring tool for Linux systems that generates graphs and web pages dynamically.

Server side.

## Usage

- Enter the clients' hostname and IP address in values.yaml.<br>
- Enter a storageClassName if some other than the default storageClass will be used.<br>
<br>
- Create new namespace:<br>
`kubectl create ns linux-monitor`<br>
<br>
- Deploy Helm chart:<br>
`helm install linux-monitor -f values.yaml . -n linux-monitor`<br>
<br>
- Delete Helm chart:<br>
`helm del linux-monitor -n linux-monitor`<br>

