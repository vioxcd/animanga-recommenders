#!/bin/bash
set -euo pipefail

GIT_COMMIT=$(git rev-parse --short HEAD)
GIT_BRANCH=$(git rev-parse --abbrev-ref HEAD)

docker build -t animanga-recommenders-fastapi:latest \
  --label git-commit=$GIT_COMMIT \
  --label git-branch=$GIT_BRANCH .

