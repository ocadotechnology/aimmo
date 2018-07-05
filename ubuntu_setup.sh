apt-get update
apt-get install -y apache2
curl -sL https://deb.nodesource.com/setup_10.x | sudo -E bash -
curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -
echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list
apt-get update
apt-get install -y nodejs
apt-get install -y python-pip
pip install pipenv

apt-get install -y yarn
yarn add global parcel-bundler
sysctl fs.inotify.max_user_watches=99999
export PATH="$(yarn global bin):$PATH"

pipenv install && pipenv shell
