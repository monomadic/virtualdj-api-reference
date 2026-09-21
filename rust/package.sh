#!/bin/zsh
# Package a Rust plugin crate as a VirtualDJ .bundle (and optionally install it).
#
#   rust/package.sh tremolo              # build rust/bundle/RustTremolo.bundle
#   rust/package.sh tremolo --install    # …and copy it into VirtualDJ's plugin folder
#
# Mirrors the proven recipe in tools/plugin/build.sh: a true MH_BUNDLE image
# (clang -bundle over the staticlib — the exact load format the C++ instrument
# verified loadable), an ad-hoc code signature (sufficient because VirtualDJ
# ships com.apple.security.cs.disable-library-validation), and a
# DllGetClassObject export check before anything is installed.
set -eu -o pipefail

HERE="${0:a:h}"

# Registry: example name -> cargo package, bundle name, VirtualDJ subfolder.
case "${1-}" in
    tremolo)
        PKG=vdj-rust-tremolo
        LIB=libvdj_rust_tremolo.a
        NAME=RustTremolo
        SUBDIR_DEFAULT=SoundEffect
        ;;
    *)
        print -u2 "usage: package.sh <tremolo> [--install]"
        exit 2
        ;;
esac
shift

SUBDIR="${VDJ_PLUGIN_SUBDIR-$SUBDIR_DEFAULT}"
BUNDLE="$HERE/bundle/$NAME.bundle"
PLUGIN_DIR="$HOME/Library/Application Support/VirtualDJ/PluginsMacArm"

cargo build --release --manifest-path "$HERE/Cargo.toml" -p "$PKG"

rm -rf "$BUNDLE"
mkdir -p "$BUNDLE/Contents/MacOS"

cat > "$BUNDLE/Contents/Info.plist" <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>CFBundleDevelopmentRegion</key>
	<string>en</string>
	<key>CFBundleExecutable</key>
	<string>$NAME</string>
	<key>CFBundleIdentifier</key>
	<string>local.vdj-plugin.${NAME:l}</string>
	<key>CFBundleInfoDictionaryVersion</key>
	<string>6.0</string>
	<key>CFBundleName</key>
	<string>$NAME</string>
	<key>CFBundlePackageType</key>
	<string>BNDL</string>
	<key>CFBundleShortVersionString</key>
	<string>0.1.0</string>
	<key>CFBundleSupportedPlatforms</key>
	<array>
		<string>MacOSX</string>
	</array>
	<key>CFBundleVersion</key>
	<string>1</string>
	<key>LSMinimumSystemVersion</key>
	<string>10.14</string>
</dict>
</plist>
PLIST

# -u forces the archive member holding DllGetClassObject to be pulled in;
# -exported_symbol hides everything else, matching -fvisibility=hidden builds.
# No -mmacosx-version-min: the staticlib's objects carry the Rust toolchain's
# own deployment target, and forcing an older one only produces ld warnings.
clang \
    -arch arm64 \
    -bundle \
    -u _DllGetClassObject \
    -Wl,-exported_symbol,_DllGetClassObject \
    "$HERE/target/release/$LIB" \
    -o "$BUNDLE/Contents/MacOS/$NAME"

codesign --force --sign - --timestamp=none "$BUNDLE"
codesign --verify --verbose=1 "$BUNDLE"

print "built: $BUNDLE"
nm -gU "$BUNDLE/Contents/MacOS/$NAME" | grep -q DllGetClassObject || {
    print -u2 "error: DllGetClassObject not exported"; exit 1
}
file "$BUNDLE/Contents/MacOS/$NAME"

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
