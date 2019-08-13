import argparse

from semantic_release.history import set_new_version

from aimmo import __version__

parser = argparse.ArgumentParser(description="Update version based on branch.")
parser.add_argument("DEPLOY_TO_DEV", type=bool, help="True if build to dev")
parser.add_argument("TRAVIS_BUILD_NUMBER", type=int, help="Travis build number")
parser.add_argument(
    "TRAVIS_PULL_REQUEST_BRANCH",
    type=basestring,
    help="The name of the PR branch, otherwise empty",
)
parser.add_argument(
    "TRAVIS_BRANCH", type=basestring, help="Name of the branch the build is on"
)

args = parser.parse_args()

if args.DEPLOY_TO_DEV:
    version = __version__ + "dev" + args.TRAVIS_BUILD_NUMBER

if args.TRAVIS_PULL_REQUEST_BRANCH != "":
    BRANCH = args.TRAVIS_PULL_REQUEST_BRANCH
else:
    BRANCH = args.TRAVIS_BRANCH

if BRANCH == "development":
    version = __version__ + ".b" + args.TRAVIS_BUILD_NUMBER
else:
    version = __version__

set_new_version(version)
