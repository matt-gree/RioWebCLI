#!/bin/bash
set -e

# GitHub repo in format: user/repo
GITHUB_REPO="matt-gree/RioWebCLI"

# Get the latest release version
echo "🔍 Checking latest release on GitHub..."
LATEST_VERSION=$(curl -s "https://api.github.com/repos/$GITHUB_REPO/releases/latest" | sed -n 's/.*"tag_name": "\(.*\)".*/\1/p')

echo "📌 Latest GitHub release: ${LATEST_VERSION:-No releases yet}"

# Prompt for new version
read -p "📝 Enter new version number (e.g., 1.0.1): " VERSION

if [[ -z "$VERSION" ]]; then
  echo "❌ Version number cannot be empty."
  exit 1
fi

RELEASE_NAME="RioWebCLI-v$VERSION"

echo "📦 Building $RELEASE_NAME.zip with submodule..."

rm -f "$RELEASE_NAME.zip" pyRio.zip

# Archive main project
git archive --format=zip HEAD -o "$RELEASE_NAME.zip"

# Archive submodule with correct folder structure
cd pyRio
git archive --format=zip --prefix=pyRio/ HEAD -o "../pyRio.zip"
cd ..

# Merge submodule contents into main zip
mkdir -p temp_pyRio
unzip -q pyRio.zip -d temp_pyRio
cd temp_pyRio
zip -ur "../$RELEASE_NAME.zip" .
cd ..
rm -rf temp_pyRio pyRio.zip

echo "✅ Done! Created $RELEASE_NAME.zip with pyRio/ included."