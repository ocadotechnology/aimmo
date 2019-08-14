## So you want to **clone** the project and figure out **what** to do...
* The good practice is to: 
    * Fork the project on your account
    * Clone your repo using HTTPS
    * Work on a new git branch.
    * Need help with [git](https://git-scm.com/docs/gittutorial)?
* The [issues are listed on ocadotechnology/aimmo](https://github.com/ocadotechnology/aimmo/issues). 
It's even better if you're using [ZenHub](https://www.zenhub.com/) because it will allow you to look at a [Kanban-ish board](https://github.com/ocadotechnology/aimmo/issues#boards) for the project.
The new starter / up-for-grabs issues are listed with the [help wanted label](https://github.com/ocadotechnology/aimmo/labels/help%20wanted)

## Now you want to **test** your changes and **run** the project locally...
* To work on the project, you can use whichever editor you like. Lots here like [IntelliJ or PyCharm](https://www.jetbrains.com/), for instance.
* As said in the [readme](https://github.com/ocadotechnology/aimmo), you should set up a virtual environment. 
    * e.g. the first time, `mkvirtualenv -a path/to/aimmo aimmo`
    * and thereafter: `workon aimmo`
* You can test your change by running the test suite - you can go to the root of the project and type: `python example_project/manage.py test` ; but Travis uses `python setup.py test` (will also install stuff in your virtualenv needed for the tests)
* To manually test things and run the project, `./run` in the root.

## Great, you can **commit**, open a **Pull Request**, and we'll **review** it...

Before you merge:
- Your PR should be connected to a corresponing ZenHub issue.
- All required status checks must pass.
- Add documentation if necessary

* Do not accept a PR yourself - at least someone else should review your code and approve it first.

### When a PR is accepted

1. It will be merged into the  development branch
2. A new beta version of Kurono will be released on PyPI and Docker Hub
3. The beta will be tested on our staging servers

Eventually, development will be merged into master. This will trigger a stable release which will make it's way up to production. Congrats! 🎉

## Some conventions to keep in mind...
We follow PEP8 convention quite strictly however we do make a few exceptions to this rule. They are as follows:

#### Maximum Line Length
PEP8 specifies that the maximum line length is to be limited to *79 characters* with some lines even shorter than this. We replace this rule and try to stick to *90 characters*.

#### Line Breaking after/before binary operators
The internet seems to be divided and PEP8 had some major changes when it comes to this rule. We have agreed that we want to strictly use binary operators on the **next** line, as opposed to before the line break.

#### Indentation on line breaks
The indentation should be kept consistent by the use of **parenthesis** appropriately. Example:
```python
if (cell.location != always_empty_location
        and random.random() < self.settings['OBSTACLE_RATIO']):
```
