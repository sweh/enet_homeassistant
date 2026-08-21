#!/bin/bash

set -e

gh release create $@ \
    --title "$@" \
    --generate-notes
