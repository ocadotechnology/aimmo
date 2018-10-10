if [ "$TRAVIS_PULL_REQUEST_BRANCH" != "" ]
then
    export BRANCH=$TRAVIS_PULL_REQUEST_BRANCH
else
    export BRANCH="$TRAVIS_BRANCH"
fi

if [ "$BRANCH" = "versions" ]
then
    export TAG_NAME="$(cat version.txt).b$TRAVIS_BUILD_NUMBER"
else
    export TAG_NAME="$(cat version.txt)"
fi

git tag "$TAG_NAME"
git push origin "$TAG_NAME"
