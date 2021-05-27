# Life cycle of a code change

Once you're confident with the changes implemented in your local branch, you should push them and open a GitHub pull request that can be reviewed and approved. **Note that** this should be a `semantic` pull request.

## Development to Staging

The branch is ready to be merged into the `development` branch when all changes are reviewed and there are no conflicts or blocking errors.

After the PR is merged in, a `development` build starts and a beta release may or may not be created depending on the semantic PR title (see [semantic release notes](https://github.com/semantic-release/semantic-release)). The version is updated and the following are built and pushed:

- aimmo `PyPi` package (beta)
- `Docker` images: aimmo-game, aimmo-game-creator and aimmo-game-worker (beta)

Once the new beta version is released on PyPi and Docker Hub, Semaphore CI is notified and deploys it to our staging server, where the code changes will be tested further. See more details in our deploy app engine [documentation](https://github.com/ocadotechnology/codeforlife-deploy-appengine/blob/master/docs/life-cycle-of-a-code-change.md).

## Staging to Production

Once the changes on `development` are stable, this branch is merged into the `master` branch, updating it with the latest beta release. This triggers a `master` build and creates a release version. Deployment to production is manually triggered on Semaphore CI.

After a successful deployment, the `master` branch has to be merged back into the `development` one to ensure that the latter is up-to-date and ready for the next release.
