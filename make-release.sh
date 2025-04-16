#!/bin/bash
set -e

# GitHub repo in format: user/repo
GITHUB_REPO="matt-gree/RioWebCLI"

# Get the latest release version from GitHub
echo "🔍 Checking latest release on GitHub..."
LATEST_VERSION=$(curl -s "https://api.github.com/repos/$GITHUB_REPO/releases/latest" | sed -n 's/.*"tag_name": "\(.*\)".*/\1/p')

echo "📌 Latest GitHub release: ${LATEST_VERSION:-No releases yet}"

# Prompt for new version number
read -p "📝 Enter new version number (e.g., 1.0.1): " VERSION

if [[ -z "$VERSION" ]]; then
  echo "❌ Version number cannot be empty."
  exit 1
fi

RELEASE_NAME="RioWebCLI-v$VERSION"
RELEASE_DIR="../releases"
RELEASE_ZIP="$RELEASE_DIR/$RELEASE_NAME.zip"

# Make sure the release directory exists
mkdir -p "$RELEASE_DIR"

echo "📦 Building $RELEASE_NAME.zip with submodule..."

# Clean up old zips if they exist
rm -f "$RELEASE_ZIP" pyRio.zip

# Archive main project
git archive --format=zip HEAD -o "$RELEASE_ZIP"

# Archive submodule with proper folder structure
cd pyRio
git archive --format=zip --prefix=pyRio/ HEAD -o "../pyRio.zip"
cd ..

# Merge submodule into final zip
mkdir -p temp_pyRio
unzip -q pyRio.zip -d temp_pyRio
cd temp_pyRio
zip -ur "$RELEASE_ZIP" .
cd ..
rm -rf temp_pyRio pyRio.zip

echo "✅ Done! Created $RELEASE_ZIP with pyRio/ included."