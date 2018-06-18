#!/user/bin/env python
from __future__ import print_function

import docker
import kubernetes
import os
import re
import socket
import yaml
import platform
from shell_api import (run_command, create_test_bin, BASE_DIR)
from aimmo_runner.kubernetes_setup import KubernetesBaseSetup


class VagrantRunner(KubernetesBaseSetup):
    def create_docker_client(self):
        """
        Creates a docker client using the python SDK.
        :param raw_env_settings: String that is returned by the 'minikube docker-env' command.
        :return:
        """
        return docker.from_env(
            version='auto'
        )

    def load_kube_config(self):
        kubernetes.config.load_kube_config(config_file='/vagrant/kubeconfig_aimmo.yml', context='service-account-context')

    def start(self):
        """
        The entry point to the minikube class. Sends calls appropriately to set
        up minikube.
        """
        if platform.machine().lower() not in ('amd64', 'x86_64'):
            raise ValueError('Requires 64-bit')
        create_test_bin()
        self.build_docker_images()
        ingress = self.create_ingress_yaml()
        game_creator = self.create_creator_yaml()
        self.restart_pods(game_creator, ingress)
        print('Cluster ready')
