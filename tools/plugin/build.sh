#!/bin/zsh
# Build (and optionally install) the read-only VDJIntrospect plugin bundle.
#
#   tools/plugin/build.sh            # build to build/VDJIntrospect.bundle
#   tools/plugin/build.sh --install  # build, then copy into VirtualDJ's plugin folder
#   tools/plugin/build.sh --dsp      # the Sound Effect variant
#   tools/plugin/build.sh --skin     # Sound Effect + custom skin interface
#
# Needs the Atomix SDK headers, which this repo does not vendor. Put a copy under
# vendor/ (see .gitignore and docs/Plugin SDK.md); any directory containing
# vdjPlugin8.h works, or point VDJ_SDK at one.
#
# Xcode is NOT required — Command Line Tools clang++ builds this. Xcode's own
# toolchain works too if it happens to be selected.
set -eu -o pipefail

REPO="${0:a:h:h:h}"
NAME="VDJIntrospect"
DEFINES=()
# --dsp builds the Sound Effect variant instead of the headless AutoStart probe.
# It installs into SoundEffect/ so VirtualDJ files it under Extensions > Effects:
# the Extensions list is organised by functional type, and a plugin that is no
# recognised type is loaded but never listed.
if [[ " $* " == *" --dsp "* ]]; then
    NAME="VDJIntrospectFX"
    DEFINES=(-DVDJINTROSPECT_DSP)
    SUBDIR_DEFAULT="SoundEffect"
fi
# --skin is the DSP build plus a custom skin interface: the effect answers
# OnGetUserInterface with VDJINTERFACE_SKIN and serves skin.xml/skin.png from the
# working dir. Separate bundle NAME because the bundle filename is the plugin's
# identity to VirtualDJ, not the declared PluginName — so this can sit beside the
# plain FX build and be told apart in the effects list.
if [[ " $* " == *" --skin "* ]]; then
    NAME="VDJIntrospectSkin"
    DEFINES=(-DVDJINTROSPECT_DSP -DVDJINTROSPECT_SKIN)
    SUBDIR_DEFAULT="SoundEffect"
fi
BUILD="$REPO/build"
BUNDLE="$BUILD/$NAME.bundle"
PLUGIN_DIR="$HOME/Library/Application Support/VirtualDJ/PluginsMacArm"
# AutoStart is where VirtualDJ's own non-effect plugins live (Ableton Link,
# Network Control). Which folder actually loads a basic/start-stop plugin is one
# of the things this build settles; override with VDJ_PLUGIN_SUBDIR= to retry
# elsewhere without editing this script.
SUBDIR="${VDJ_PLUGIN_SUBDIR-${SUBDIR_DEFAULT-AutoStart}}"

SDK="${VDJ_SDK-}"
if [[ -z "$SDK" ]]; then
    # The DSP build needs vdjDsp8.h beside vdjPlugin8.h, so anchor on whichever
    # header this variant actually requires.
    ANCHOR=vdjPlugin8.h
    [[ -n "${DEFINES[*]}" ]] && ANCHOR=vdjDsp8.h
    SDK="$(find "$REPO/vendor" -name "$ANCHOR" -print -quit 2>/dev/null || true)"
    SDK="${SDK:h}"
fi
if [[ -z "$SDK" || ! -f "$SDK/vdjPlugin8.h" ]]; then
    print -u2 "error: vdjPlugin8.h not found. Put the SDK headers under vendor/ or set VDJ_SDK=<dir>."
    print -u2 "       https://www.virtualdj.com/wiki/PluginSDK8.html"
    exit 1
fi
print "SDK headers: $SDK"

rm -rf "$BUNDLE"
mkdir -p "$BUNDLE/Contents/MacOS"
sed "s/VDJIntrospect/$NAME/g" "$REPO/tools/plugin/Info.plist" > "$BUNDLE/Contents/Info.plist"

clang++ \
    -std=c++17 \
    -arch arm64 \
    -mmacosx-version-min=10.14 \
    -bundle \
    -fvisibility=hidden \
    -O2 \
    -Wall \
    -I "$SDK" \
    "${DEFINES[@]}" \
    -framework CoreFoundation \
    "$REPO/tools/plugin/VDJIntrospect.cpp" \
    -o "$BUNDLE/Contents/MacOS/$NAME"

# Ad-hoc signature. VirtualDJ carries com.apple.security.cs.disable-library-validation,
# so an ad-hoc signed bundle is loadable; without any signature at all, arm64 macOS
# would reject the image outright.
codesign --force --sign - --timestamp=none "$BUNDLE"
codesign --verify --verbose=1 "$BUNDLE"

print "built: $BUNDLE"
nm -gU "$BUNDLE/Contents/MacOS/$NAME" | grep DllGetClassObject || {
    print -u2 "error: DllGetClassObject not exported"; exit 1
}

# Flags may arrive in any order (`--dsp --install`), so scan all of them.
if [[ " $* " == *" --install "* ]]; then
    if [[ ! -d "$PLUGIN_DIR" ]]; then
        print -u2 "error: $PLUGIN_DIR does not exist"
        exit 1
    fi
    DEST="$PLUGIN_DIR/$SUBDIR"
    mkdir -p "$DEST"
    rm -rf "$DEST/$NAME.bundle"
    cp -R "$BUNDLE" "$DEST/"
    print "installed: $DEST/$NAME.bundle"
    print "Restart VirtualDJ to load it (editing a loaded bundle is not picked up live)."
fi
