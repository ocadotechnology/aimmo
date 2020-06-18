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
    "-ns",
    "--no-server",
    dest="server_wait",
    action="store_false",
    default=True,
    help="""Specify if you don't wish to start and wait for the server. If not, the
    run command will end after building the docker images.""",
)

if __name__ == "__main__":
    try:
        args = parser.parse_args()

        runner.run(args.use_minikube, args.server_wait, build_target=args.build_target)
    except Exception as err:
        traceback.print_exc()
        raise
    finally:
        os.killpg(0, signal.SIGTERM)
        time.sleep(0.9)
        os.killpg(0, signal.SIGKILL)
