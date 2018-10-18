from subprocess import Popen, PIPE, STDOUT


# For creating a prometheus deployment to monitor the cluster (locally)
def cmd(command):
    p = Popen(command, stdin=PIPE, stdout=STDOUT, stderr=PIPE, shell=True)
    (_, _) = p.communicate()

cmd('kubectl create namespace monitoring')

cmd('kubectl create -f clusterRole.yaml')

cmd('kubectl create -f config-map.yaml -n monitoring')

cmd('kubectl create  -f prometheus-deployment.yaml --namespace=monitoring')

cmd('kubectl create -f prometheus-service.yaml --namespace=monitoring')
