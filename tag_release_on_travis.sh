if [ "$TRAVIS_PULL_REQUEST_BRANCH" != "" ]
then
    export BRANCH=$TRAVIS_PULL_REQUEST_BRANCH
else
    export BRANCH="$TRAVIS_BRANCH"
fi

if [ "$BRANCH" = "versions" ]
then
    git tag "$(cat version.txt).b$TRAVIS_BUILD_NUMBER"
else
    git tag "$(cat version.txt)"
fi
