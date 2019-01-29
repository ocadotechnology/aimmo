# Grafana Persistence
Here we will talk about how to connect our instances of Grafana to a database on Gcloud to ensure that data such as logins, permissions, and dashboards persist if the pod stops or is restarted for whatever reason.

## Setup

1. First, we need a database that Grafana will link to. To do this go to the [Google Cloud Console](https://console.cloud.google.com/home/dashboard?project=decent-digit-629) and in the menu go into the SQL section.

2. Look for an instance named `aimmo-monitoring`, if this does not exist for whatever reason, one will need to be created by following the steps after clicking the `create instance` button (you can create either a MySQL or PostgreSQL instance, for simplicity we recommend choosing PostgreSQL).

3. Now that you have an instance, go into it, then find the databases tab. You need 1 database per instance of Grafana (so one per cluster), the names of these databases are used later by the Grafana deployment so they are important. Recommended names are: `aimmo_monitoring_dev`, `aimmo_monitoring_staging`, `aimmo_monitoring_default`.

4. You should now have a database for the cluster you're working with. Next, you need a user, there should already be a user called `grafana` that you can use, if not click `create user` and go through the steps there. You need to make sure the user will have access to the instance you created if you had to create a new one.

5. Next, you should see 2 secrets on the cluster, one contains service account info, and the other has login details for Grafana. These are used in the `grafana-deployment.yaml`. If you need to recreate these secrects for whatever reason make sure the correct data is passed into this yaml. [Here](https://github.com/GoogleCloudPlatform/kubernetes-engine-samples/blob/master/cloudsql/postgres_deployment.yaml) is an example deployment which makes a good reference for this step.
