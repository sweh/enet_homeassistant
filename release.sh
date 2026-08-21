#!/bin/bash

set -e

gh release create v$@ \
    --title "v$@" \
    --generate-notes
