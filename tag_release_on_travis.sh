if [ "$TRAVIS_PULL_REQUEST_BRANCH" != "" ]
then
    export BRANCH=$TRAVIS_PULL_REQUEST_BRANCH
else
    export BRANCH="$TRAVIS_BRANCH"
fi


git tag "$(cat version.txt).b$TRAVIS_BUILD_NUMBER.dev$TRAVIS_BUILD_NUMBER"
# if [ "$BRANCH" = "development" ]
# then
#     git tag "$(cat version.txt).b$TRAVIS_BUILD_NUMBER"
# else
#     git tag "$(cat version.txt)"
# fi
