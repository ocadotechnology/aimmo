#!/usr/bin/env python
import argparse
import os
import signal
import traceback

import time

from aimmo_runner import runner

parser = argparse.ArgumentParser(description="Runs Kurono.")

parser.add_argument(
    "-k",
    "--kube",
    dest="use_minikube",
    action="store_true",
    default=False,
    help="To specify if you want to use your minikube enviroment for Kurono, default is basic docker containers.",
)
parser.add_argument(
    "-t",
    "--target",
    dest="build_target",
    choices=["runner", "tester"],
    action="store",
    default="runner",
    help="""Specify the build stage you wish the docker containers to stop at.
                            By default we simply run the project. This can be used to run the tests
                            but it is recommended that you used 'all_tests.py'
                            Options: runner, tester  """,
)
parser.add_argument(
    "-c",
    "--using-cypress",
    dest="using_cypress",
    action="store_true",
    default=False,
    help="""Specify if you want to run the project for running Cypress tests. This
    disables the building of the Docker images.""",
)

if __name__ == "__main__":
    try:
        args = parser.parse_args()

        runner.run(
            args.use_minikube,
            using_cypress=args.using_cypress,
            build_target=args.build_target,
        )
    except Exception as err:
        traceback.print_exc()
        raise
    finally:
        os.killpg(0, signal.SIGTERM)
        time.sleep(0.9)
        os.killpg(0, signal.SIGKILL)
