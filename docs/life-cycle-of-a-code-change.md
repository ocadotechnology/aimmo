# Life cycle of a code change
Once you're confident with the changes implemented in your local branch, you should push them and open a GitHub pull request that can be reviewed and approved. **Note that** this should be a [semantic pull request](https://github.com/semantic-release/semantic-release).

* The branch is ready to be merged into the `development` branch when all changes are reviewed and there are no conflicts or blocking errors.
* After the PR is merged in, a `development` build starts and a beta release may or may not be created depending on the semantic PR title.
* The `master` branch then has to be updated with the latest beta release by having the `development` branch merged in. This triggers a `master` build and creates a release version.
* Deployment to production is manually triggered on Semaphore CI 🚦
* After a successful deployment, the `master` branch has to be merged back into the `development` one to ensure that the latter is up-to-date and ready for the next release 🚀
