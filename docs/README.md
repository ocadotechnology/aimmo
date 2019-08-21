# Table Of Contents

---

## Getting started
The first required steps to get familiar with the project and run it locally.
- [FAQ](FAQ.md) - Frequently asked questions with answers.
- [Usage](usage.md) - How to get the project up and running.
- [Common Issues](common-issues.md) - Common issues and their solutions.

## Architecture

Architecture of the project. How things are structured, what components exist, etc.
![](architecture/uml.png?raw=true)
- [Architecture](architecture/README.md)
    - [Game Creator](architecture/game-creator/README.md)
    - [Games](architecture/games/README.md)
    - [Workers](architecture/workers/README.md)
    - [UI](architecture/ui/README.md)

### Babylon

Babylon side of the project. Game engine and structure.
- [Babylon](babylon/README.md)


### Infrastucture

We describe the technologies that are underlying to the project and support it
- [Infrastructure](infrastructure/README.md)

### Testing 

Levels of testing within Kurono.

- [Testing](testing/README.md)
    - [Manual Test Plan](testing/test-plan.md)
    - [Automatic Test Plan](testing/automatic-testing.md)

### Deployment

The process of continuous integration and deployment of our project onto our cloud.

- [Deployment](deployment/README.md)
    - [Sequence of Deployment Events](deployment/deployment-events.md)
    - [Admin NGINX & SSL setup on GCP](deployment/nginx-setup.md)
