import logging
import unittest
import psutil
import time
import kubernetes.client
from aimmo_runner import runner
from connection_api import (delete_old_database, create_custom_game_default_settings)

logging.basicConfig(level=logging.WARNING)


class TestKubernetes(unittest.TestCase):
    def setUp(self):
        """
        Sets a clean database for each test before running
        starting starting the run script again. Sleeps 60 second
        between each test to ensure stable state and loads the
        api instance from the kubernetes client.
        """
        delete_old_database()
        self.processes = runner.run(use_minikube=True, server_wait=False, capture_output=True, test_env=True)
        time.sleep(120)
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
        of pods, replication controllers services, service accounts, roles/cluster roles
        and their bindings are created.
        All components created by the game will be in the "default"
        namespace.
        """

        # PODS
        api_response = self.api_instance.list_namespaced_pod("default")
        self.assertEqual(len(api_response.items), 1)
        pod_item = api_response.items[0]
        self.assertTrue(pod_item.metadata.name.startswith("aimmo-game-creator-"))
        self.assertEqual(len(pod_item.metadata.owner_references), 1)
        self.assertEqual(pod_item.metadata.owner_references[0].kind, "ReplicationController")

        # REPLICATION CONTROLLERS
        api_response = self.api_instance.list_namespaced_replication_controller("default")
        self.assertEqual(len(api_response.items), 1)
        pod_item = api_response.items[0]
        self.assertTrue(pod_item.metadata.name.startswith("aimmo-game-creator"))

        # SERVICES
        api_response = self.api_instance.list_namespaced_service("default")
        self.assertEqual(len(api_response.items), 1)
        pod_item = api_response.items[0]
        self.assertEqual(pod_item.metadata.name, "kubernetes")

        # SERVICE ACCOUNTS
        api_response = self.api_instance.list_namespaced_service_account('default')
        service_account_info = api_response.items
        single_service_account = service_account_info[1].metadata.annotations['kubectl.kubernetes.io/last-applied-configuration']
        self.assertTrue('game-creator' in single_service_account)

        single_service_account = service_account_info[2].metadata.annotations['kubectl.kubernetes.io/last-applied-configuration']
        self.assertTrue('worker' in single_service_account)

        single_service_account = service_account_info[3].metadata.annotations['kubectl.kubernetes.io/last-applied-configuration']
        self.assertTrue('worker-manager' in single_service_account)

        api_extension = kubernetes.client.RbacAuthorizationV1Api()

        # ROLES
        api_response = api_extension.list_namespaced_role('default')
        role_info = api_response.items[0].metadata.annotations['kubectl.kubernetes.io/last-applied-configuration']
        self.assertTrue('worker-manager' in role_info)

        # CLUSTER ROLES
        api_response = api_extension.list_cluster_role()
        cluster_role_info = api_response.items[0].metadata.annotations['kubectl.kubernetes.io/last-applied-configuration']
        self.assertTrue('game-creator' in cluster_role_info)

        # BINDINGS
        api_response = api_extension.list_namespaced_role_binding('default')
        role_binding_info = api_response.items[0].metadata.annotations['kubectl.kubernetes.io/last-applied-configuration']
        self.assertTrue('manage-workers' in role_binding_info)

        api_response = api_extension.list_cluster_role_binding()
        cluster_role_binding_info = api_response.items[0].metadata.annotations['kubectl.kubernetes.io/last-applied-configuration']
        self.assertTrue('create-games' in cluster_role_binding_info)

    def test_correct_initial_ingress_yaml(self):
        """
        This test will ensure that the initial yaml created on a
        fresh state of the cluster. It assumes: ingress name, no backend
        and only one specific rule, with only one path specified!
        """
        api_response = self.api_extension_instance.list_namespaced_ingress("default")
        self.assertEqual(len(api_response.items), 1)

        # NAME
        self.assertEqual(api_response.items[0].metadata.name, "aimmo-ingress")

        # NO BACKEND
        self.assertEqual(api_response.items[0].spec.backend, None)

        # RULES
        rule = api_response.items[0].spec.rules[0]
        self.assertEqual(len(api_response.items[0].spec.rules), 1)
        self.assertEqual(rule.host,
                         "local.aimmo.codeforlife.education")

        # PATHS
        path = rule.http.paths[0]
        self.assertEqual(len(rule.http.paths), 1)
        self.assertEqual(path.backend.service_name, "default-http-backend")
        self.assertEqual(path.path, None)

    @unittest.skip("Broken Test.")
    def test_adding_custom_game_sets_cluster_correctly(self):
        """
        Log into the server as admin (superuser) and create a game
        with the name "testGame", using the default settings provided.
        """

        def _wait_for_kubernetes_cluster(api_instance):
            timeout = 0

            while timeout <= 200:
                temp_response = api_instance.list_namespaced_pod("default")

                if timeout == 200:
                    self.fail("Worker not created!")

                for item in temp_response.items:
                    if item.metadata.name.startswith("aimmo-1-worker"):
                        return

                timeout += 1
                time.sleep(1)

        request_response = create_custom_game_default_settings(name="testGame")

        # WORKER
        _wait_for_kubernetes_cluster(self.api_instance)

        # SERVICE
        api_response = self.api_instance.list_namespaced_service("default")

        service_names = [service.metadata.name for service in api_response.items]
        if "game-1" not in service_names:
            self.fail("Service not created!")

        # REPLICATION CONTROLLERS
        api_response = self.api_instance.list_namespaced_replication_controller("default")

        rc_names = [rc.metadata.name for rc in api_response.items]
        if "game-1" not in rc_names:
            self.fail("Replication controller not created!")

    @unittest.skip("Not Implemented.")
    def test_adding_game_appends_path_to_ingress(self):
        """
        Adding a game (level), will append the correct path to the ingress at /game-1.
        """
        pass

    @unittest.skip("Not Implemented.")
    def test_remove_old_ingress_paths_on_startup(self):
        """
        A game is created in the minikube instance and ingress path is appended. The
        cluster is then stopped and started again with a fresh database. When this happens,
        we check that the ingress paths are returned to default again.
        """
        pass
