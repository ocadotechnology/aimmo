read CONTAINERID <<< $(docker ps --all -q | head -1)
sudo docker cp -a $CONTAINERID:.coverage $(pwd)/.coverage
sudo docker cp -a $CONTAINERID:coverage.xml $(pwd)/coverage.xml