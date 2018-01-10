import logging
import psutil
import time
import kubernetes.client
from unittest import TestCase
from connection_set_up import delete_old_database

import sys
sys.path.append("..")

from .. import run

logging.basicConfig(level=logging.WARNING)


class TestKubernetes(TestCase):
    def setUp(self):
        """
        Sets a clean database for each test before running
        starting starting the run script again. Sleeps 60 second
        between each test to ensure stable state and loads the
        api instance from the kubernetes client.
        """
        delete_old_database()
        time.sleep(120)
        run.main(use_minikube=True, server_wait=False)
        kubernetes.config.load_kube_config(context='minikube')
        self.api_instance = kubernetes.client.CoreV1Api()
        self.api_extension_instance = kubernetes.client.ExtensionsV1beta1Api()

    def tearDown(self):
        """
        Kills the process and its children peacefully.
        """
        for process in self.processes:
            try:
                parent = psutil.Process(process.pid)
            except psutil.NoSuchProcess:
                return

            children = parent.children(recursive=True)

            for child in children:
                child.terminate()

    def test_clean_starting_state_of_cluster(self):
        """
        The purpose of this test is to check the correct number
        of pods, replication controllers and services are created.
        All components created by the game will be in the "default"
        namespace.
        """

        # PODS
        api_response = self.api_instance.list_namespaced_pod("default")
        self.assertEqual(len(api_response.items), 1)
        pod_item = api_response.items[0]
        self.assertTrue(pod_item.metadata.name.startswith("aimmo-game-creator-"))
        self.assertEquals(len(pod_item.metadata.owner_references), 1)
        self.assertEquals(pod_item.metadata.owner_references[0].kind, "ReplicationController")

        # REPLICATION CONTROLLERS
        api_response = self.api_instance.list_namespaced_replication_controller("default")
        self.assertEqual(len(api_response.items), 1)
        self.assertTrue(pod_item.metadata.name.startswith("aimmo-game-creator"))

        # SERVICES
        api_response = self.api_instance.list_namespaced_service("default")
        self.assertEqual(len(api_response.items), 1)
        self.assertTrue(pod_item.metadata.name == "kubernetes")

    def test_correct_initial_ingress_yaml(self):
        """
        This test will ensure that the initial yaml created on a
        fresh state of the cluster. It assumes: ingress name, no backend
        and only one specific rule, with only one path specified!
        """
        api_response = self.api_extension_instance.list_namespaced_ingress("default")
        self.assertEquals(api_response.items, 1)

        # NAME
        self.assertEqual(api_response.items[0].metadata.name, "aimmo-ingress")

        # NO BACKEND
        self.assertEqual(api_response.items[0].spec.backend, None)

        # RULES
        rule = api_response.items[0].spec.rules[0]
        self.assertEqual(len(api_response.items[0].spec.rules), 1)
        self.assertEqual(rule.host,
                         "dev.aimmo.codeforlife.education")

        # PATHS
        path = rule.http.path[0]
        self.assertEqual(len(rule.http.paths), 1)
        self.assertEqual(path.service_name, "default_http_backend")
        self.assertEqual(path.path, None)
