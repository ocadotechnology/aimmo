# Deployment Events

**_We have moved to using Github actions for our CI. This sections needs updating._**

---

We use Travis for contiguous integration. Travis CI is the first step in our integration pipeline. Each time a push is made Travis runs all our tests. We are currently in the process of migrating our coverage reports from [coveralls.io](https://coveralls.io/) to [codecov.io](https://codecov.io/).

Our package Django app `aimmo` is deployed to [Pypi](https://pypi.python.org/pypi/aimmo) and we use [Versioneer](https://github.com/warner/python-versioneer) for package versioning.

The rest of the components are Dockerised. Travis CI automatically recognises the **Dockerfiles** inside of each of the modules and pushes the newly created images to the **Docker Hub Registry**. Each of the components are then pulled automatically by the Google Cloud Container Engine.

After all the Travis processes are finished, a curl request is made to SemaphoreCI. SemaphoreCI is responsible for orchestrating the deployment processes for all the Code For Life repositories. The Django application `aimmo` is installed directly from Pypi together with all the other modules. Due to the modularity of Django, the aimmo app can be just plugged inside the bigger Django project. _Currently, the pulled version in production will be the latest stable release._

The application is then deployed to the Google Cloud. This finishes our build.

Once the application is deployed to the Google Cloud, it needs to find the other services. The discovery of the game services provided is done using a hook that can be found in [this repository](https://github.com/ocadotechnology/codeforlife-deploy-appengine).

```python
AIMMO_GAME_SERVER_LOCATION_FUNCTION = lambda game: ('http://staging.aimmo.codeforlife.education', "/game/%s/socket.io" % game)
```

# Deploying to production

Every time a new push is made to the development branch, the deployment process detailed above runs. This updates the `aimmo` project in our staging environment.

To deploy to production, a pull request needs to be made from development into master. After the pull request is successfully reviewed and merged, the deployment process will run once more, with the small difference that the build tag will indicate that it is now a stable release, instead of a beta build.

Monitoring the deployment process at this point is as important as always, if not more. Once the tests on Travis have passed, the Pypi package has been deployed and the Docker images have been built, the new version can then be deployed onto production from Semaphore CI. It is important to remember that this will also deploy the latest changes from Rapid Router and the Portal onto production.
