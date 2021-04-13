## So you want to **clone** the project and figure out **what** to do...
* The good practice is to: 
    * Fork the project on your account
    * Clone your repo using HTTPS
    * Work on a new git branch.
    * Need help with [git](https://git-scm.com/docs/gittutorial)?
* The [issues are listed on ocadotechnology/aimmo](https://github.com/ocadotechnology/aimmo/issues). 
It's even better if you're using [ZenHub](https://www.zenhub.com/) because it will allow you to look at a [Kanban-ish board](https://github.com/ocadotechnology/aimmo/issues#boards) for the project.
Check the list selected as ["good first issue" here](https://github.com/ocadotechnology/aimmo/contribute).
## Now you want to **test** your changes and **run** the project locally...
* To work on the project, you can use whichever editor you like. Recommended: [VSCode](https://code.visualstudio.com/) with [black formatter](https://black.readthedocs.io/en/stable/) installed.
* Follow the [setup guideline here](https://github.com/ocadotechnology/aimmo/blob/development/docs/usage.md)
* You can test your change by running the test suite: `pytest`
* Don't forget to add comments if you think they will help other people to understand your code

## Great, you can **push** your changes, open a **Pull Request**, and someone in the core team will **review** it...

- Your PR title must follow the [semantic PR](https://github.com/zeke/semantic-pull-requests). Basically use `feat:` prefix for feature, and `fix:` prefix for bug fixes.
- Your PR should be connected to a corresponding ZenHub issue.
- All required status checks must pass.
- We use [reviewable](https://reviewable.io/) for code reviews. Keep an eye on notification from reviewable. You might need to go back, revise your code and push the changes again. Repeat until the PR is accepted.
## When a PR is accepted

- It will be merged into the  development branch and will get deployed into [the staging server](https://staging-dot-decent-digit-629.appspot.com/)

- Eventually, what's on staging will make its way up to [production](https://www.codeforlife.education/). Congrats! 🎉

