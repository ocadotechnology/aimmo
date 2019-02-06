# Gets the container ID of the last container (will be the one used for tests on travis) and pulls the
# coverage files out.
read CONTAINERID <<< $(docker ps --all -q | head -1)
sudo docker cp -a $CONTAINERID:.coverage $(pwd)/.coverage
sudo docker cp -a $CONTAINERID:coverage.xml $(pwd)/coverage.xml
