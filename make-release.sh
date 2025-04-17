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

# Create ./releases directory inside project
RELEASE_DIR="$(pwd)/releases"
mkdir -p "$RELEASE_DIR"

FINAL_ZIP="$RELEASE_DIR/$RELEASE_NAME.zip"
TEMP_ZIP="$RELEASE_NAME-temp.zip"

echo "📦 Building $RELEASE_NAME.zip with pyRio/ submodule..."

# Clean up old zips
rm -f "$TEMP_ZIP" pyRio.zip "$FINAL_ZIP"

# Archive main project
git archive --format=zip HEAD -o "$TEMP_ZIP"

# Archive submodule with correct structure
cd pyRio
git archive --format=zip --prefix=pyRio/ HEAD -o "../pyRio.zip"
cd ..

# Merge submodule into main zip
mkdir -p temp_pyRio
unzip -q pyRio.zip -d temp_pyRio
cd temp_pyRio
zip -ur "../$TEMP_ZIP" .
cd ..
rm -rf temp_pyRio pyRio.zip

# Move final zip into ./releases/
echo "📁 Moving final zip to: $FINAL_ZIP"
mv "$TEMP_ZIP" "$FINAL_ZIP"

# Final confirmation
echo "✅ Done! Created release:"
ls -lh "$FINAL_ZIP"