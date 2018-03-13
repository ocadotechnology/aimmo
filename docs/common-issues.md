# Common / Known Issues
- [When running the game I get `no module named google.auth`](#when-running-the-game-i-get-`no-module-named-google.auth`)
- [When deploying I get `error: Error -5 while decompressing data (...)`](#when-deploying-i-get-`error:-error--5-while-decompressing-data-(...)`)
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
