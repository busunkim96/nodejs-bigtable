#!/bin/bash

set -xeo pipefail

ROOT=${KOKORO_ARTIFACTS_DIR}/github/nodejs-bigtable

export PACKAGE=bigtable
export PACKAGE_VERSION=$(python ${ROOT}/docs-experimental/get_package_version.py ${ROOT})
export PACKAGE_LANGUAGE=nodejs
export PACKAGE_DOCUMENTATION=${ROOT}/docs/@google-cloud/${PACKAGE}/${PACKAGE_VERSION}

cd ${ROOT}

# Build docs
export NPM_CONFIG_PREFIX=/home/node/.npm-global

npm install

npm run docs

# Set git account identity
git config --global user.email "busunkim@google.com"
git config --global user.name "Bu Sun Kim"

# docs-publisher will push the docs to git-on-borg repo
python ${ROOT}/docs-experimental/experimental_docs_publisher.py
