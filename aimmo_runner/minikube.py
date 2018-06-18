#!/user/bin/env python
from __future__ import print_function

import docker
import kubernetes
import os
import re
import platform
from shell_api import (run_command, create_test_bin, BASE_DIR)
from aimmo_runner.kubernetes_setup import KubernetesBaseSetup

MINIKUBE_EXECUTABLE = "minikube"


class MinikubeRunner(KubernetesBaseSetup):

    def restart_ingress_addon(self):
        """
        Ingress needs to be restarted for old paths to be removed at startup.
        :param minikube: Executable minikube installed beforehand.
        """
        try:
            run_command([MINIKUBE_EXECUTABLE, 'addons', 'disable', 'ingress'])
        except:
            pass
        run_command([MINIKUBE_EXECUTABLE, 'addons', 'enable', 'ingress'])

    def start_cluster(self):
        """
        Starts the cluster unless it has been already started by the user.
        :param minikube: Executable minikube installed beforehand.
        """
        status = run_command([MINIKUBE_EXECUTABLE, 'status'], True)
        if 'minikube: Running' in status:
            print('Cluster already running')
        else:
            run_command([MINIKUBE_EXECUTABLE, 'start', '--memory=2048', '--cpus=2'])

    def create_docker_client(self):
        """
        Creates a docker client using the python SDK.
        :param raw_env_settings: String that is returned by the 'minikube docker-env' command.
        :return:
        """
        raw_env_settings = run_command([MINIKUBE_EXECUTABLE, 'docker-env', '--shell="bash"'], True)
        if self.vm_none_enabled(raw_env_settings):
            matches = re.finditer(r'^export (.+)="(.+)"$', raw_env_settings, re.MULTILINE)
            env_variables = dict([(m.group(1), m.group(2)) for m in matches])

            return docker.from_env(
                environment=env_variables,
                version='auto',
            )
        else:
            # VM driver is set
            return docker.from_env(
                version='auto'
            )

    def vm_none_enabled(self, raw_env_settings):
        """
        Check if the VM driver is enabled or not. This is important to see where
        the environment variables live.
        :param raw_env_settings: String that is returned by the 'minikube docker-env' command.
        :return: Boolean value indicating if enabled or not.
        """
        return False if 'driver does not support' in raw_env_settings else True

    def load_kube_config(self):
        kubernetes.config.load_kube_config(context='minikube')

    def start(self):
        """
        The entry point to the minikube class. Sends calls appropriately to set
        up minikube.
        """
        if platform.machine().lower() not in ('amd64', 'x86_64'):
            raise ValueError('Requires 64-bit')
        create_test_bin()
        os.environ['MINIKUBE_PATH'] = MINIKUBE_EXECUTABLE
        self.start_cluster()
        self.build_docker_images()
        self.restart_ingress_addon()
        ingress = self.create_ingress_yaml()
        game_creator = self.create_creator_yaml()
        self.restart_pods(game_creator, ingress)
        print('Cluster ready')
