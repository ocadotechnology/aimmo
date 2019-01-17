# Monitoring

This document outlines the process we use to collect metrics from our clusters on Google cloud engine and how to restart the relavent pods in the event they break in some way.

*Note: the monitoring setup is a one time event that should only be done again in the event of failure or breakage*

## Monitoring with Prometheus

---

Everything on our cluster is monitored via [Prometheus](https://prometheus.io/), and more specifically the [kube-prometheus](https://github.com/coreos/prometheus-operator/tree/master/contrib/kube-prometheus) setup used to monitor Kubernetes clusters.