#!/usr/bin/env python
import argparse
import logging
import traceback

from aimmo_runner import runner

logging.basicConfig()

parser = argparse.ArgumentParser(description="Runs Kurono.")

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
    disables the building of the Docker images and builds the frontend in production 
    mode without watching for changes.""",
)

if __name__ == "__main__":
    try:
        args = parser.parse_args()

        runner.run(
            using_cypress=args.using_cypress,
            build_target=args.build_target,
        )
    except Exception as err:
        traceback.print_exc()
        raise
