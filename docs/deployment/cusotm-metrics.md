# Custom Metrics

This document outlines how to create a custom metrics on our k8s clusters.

---

There are a few things to be aware of before creating a custom metric:

* For any metric you create, you must have a service that can expose the metric.
* For any services exposing metrics, there must be a `ServiceMonitor` that targets this service.
* Metrics must be unique (I know this seems obvious but it can be a source of some ambiguous errors).

Okay, now we can look at creating our metric.

--- 

1. Think carefully about what it is you want to measure, and what the most appropriate way to measure it would be. Metrics can be one of the 4 types outlined on the prometheus website [here](https://prometheus.io/docs/concepts/metric_types/).

2. Give your metric and suitable name. Naming conventions for metrics can be found [here](https://prometheus.io/docs/practices/naming/). Don't worry to much about it sticking strictly to the convention, just as long as it's clear what you're measuring that is usually enough.

3. Now it's time to create your metric. When implementing things we want to keep the metrics as unintrusive as possible from existing code, so when possible you should follow the example in `aimmo-game`.

    * Below is an example of a custom metric from the `metrics.py` file. The first snippet contains the metrics iteself, while the second snippet contains the function with how we want to use that metrics.
    * This approach allows us to keep all our metrics is a single place so they're easy to find. Then you can simply import your metric where needed for use.

        ```python
        CUSTOM_BUCKET = [x/10 for x in range(10, 61)]
        GAME_TURN = Histogram('game_turn_time', 'Measures the time taken for the game to complete a single turn in seconds',
                        buckets=CUSTOM_BUCKET)
        ```

        ```python
        def GAME_TURN_TIME():
            """ Used for measuring the time it games for the game to complete a turn.
                This is measured using the Histogram datatype. """
            return GAME_TURN.time()
        ```

    * If you're creating a metric not in aimmo game or game creator, you will need to create a service for the pod you're working with. Then add the exporter so a service monitor can find them. Follow the [Prometheus client](https://github.com/prometheus/client_python#exporting) section for exporting if this is needed (aimmo-game should already have this present).

4. Now you should have a metric of your own, being exported to `/metrics` by default. You can check this by running the project locally in docker mode and going to that endpoint for the pod(s) you're interested in, if all is well you'll be greated by a wall of text and numbers (this is normal).

5. last step is the `ServiceMonitor`. Below is the config for the service monitor we use for the games.

    ```yaml
    apiVersion: monitoring.coreos.com/v1
    kind: ServiceMonitor
    metadata:
    name: aimmo-game
    namespace: default
    spec:
    endpoints:
      - targetPort: 5000
        interval: 15s
    selector:
        matchLabels:
        app: aimmo-game
    ```
    * Service monitors only have two required fields in their spec: `endpoints` & `selector`. These fields specify how to find your service(s), and what to look for once they've found them. So in this example above we can see in the `endpoints` section we're looking for all services with a target port of 5000, which all of our games have. Then, just to make sure we are definitely getting the games we specify that we are looking for services with a label `app` that has the value `aimmo-game`. There are many other options and ways to configure your service monitor but the above example is sufficient for most basic use cases.
    * Give your service monitor a suitable name so it is easy to find if you need to create a new one (games already have a service monitor).

6. You should now be able to see your custom metric in the Prometheus web UI. If not make sure your service monitor is configured correctly on the cluster and that you're custom metric is functioning properly.