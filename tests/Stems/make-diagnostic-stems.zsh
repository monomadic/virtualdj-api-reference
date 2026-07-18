#!/usr/bin/env zsh
# ============================================================================
# make-diagnostic-stems.zsh — audible probe files for VirtualDJ stem routing
# ============================================================================
#
# Generates stem files where every stream is acoustically unique, so listening
# in VirtualDJ reveals exactly which stream is routed where:
#
#   Stream        Content            How to identify by ear
#   master/orig   white noise        hiss, no pitch
#   kick          100 Hz sine        low thump ladder …
#   bass          200 Hz sine
#   vocal         400 Hz sine
#   instruments   800 Hz sine
#   hihat         1600 Hz sine       … top of the ladder
#
# The master is deliberately NOT the sum of the stems: the moment VirtualDJ
# switches from master to stem playback you hear noise being replaced by
# tones. Muting one stem pad removes exactly one tone — which tone disappears
# tells you the pad→stream mapping.
#
# Outputs (into TARGET_DIR, default ~/Music/Stems/vdj-diagnostic):
#   DIAG-standalone.m4a               6-stream M4A per the working 2026 recipe
#   DIAG-sidecar-stamped.flac         noise "original" (44.1 kHz)
#   DIAG-sidecar-stamped.flac.vdjstems    Matroska sidecar, VirtualDJ
#                                         writing-application stamp applied
#   DIAG-sidecar-unstamped.flac       second noise original
#   DIAG-sidecar-unstamped.flac.vdjstems  identical sidecar but Lavf
#                                         writing-application (A/B probe)
#
# Dependencies: ffmpeg, MP4Box; mkvpropedit for the stamped sidecar
# See docs/Stem File Format.md for the format contracts under test.
# ============================================================================
set -euo pipefail

OUT="${1:-$HOME/Music/Stems/vdj-diagnostic}"
DUR=60
mkdir -p "$OUT"
W="$(mktemp -d)"
trap "rm -rf '$W'" EXIT

typeset -A FREQ
FREQ=(kick 100 bass 200 vocal 400 instruments 800 hihat 1600)

print "→ Generating tones (${DUR}s)…"
for stem freq in "${(@kv)FREQ}"; do
  ffmpeg -y -loglevel error -f lavfi -i "sine=frequency=${freq}:duration=${DUR}" \
    -af "volume=-12dB" -ac 2 -ar 44100 -c:a pcm_s16le "$W/$stem.wav"
done
ffmpeg -y -loglevel error -f lavfi -i "anoisesrc=color=white:duration=${DUR}:seed=1" \
  -af "volume=-20dB" -ac 2 -ar 44100 -c:a pcm_s16le "$W/noise.wav"

# ---------------------------------------------------------------------------
# Standalone M4A (working 2026 recipe): master = NOISE, not the stem sum
# ---------------------------------------------------------------------------
print "→ Building DIAG-standalone.m4a…"
for s in kick instruments vocal bass hihat; do
  ffmpeg -y -loglevel error -i "$W/$s.wav" -c:a aac -b:a 320k "$W/$s.aac"
done
ffmpeg -y -loglevel error -i "$W/noise.wav" -c:a aac -b:a 320k "$W/mixed.aac"

ffmpeg -y -loglevel error \
  -i "$W/kick.aac" -i "$W/instruments.aac" -i "$W/vocal.aac" \
  -i "$W/bass.aac" -i "$W/hihat.aac" -i "$W/mixed.aac" \
  -map 5:a -map 2:a -map 4:a -map 3:a -map 1:a -map 0:a \
  -c:a copy \
  -disposition:a:0 default -disposition:a:1 0 -disposition:a:2 0 \
  -disposition:a:3 0 -disposition:a:4 0 -disposition:a:5 0 \
  -metadata title="virtualdj" -metadata artist="output" \
  -brand isom \
  "$W/standalone.m4a"

cat > "$W/itags.txt" <<EOF
tool=VirtualDJ 2023.7544
created=0
tempo=120
rate=0
EOF
MP4Box \
  -udta "1:type=name" -udta "1:type=name:str=mixed track" \
  -udta "2:type=name" -udta "2:type=name:str=vocal" \
  -udta "3:type=name" -udta "3:type=name:str=hihat" \
  -udta "4:type=name" -udta "4:type=name:str=bass" \
  -udta "5:type=name" -udta "5:type=name:str=instruments" \
  -udta "6:type=name" -udta "6:type=name:str=kick" \
  -itags "$W/itags.txt" \
  -flat -brand isom:512 -rb mp42 -ab mp41 \
  -out "$OUT/DIAG-standalone.m4a" "$W/standalone.m4a" >/dev/null 2>&1
print "  ✓ $OUT/DIAG-standalone.m4a"

# ---------------------------------------------------------------------------
# Sidecar pairs: noise "original" + Matroska sidecar of tones
# ---------------------------------------------------------------------------
make_sidecar() {  # make_sidecar BASENAME
  local base="$1"
  ffmpeg -y -loglevel error -i "$W/noise.wav" -c:a flac "$OUT/$base.flac"
  ffmpeg -y -loglevel error \
    -i "$W/vocal.wav" -i "$W/hihat.wav" -i "$W/bass.wav" \
    -i "$W/instruments.wav" -i "$W/kick.wav" \
    -map 0:a -map 1:a -map 2:a -map 3:a -map 4:a \
    -c:a aac -b:a 320k -ar 44100 -ac 2 \
    -disposition:a:0 0 -disposition:a:1 0 -disposition:a:2 0 \
    -disposition:a:3 0 -disposition:a:4 0 \
    -metadata:s:a:0 title="vocal" \
    -metadata:s:a:1 title="hihat" \
    -metadata:s:a:2 title="bass" \
    -metadata:s:a:3 title="instruments" \
    -metadata:s:a:4 title="kick" \
    -f matroska "$OUT/$base.flac.vdjstems"
}

print "→ Building sidecar pairs…"
make_sidecar "DIAG-sidecar-stamped"
if command -v mkvpropedit >/dev/null 2>&1; then
  mkvpropedit "$OUT/DIAG-sidecar-stamped.flac.vdjstems" --edit info \
    --set "writing-application=VirtualDJ 2026.9336.stems2" >/dev/null
  print "  ✓ DIAG-sidecar-stamped (writing-application=VirtualDJ 2026.9336.stems2)"
else
  print "  ⚠ mkvpropedit missing — stamped variant NOT stamped" >&2
fi
make_sidecar "DIAG-sidecar-unstamped"
print "  ✓ DIAG-sidecar-unstamped (writing-application=Lavf, control)"

# ---------------------------------------------------------------------------
# 4-stem M4A variant (historical naming: All, Vocal, Instrument, Bass, Drums)
# Master ("All") = noise; probes whether the 4-stem title family still works.
# ---------------------------------------------------------------------------
print "→ Building DIAG-4stem.m4a…"
ffmpeg -y -loglevel error \
  -i "$W/mixed.aac" -i "$W/vocal.aac" -i "$W/instruments.aac" \
  -i "$W/bass.aac" -i "$W/kick.aac" \
  -map 0:a -map 1:a -map 2:a -map 3:a -map 4:a \
  -c:a copy \
  -disposition:a:0 default -disposition:a:1 0 -disposition:a:2 0 \
  -disposition:a:3 0 -disposition:a:4 0 \
  -metadata title="virtualdj" -metadata artist="output" \
  -brand isom \
  "$W/fourstem.m4a"
MP4Box \
  -udta "1:type=name" -udta "1:type=name:str=All" \
  -udta "2:type=name" -udta "2:type=name:str=Vocal" \
  -udta "3:type=name" -udta "3:type=name:str=Instrument" \
  -udta "4:type=name" -udta "4:type=name:str=Bass" \
  -udta "5:type=name" -udta "5:type=name:str=Drums" \
  -itags "$W/itags.txt" \
  -flat -brand isom:512 -rb mp42 -ab mp41 \
  -out "$OUT/DIAG-4stem.m4a" "$W/fourstem.m4a" >/dev/null 2>&1
print "  ✓ $OUT/DIAG-4stem.m4a (Drums tone = 100 Hz kick source)"

print "\nListening key: noise=master · 100Hz=kick/Drums · 200Hz=bass · 400Hz=vocal · 800Hz=instruments · 1600Hz=hihat"
print "Files in: $OUT"
