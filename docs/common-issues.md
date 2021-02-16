# Common / Known Issues
- [When running the game I get `no module named google.auth`](#when-running-the-game-i-get-`no-module-named-google.auth`)
- [When deploying I get `error: Error -5 while decompressing data (...)`](#when-deploying-i-get-error-error--5-while-decompressing-data-)
- [When running the game I get `ImportError: No module named django.conf`](#when-running-the-game-i-get-importerror-no-module-named-djangoconf)
- [On Mac, when running the server with a fresh database, I get `django.db.utils.IntegrityError: The row in table ... with primary key '1' has an invalid foreign key: ... contains a value '1' that does not have a corresponding value in ...`](#on-mac-when-running-the-server-with-a-fresh-database-i-get-djangodbutilsintegrityerror-the-row-in-table--with-primary-key-1-has-an-invalid-foreign-key--contains-a-value-1-that-does-not-have-a-corresponding-value-in-)
---

## When running the game I get `no module named google.auth`

If you get an error when running the command `./run.py` or `./run.py -k` locally that states, somewhere in the
traceback, `no module named google.auth`; then rerun the command again and the dependency should be
detected. This is a [logged issue](https://github.com/ocadotechnology/aimmo/issues/449).

## When deploying I get `error: Error -5 while decompressing data (...)`

**This issue can only be solved by a repository admin.**

When deploying with semaphoreCI, the cache may be old and corrupt one of the packages being installed by `pip`. 

The error you may get may look like this `error: Error -5 while decompressing data: incomplete or truncated stream`. 

You need to `ssh` into the appropriate server and delete the cache directory. Another solution is to `pip install` with the `--no-cache-dir` flag but we do not recommend this.

## When running the game I get `ImportError: No module named django.conf`

Run a pip install command to install django before running the project. Django should then resolve all the other dependencies specified in the setup file. To do this run: `pip install django=={version}`. You can find `version` from the `setup.py` file at the time.


## On Mac, when running the server with a fresh database, I get `django.db.utils.IntegrityError: The row in table '...' with primary key '1' has an invalid foreign key: ... contains a value '1' that does not have a corresponding value in ...`

This error is potentially caused by a wrong or incompatible sqlite3 version. You can check the sqlite3 version from a python shell with:

```
import sqlite3
sqlite3.sqlite_version.
```

You need to install/update sqlite3 with brew: `brew install sqlite3`. Then follow the instructions in `brew info sqlite3` before installing a python version with `pyenv`.

```
If you need to have sqlite first in your PATH, run:
  echo 'export PATH="/usr/local/opt/sqlite/bin:$PATH"' >> ~/.zshrc

For compilers to find sqlite you may need to set:
  export LDFLAGS="-L/usr/local/opt/sqlite/lib"
  export CPPFLAGS="-I/usr/local/opt/sqlite/include"
```

If you already installed a python version and a virtual environment, you need to clear them up:
```
pyenv versions
pyenv uninstall <PYTHON VERSION>
pipenv --rm
```

Then reinstall pyenv with the right sqlite3 version (make sure `LDFLAGS` and `CPPFLAGS` are set as above):
```
pyenv install <PYTHON VERSION>
pipenv install --dev
```
