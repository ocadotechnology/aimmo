# Monitoring

This document outlines the process we use to collect metrics from our clusters on Google cloud engine and how to restart the relavent pods in the event they break in some way.

*Note: the monitoring setup is a one time event that should only be done again in the event of failure or breakage*

## Monitoring with Prometheus

---

Everything on our cluster is monitored via [Prometheus](https://prometheus.io/), and more specifically the [kube-prometheus](https://github.com/coreos/prometheus-operator/tree/master/contrib/kube-prometheus) setup used for kubernetes clusters.

### Prometheus workflow

Here is the offical workflow for [Prometheus](https://prometheus.io/): ![Prometheus workflow & relationship diagram](prometheus4k8s.png) *[image source](https://itnext.io/kubernetes-monitoring-with-prometheus-in-15-minutes-8e54d1de2e13)*

In the above picture there are a number of different components. In short, [Prometheus](https://prometheus.io/) uses service monitors to scrape metrics from all services on the cluster and holds them for a set amount of time. The operator is build on a framework used to package and deploy applications to kubernetes clusters, more information on operators can be found [here](https://coreos.com/operators/), but it's not required to understand how [Prometheus](https://prometheus.io/) interacts with the cluster.

This gives us all we need all we need to collect data and store it, but not a good way of making use of any of that data. That is handled via various Data vizualisation tools.

### Data Visualisation

There are a number of ways to view the data [Prometheus](https://prometheus.io/) collects, the ones we make use of are: The Prometheus web UI, and [Grafana](https://grafana.com/). The Prometheus web UI is a simple tool that allows you to create queries on various metrics, view results in simple graphs, and view things like data targets (which is where all your data comes from), rules, and alerts (alerts will be explained later).

[Grafana](https://grafana.com/) is a tool that allows to create dashboards and organise our data, and gives a much wider range of options when it comes to creating graphs and charts. it uses the same query language as the Prometheus web UI for collecting data, making it much simpler to switch between the web UI and Grafana.

# Setup

In the `monitoring` folder in the AI:MMO root directory (will be moved to app-engine in future), you will find a sub-folder called `manifests`. This folder contains all the configuration required to get [Prometheus](https://prometheus.io/) and [Grafana](https://grafana.com/) onto our clusters, but they will need to be exposed manually.

1. To do this, first find thet file named `prometheus-prometheus.yaml` and change the following line:

```yaml
  externalUrl: "https://{CLUSTER}-aimmo.codeforlife.education/prometheus"
```

by replacing the word `{CLUSTER}` with either dev/staging/default depending on which cluster you are applying the manifests to.

2. Next we need to repeat this step for the `alertmanager-alertmanager.yaml` file, again finding the the line:

```yaml
  externalUrl: "https://{CLUSTER}-aimmo.codeforlife.education/alertmanager"
```

and replacing `{CLUSTER}` with either dev/staging/default depending on which cluster you're workking with.

3. Now we need to look for files named: `monitoring-ingress.yaml` & `grafana-ingress.yaml`. In both files there will be a line that looks like this:

```yaml
  - host: "https://{CLUSTER}-aimmo.codeforlife.education"
```

Again you need to replace `{CLUSTER}` with either dev/staging/default depending on which cluster you're working on.

4. After that, look for the `grafana-ini-configmap.yaml` file, this contains the the main config file used to setup [Grafana](https://grafana.com/). inside the `[server]` header, look for the lines:

```ini
domain = {CLUSTER}-aimmo.codeforlife.education
...
root_url = https://{CLUSTER}-aimmo.codeforlife.education/grafana/
```

and once again replace `{CLUSTER}` with either dev/staging/default.

5. Next, you need to go onto the Kubernetes Engine section of our [Google cloud console](https://console.cloud.google.com) dashboard, then go into services and look for the `aimmo-ingress` for the cluster you're working. It should be near to, or at the top of the list of services.

Click on the ingress to open up it's details, then click "EDIT". You should see something like this:

```yaml
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  annotations:
    kubernetes.io/ingress.class: nginx
    kubernetes.io/ingress.global-static-ip-name: dev-aimmo-ingress
    ...
```

Now add this line into the annotations section:

```yaml
nginx.org/mergeable-ingress-type: master
```

This is needed because we make use of multiple ingress files but you are only allowed a single ingress per host. For more information see the following example [here](https://github.com/nginxinc/kubernetes-ingress/tree/master/examples/mergeable-ingress-types).

6. Finally, should be able to apply these manifests to the cluster you're working with.

to do this, run `kubectl create -f manifests/ || true`, if prometheus does not exist on that cluster at all. If the manifests have already been applied before, use: `kubectl apply -f manifests/ || true` and this will update the existing manifests and reset all the relavent components. You can use `kubectl delete -f manifests/ || true` if you need to remove our monitoring for whatever reason (at present this will also destroy all data).

*Note: kubectl needs to be configured to work with the GCloud cluster for this method to work*

## Potential setup issues

Below are some issues you may encounter when setting up [Prometheus](https://prometheus.io/) and [Grafana](https://grafana.com/) on any of the clusters.

### Grafana looks a bit empty

If when you go to `https://CLUSTER_URL/grafana` all you see is a mostly blank page containing some text, this means the ingress isn't configured quite right so it's not exposing all the styles. Below are some examples for working configs for the `grafana-ingress.yaml`

```yaml
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: grafana-ingress
  namespace: monitoring
  annotations:
    kubernetes.io/ingress.class: nginx
    nginx.ingress.kubernetes.io/rewrite-target: /$1
    nginx.org/mergeable-ingress-type: minion
spec:
  rules:
  - host: staging-aimmo.codeforlife.education
    http:
      paths:
      - backend:
          serviceName: grafana
          servicePort: 3000
        path: /grafana/?(.*)
```

```yaml
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: grafana-ingress
  namespace: monitoring
  annotations:
    kubernetes.io/ingress.class: nginx
    nginx.ingress.kubernetes.io/rewrite-target: /
    nginx.org/mergeable-ingress-type: minion
spec:
  rules:
  - host: staging-aimmo.codeforlife.education
    http:
      paths:
      - backend:
          serviceName: grafana
          servicePort: 3000
        path: /grafana
```