#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset


celery -A auction.taskapp worker -l INFO
