#!/bin/bash

set -xeo pipefail

export PACKAGE=bigtable
export GITHUB_PACKAGE_ROOT=${KOKORO_ARTIFACTS_DIR}/github/nodejs-bigtable
export GITHUB_PACKAGE_VERSION=$(python ${GITHUB_PACKAGE_ROOT}/docs-experimental/get_package_version.py ${GITHUB_PACKAGE_ROOT})
export GITHUB_PACKAGE_LANGUAGE=nodejs
export GITHUB_PACKAGE_DOCUMENTATION=${GITHUB_PACKAGE_ROOT}/docs/@google-cloud/${PACKAGE}/${GITHUB_PACKAGE_VERSION}

cd $GITHUB_PACKAGE_ROOT

# Build docs
export NPM_CONFIG_PREFIX=/home/node/.npm-global

npm install

npm run docs

# Set git account identity
git config --global user.email "busunkim@google.com"
git config --global user.name "Bu Sun Kim"

# docs-publisher will push the docs to git-on-borg repo
python ${GITHUB_PACKAGE_ROOT}/docs-experimental/experimental_docs_publisher.py
