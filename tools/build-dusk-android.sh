#!/usr/bin/env bash
# Build an installable Dusk.apk (Capacitor + Gradle).
# Optional env: DUSK_KEYSTORE (+ password/alias) for a stable release signature.
# Without a keystore, signs with a CI-local key so the APK installs on phones.
set -euo pipefail
cd "$(dirname "$0")/.."

export ELECTRON_SKIP_BINARY_DOWNLOAD=1

npm ci --no-audit --no-fund
node tools/build-locales.mjs
node mobile/build.mjs
npx cap sync android

VERSION="$(node -p "require('./package.json').version")"
export DUSK_VERSION_NAME="${DUSK_VERSION_NAME:-$VERSION}"
export DUSK_VERSION_CODE="${DUSK_VERSION_CODE:-${GITHUB_RUN_NUMBER:-1}}"

if [[ -z "${DUSK_KEYSTORE:-}" ]]; then
  KS="$PWD/android/.dusk-ci.jks"
  if [[ ! -f "$KS" ]]; then
    keytool -genkeypair -v \
      -keystore "$KS" \
      -storepass duskci \
      -keypass duskci \
      -alias dusk \
      -keyalg RSA -keysize 2048 -validity 10000 \
      -dname "CN=Dusk Music, OU=zxypablo11, O=zxypablo11, L=Internet, ST=NA, C=DE"
  fi
  export DUSK_KEYSTORE="$KS"
  export DUSK_KEYSTORE_PASSWORD=duskci
  export DUSK_KEY_PASSWORD=duskci
  export DUSK_KEY_ALIAS=dusk
fi

cd android
chmod +x gradlew
./gradlew assembleRelease --no-daemon
mkdir -p ../dist
cp app/build/outputs/apk/release/app-release.apk ../dist/Dusk.apk
ls -lh ../dist/Dusk.apk
echo "APK ready: dist/Dusk.apk"
