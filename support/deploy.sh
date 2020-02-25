#!/bin/bash

echo "Deploy to gh-graph of ${GITHUB_REPOSITORY}"
SSH_DIR="${HOME}/.ssh"
HAVE_PAGES_BRANCH=true
SKIP_PUSH=false

mkdir "${SSH_DIR}"
ssh-keyscan -t rsa github.com > "${SSH_DIR}/known_hosts"
echo "${GITHUB_PAGES_DEPLOY_KEY}" > "${SSH_DIR}/id_rsa"
chmod 400 "${SSH_DIR}/id_rsa"

GITHUB_REPOSITORY='ousheobin/covid-19-vis'
REMOTE_REPO="git@github.com:${GITHUB_REPOSITORY}.git"
REMOTE_BRANCH="gh-pages"

git fetch origin

if [ -n "$(git branch -a | grep gh-pages)" ]; then
    echo "Git branch gh-pages exists. Will fetch branch from github."
    git clone -b gh-pages ${REMOTE_REPO} distrepo
    cd "./distrepo"
    rm -rf ./*
    cp -r ../dist/. ./
    git checkout gh-pages
else
    echo "Git branch gh-pages not exists. Will create it."
    cd "./dist"
    git init
    git checkout --orphan "${REMOTE_BRANCH}"
    git remote add origin "${REMOTE_REPO}"
fi

git config user.name "Github Action Robort"
git config user.email "ousheobin@users.noreply.github.com"

git add --all

git commit -m "[Automation] Update the web pages and reference csv." || SKIP_PUSH=true

git push origin "${REMOTE_BRANCH}"

echo "Deployment done. SHA: ${GITHUB_SHA}"