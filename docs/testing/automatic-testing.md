# Automatic Testing
- [Unit Tests](#unit-tests)
- [Functional Tests](#functional-tests)
- [Integration Tests](#integration-tests)
- [Testing Tools](#testing-tools)
- [Coverage Tools](#coverage-tools)

---


## Unit Tests
Currently our unit tests are located in `[module name]/tests/test_simulation`. They check that individual pieces of our code base work correctly, without integration of other functionality. They are all prefixed with `test_` and this is the requirement for it to be recognized when `all_tests.py` is ran. 

Every time you add a new piece of functionality; the bare minimum is to reflect this in the unit tests.

## Functional Tests
Our functional tests can be found in `[module name]/tests/functional`. They generally tend to mock all the logic of the game without actually integrating the surrounding server architectures.

## Integration Tests
TODO

## Testing Tools
[Hypothesis](https://hypothesis.works/) is a property based tool that can be used to run tests with a way wider range of scenario's than we could possibly design. It tends to find edge cases that we may have (and have already) missed various times. We encourage to convert current tests to make use of this framework as well as designing new ones with this.

## Coverage Tools
Our coverage tool right now is [coveralls](https://coveralls.io/). For the moment we do not count the coverage over the tests. This gives a closer to reality coverage, but it does not check if all the tests run.