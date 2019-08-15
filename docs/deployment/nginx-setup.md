# NGINX Controller Ingress Setup

**Note: This should only be done once only. The only time when a new setup might be required is when you reset the cluster to a fresh state or delete the relevant pods, services & deployments.**

--- 


In order to deploy our ingress correctly with a specific nginx controller used in google cloud platform, we need to create several services. All of these up to date instructions can be found [**here**](https://github.com/kubernetes/ingress-nginx/blob/master/deploy/README.md). 

For the sake of correct version control, we have saved the yaml files at the time of setup in the repository `ocadotechnology/codeforlife-deploy-appengine` at the path `./clusters_setup/ingress_nginx`.

To set up from scratch do the following:
* Install gcloud locally. This is usually done by the following command: `pip install google-cloud`. At the time of writing the version is `0.32.0` and Google Cloud SDK of `189.0.0`.
* Set the current project for this workspace by typing: `gcloud config set project decent-digit-629`.
* Authenticate accordingly. You can read up on this [**here**](https://cloud.google.com/appengine/docs/standard/python/oauth/). Usually the following should work: `gcloud auth login`. This will open a web browser and will ask you to authenticate and give permissions to the google account. You should then (or only) run `gcloud auth application-default login` which will create the kubeconfig required for `kubectl` to work. 
* Get credentials to the appropriate cluster you want to work on by doing the following command: `gcloud container clusters get-credentials [dev/staging/default] --zone europe-west1-b`
* `kubectl apply -f` should now be used on the following files (see path above to find these files):
    * `namespace.yaml`, `default-backend-service.yaml`, `default-backend-deployment.yaml`, `configmap.yaml`, `tcp-services-configmap.yaml`, `udp-services-configmap.yaml`. 
* Now install no RBAC roles by doing the same on `without-rbac.yaml`.
* And finally GCE specific settings and patches:
    * Run `kubectl patch deployment -n ingress-nginx nginx-ingress-controller --type='json' --patch="$(curl https://raw.githubusercontent.com/kubernetes/ingress-nginx/master/deploy/publish-service-patch.yaml)"`.
    * `kubectl apply -f` on `service.yaml` and `patch-service-without-rbac.yaml`

***
# Reserving a static external IP address for a cluster

The load balancer IP needs to be static in order to be resolved to a single DNS address. The whole setup process won't have to be done again but for reference:
* Go to **VPC Networks -> External IP addresses ** in the Google Cloud Platform UI and reserve a _**static**_ IP address with the name `[env]-aimmo-ingress`
* In your appengine project, open the [`ingress.yaml`](https://github.com/ocadotechnology/codeforlife-deploy-appengine/blob/master/clusters_setup/ingress.yaml) file and make sure that the following complies:
    * In metadata:annotations `kubernetes.io/ingress.global-static-ip-name: [env]-aimmo-ingress` is set.
    * Ensure the spec:host entry is made for this domain in the ingress. For example `- host: default-aimmo.codeforlife.education`
* Make a ANAME record in the DNS server to attatch it to that IP address that was reserved. Make sure this domain is `[env]-aimmo.codeforlife.education`.

***
# Securing the cluster with SSL.

When settings the above DNS, you should generate/obtain appropriate CA, cert and key files. To now secure your domain you should:
* In file [`ingress.yaml`](https://github.com/ocadotechnology/codeforlife-deploy-appengine/blob/master/clusters_setup/ingress.yaml) on the appengine project, the section _**spec:rules**_ should contain:
```  
tls:
  - hosts:
    - [env]-aimmo.codeforlife.education
    secretName: ssl-cert-secret
```
* In your terminal, go to the directory that contains the above mentioned files and use the following to generate the secret: `kubectl create secret tls foo-secret --key=/tmp/tls.key --cert=/tmp/tls.crt`. This will require correct authentication which is described above.
* The downtime between deleting the old `ssl-cert-secret` on a cluster and creating a new one will hang the game creator as it will not receive information since a certificate authority issue will occur. The solution for this is to delete the game creator **pod** which will reinstantiate all the games and workers from scratch.
