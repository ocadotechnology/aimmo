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
from abc import ABCMeta, abstractmethod


class KubernetesBaseSetup():
    __metaclass__ = ABCMeta

    def get_ip(self):
        """
        Get a single primary IP address. This will not return all IPs in the
        interface. See http://stackoverflow.com/a/28950776/671626
        :return: Integer with the IP of the user.
        """
        os_name = platform.system()
        if os_name == "Darwin":
            return socket.gethostbyname(socket.gethostname())

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # noinspection PyBroadException
        try:
            # doesn't even have to be reachable
            client_socket.connect(('10.255.255.255', 0))
            IP = client_socket.getsockname()[0]
        except:
            IP = '127.0.0.1'
        finally:
            client_socket.close()
        return IP

    def create_ingress_yaml(self):
        """
        Loads a ingress yaml file into a python object.
        """
        path = os.path.join(BASE_DIR, 'ingress.yaml')
        with open(path) as yaml_file:
            content = yaml.safe_load(yaml_file.read())
        return content

    def create_creator_yaml(self):
        """
        Loads a replication controller yaml file into a python object.
        """
        orig_path = os.path.join(BASE_DIR, 'aimmo-game-creator', 'rc-aimmo-game-creator.yaml')
        with open(orig_path) as orig_file:
            content = yaml.safe_load(orig_file.read().replace('latest', 'test').replace('REPLACE_ME', 'http://%s:8000/players/api/games/' % self.get_ip()))
        return content

    @abstractmethod
    def create_docker_client(self):
        pass

    def build_docker_images(self):
        """
        Finds environment settings and builds docker images for each directory.
        :param minikube: Executable command to run in terminal.
        """
        print('Building docker images')

        client = self.create_docker_client()

        directories = ('aimmo-game', 'aimmo-game-creator', 'aimmo-game-worker')
        for dir in directories:
            path = os.path.join(BASE_DIR, dir)
            tag = 'ocadotechnology/%s:test' % dir
            print("Building %s..." % tag)
            client.images.build(
                path=path,
                tag=tag,
                encoding='gzip'
            )

    @abstractmethod
    def load_kube_config(self):
        pass

    def restart_pods(self, game_creator_yaml, ingress_yaml):
        """
        Disables all the components running in the cluster and starts them again
        with fresh updated state.
        :param game_creator_yaml: Replication controller yaml settings file.
        :param ingress_yaml: Ingress yaml settings file.
        """
        print('Restarting pods')
        self.load_kube_config()
        api_instance = kubernetes.client.CoreV1Api()
        extensions_api_instance = kubernetes.client.ExtensionsV1beta1Api()
        for rc in api_instance.list_namespaced_replication_controller('default').items:
            api_instance.delete_namespaced_replication_controller(
                body=kubernetes.client.V1DeleteOptions(),
                name=rc.metadata.name,
                namespace='default')
        for pod in api_instance.list_namespaced_pod('default').items:
            api_instance.delete_namespaced_pod(
                body=kubernetes.client.V1DeleteOptions(),
                name=pod.metadata.name,
                namespace='default')
        for service in api_instance.list_namespaced_service('default').items:
            api_instance.delete_namespaced_service(
                name=service.metadata.name,
                namespace='default')
        for ingress in extensions_api_instance.list_namespaced_ingress('default').items:
            extensions_api_instance.delete_namespaced_ingress(
                name=ingress.metadata.name,
                namespace='default',
                body=kubernetes.client.V1DeleteOptions())

        extensions_api_instance.create_namespaced_ingress("default", ingress_yaml)
        api_instance.create_namespaced_replication_controller(
            body=game_creator_yaml,
            namespace='default',
        )

    @abstractmethod
    def start():
        """
        The entry point to the kubernetes setup. Sends calls appropriately to set
        up kubernetes.
        """
        pass
