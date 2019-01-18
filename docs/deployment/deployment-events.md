# Deployment Events

We use Travis for contiguous integration. Travis CI is the first step in our integration pipeline. Each time a push is made Travis runs all our tests and sends the coverage reports for display to [coveralls.io](https://coveralls.io/). 

Our package Django app `aimmo` is deployed to [Pypi](https://pypi.python.org/pypi/aimmo) and we use [Versioneer](https://github.com/warner/python-versioneer) for package versioning.

The rest of the components are Dockerized. Travis CI automatically recognizes the **Dockerfiles** inside of each of the modules and pushes the newly created images to the **Docker Hub Registry**. Each of the components are then pulled automatically by the Google Cloud Container Engine. 

After all the Travis processes are finished, a curl request is made to SemaphoreCI. SemaphoreCI is responsible for orchestrating the deployment processes for all the Code For Life repositories. The Django application `aimmo` is installed directly from Pypi together with all the other modules. Due to the modularity of Django, the aimmo app can be just plugged inside the bigger Django project. _Currently, the pulled version in production will be the latest._

The application is then deployed to the Google Cloud. This finishes our build.

Once the application is deployed to the Google Cloud, it needs to find the other services. The discovery of the game services provided is done using a hook that can be found in [this repository](https://github.com/ocadotechnology/codeforlife-deploy-appengine). 

```python
AIMMO_GAME_SERVER_LOCATION_FUNCTION = lambda game: ('http://staging.aimmo.codeforlife.education', "/game/%s/socket.io" % game)
```
