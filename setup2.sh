#!/usr/bin/env bash

# cd /autograder/source
# source ./config.sh

mkdir -p /root/.ssh
cp ssh_config /root/.ssh/config
# Make sure to include your private key here
cp deploy_key /root/.ssh/deploy_key
chmod 0600 /root/.ssh/deploy_key
# To prevent host key verification errors at runtime
ssh-keyscan -t rsa github.com >> ~/.ssh/known_hosts

# Initialize git repo with assignment files
git clone git@github.com:tnelson/lfs.git

chmod +x run_autograder
mv run_autograder /autograder/run_autograder

cd /autograder

# Install racket
apt update
apt-get update -y
apt install software-properties-common -y
add-apt-repository ppa:plt/racket -y
apt-get install -y racket
apt-get install default-jre -y
apt-get clean

# # Install forge
# raco pkg install forge 

git clone https://github.com/tnelson/Forge.git
cd Forge/forge
git checkout grading
raco pkg install --auto --no-docs

