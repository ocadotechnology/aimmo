## So you want to **clone** the project and figure out **what** to do...
* The good practice is to: 
    * Fork the project on your account
    * Clone your repo using HTTPS
    * Work on a new git branch.
    * Need help with [git](https://git-scm.com/docs/gittutorial)?
    Anyway you can't use Ocado Technology's master.
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
* Then you can commit! On a new branch for a new Pull Request please.
* If your commit resolves a GitHub issue, please include “fixes #123” in the commit message.
* Then you can push to your forked repo, and create a pull request from your branch to ocadotechnology's master branch.
* Some tests will run automatically: Travis will run the automated tests, coverage will test the test coverage. Please fix found issues, then repush on your branch - it will rerun the tests.
* Do not accept a PR yourself - at least someone else should review your code and approve it first.
* Some old PRs will need to see the branch rebased on the current master
* When a PR is accepted, **congrats!** It will be merged on master.

## Some conventions to keep in mind...
We follow PEP8 convention quite strictly however we do make a few exceptions to this rule. They are as follows:

#### Maximum Line Length
PEP8 specifies that the maximum line length is to be limited to *79 characters* with some lines even shorter than this. We replace this rule and try to stick to *90 characters*.

#### Line Breaking after/before binary operators
The internet seems be divided and PEP8 had some major changes when it comes to this rule. We have agreed that we want to strictly use binary operators on the **next** line, as opposed to before the line break.

#### Indentation on line breaks
The indentation should be kept consistent by the use of **parenthesis** appropriately. Example:
```python
if (cell.location != always_empty_location
        and random.random() < self.settings['OBSTACLE_RATIO']):
```
