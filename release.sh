#!/bin/bash

set -euo pipefail

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <version>"
    echo "Example: $0 1.2.3"
    exit 1
fi

VERSION="$1"
MANIFEST="custom_components/enet/manifest.json"

if [ ! -f "$MANIFEST" ]; then
    echo "Manifest not found: $MANIFEST"
    exit 1
fi

# Update version in manifest.json
sed -i -E \
    's/("version"[[:space:]]*:[[:space:]]*)"[^"]*"/\1"'"$VERSION"'"/' \
    "$MANIFEST"

git add "$MANIFEST"
git commit -m "Release v${VERSION}"
git push

gh release create "v${VERSION}" \
    --title "v${VERSION}" \
    --generate-notes
