#!/usr/bin/env python
import os
import signal
import sys
import time
import traceback
import argparse
from aimmo_runner import runner

parser = argparse.ArgumentParser(description="Runs AI:MMO.")

parser.add_argument(
    "-k",
    "--kube",
    dest="use_minikube",
    action="store_true",
    default=False,
    help="To specify if you want to use your minikube enviroment for AI:MMO, default is basic docker containers.",
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

if __name__ == "__main__":
    try:
        args = parser.parse_args()

        runner.run(args.use_minikube, build_target=args.build_target)
    except Exception as err:
        traceback.print_exc()
        raise
    finally:
        os.killpg(0, signal.SIGTERM)
        time.sleep(0.9)
        os.killpg(0, signal.SIGKILL)
