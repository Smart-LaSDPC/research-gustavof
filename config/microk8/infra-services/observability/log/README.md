microk8s enable fluentd
microk8s enable community fluentd
microk8s disable fluentd

[text](https://www.digitalocean.com/community/tutorials/how-to-set-up-an-elasticsearch-fluentd-and-kibana-efk-logging-stack-on-kubernetes)

Kibana UI
- discover
- create index pattern in kibana
- logstash-*
- @timestamp
- back to discover
- search kubernetes.pod_name:ingress-nginx
- include message field
