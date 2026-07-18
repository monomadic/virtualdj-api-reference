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

# ---------------------------------------------------------------------------
# Lossless probes: is AAC required, or do ALAC/FLAC variants work?
# ---------------------------------------------------------------------------
print "→ Building DIAG-standalone-alac.m4a (ALAC: stems s16p, master s32p)…"
for s in kick instruments vocal bass hihat; do
  ffmpeg -y -loglevel error -i "$W/$s.wav" -c:a alac -sample_fmt s16p "$W/$s.alac.m4a"
done
ffmpeg -y -loglevel error -i "$W/noise.wav" -c:a alac -sample_fmt s32p "$W/mixed.alac.m4a"
ffmpeg -y -loglevel error \
  -i "$W/kick.alac.m4a" -i "$W/instruments.alac.m4a" -i "$W/vocal.alac.m4a" \
  -i "$W/bass.alac.m4a" -i "$W/hihat.alac.m4a" -i "$W/mixed.alac.m4a" \
  -map 5:a -map 2:a -map 4:a -map 3:a -map 1:a -map 0:a \
  -c:a copy \
  -disposition:a:0 default -disposition:a:1 0 -disposition:a:2 0 \
  -disposition:a:3 0 -disposition:a:4 0 -disposition:a:5 0 \
  -metadata title="virtualdj" -metadata artist="output" \
  -brand isom \
  "$W/standalone-alac.m4a"
MP4Box \
  -udta "1:type=name" -udta "1:type=name:str=mixed track" \
  -udta "2:type=name" -udta "2:type=name:str=vocal" \
  -udta "3:type=name" -udta "3:type=name:str=hihat" \
  -udta "4:type=name" -udta "4:type=name:str=bass" \
  -udta "5:type=name" -udta "5:type=name:str=instruments" \
  -udta "6:type=name" -udta "6:type=name:str=kick" \
  -itags "$W/itags.txt" \
  -flat -brand isom:512 -rb mp42 -ab mp41 \
  -out "$OUT/DIAG-standalone-alac.m4a" "$W/standalone-alac.m4a" >/dev/null 2>&1
print "  ✓ $OUT/DIAG-standalone-alac.m4a"

# Sidecars with lossless codecs (each next to its own noise original,
# both stamped — the stamp gate is already proven, so codec is the only
# variable here)
make_lossless_sidecar() {  # make_lossless_sidecar BASENAME CODEC_ARGS...
  local base="$1"; shift
  ffmpeg -y -loglevel error -i "$W/noise.wav" -c:a flac "$OUT/$base.flac"
  ffmpeg -y -loglevel error \
    -i "$W/vocal.wav" -i "$W/hihat.wav" -i "$W/bass.wav" \
    -i "$W/instruments.wav" -i "$W/kick.wav" \
    -map 0:a -map 1:a -map 2:a -map 3:a -map 4:a \
    "$@" -ar 44100 -ac 2 \
    -disposition:a:0 0 -disposition:a:1 0 -disposition:a:2 0 \
    -disposition:a:3 0 -disposition:a:4 0 \
    -metadata:s:a:0 title="vocal" \
    -metadata:s:a:1 title="hihat" \
    -metadata:s:a:2 title="bass" \
    -metadata:s:a:3 title="instruments" \
    -metadata:s:a:4 title="kick" \
    -f matroska "$OUT/$base.flac.vdjstems"
  mkvpropedit "$OUT/$base.flac.vdjstems" --edit info \
    --set "writing-application=VirtualDJ 2026.9336.stems2" >/dev/null
}

if command -v mkvpropedit >/dev/null 2>&1; then
  print "→ Building lossless sidecar probes…"
  make_lossless_sidecar "DIAG-sidecar-alac" -c:a alac -sample_fmt s16p
  print "  ✓ DIAG-sidecar-alac (ALAC streams, stamped)"
  make_lossless_sidecar "DIAG-sidecar-flac" -c:a flac
  print "  ✓ DIAG-sidecar-flac (FLAC streams, stamped)"
else
  print "  ⚠ mkvpropedit missing — lossless sidecar probes skipped" >&2
fi

# All-s16p ALAC standalone: isolates whether the s32p master (not ALAC
# itself) is what breaks VDJ's standalone ALAC playback.
print "→ Building DIAG-standalone-alac16.m4a (ALAC, ALL streams s16p)…"
ffmpeg -y -loglevel error -i "$W/noise.wav" -c:a alac -sample_fmt s16p "$W/mixed16.alac.m4a"
ffmpeg -y -loglevel error \
  -i "$W/kick.alac.m4a" -i "$W/instruments.alac.m4a" -i "$W/vocal.alac.m4a" \
  -i "$W/bass.alac.m4a" -i "$W/hihat.alac.m4a" -i "$W/mixed16.alac.m4a" \
  -map 5:a -map 2:a -map 4:a -map 3:a -map 1:a -map 0:a \
  -c:a copy \
  -disposition:a:0 default -disposition:a:1 0 -disposition:a:2 0 \
  -disposition:a:3 0 -disposition:a:4 0 -disposition:a:5 0 \
  -metadata title="virtualdj" -metadata artist="output" \
  -brand isom \
  "$W/standalone-alac16.m4a"
MP4Box \
  -udta "1:type=name" -udta "1:type=name:str=mixed track" \
  -udta "2:type=name" -udta "2:type=name:str=vocal" \
  -udta "3:type=name" -udta "3:type=name:str=hihat" \
  -udta "4:type=name" -udta "4:type=name:str=bass" \
  -udta "5:type=name" -udta "5:type=name:str=instruments" \
  -udta "6:type=name" -udta "6:type=name:str=kick" \
  -itags "$W/itags.txt" \
  -flat -brand isom:512 -rb mp42 -ab mp41 \
  -out "$OUT/DIAG-standalone-alac16.m4a" "$W/standalone-alac16.m4a" >/dev/null 2>&1
print "  ✓ $OUT/DIAG-standalone-alac16.m4a"

# ---------------------------------------------------------------------------
# Edge-case probes — one variable each; results recorded in the acceptance
# matrix of docs/Stem File Format.md (all passed, 2026-07-18)
# ---------------------------------------------------------------------------
if command -v mkvpropedit >/dev/null 2>&1; then
  print "→ Building task-8 probes…"

  # Q1: PCM streams in a sidecar
  make_lossless_sidecar "DIAG-sidecar-pcm" -c:a pcm_s16le
  print "  ✓ DIAG-sidecar-pcm (pcm_s16le streams)"

  # Q2: 24-bit FLAC sidecar (16-bit-only limit container-wide or not?)
  make_lossless_sidecar "DIAG-sidecar-flac24" -c:a flac -sample_fmt s32
  print "  ✓ DIAG-sidecar-flac24 (24-bit FLAC streams)"

  # Q3: old writing-application version string
  make_sidecar "DIAG-sidecar-oldver"
  mkvpropedit "$OUT/DIAG-sidecar-oldver.flac.vdjstems" --edit info \
    --set "writing-application=VirtualDJ 2025.8800.stems2" >/dev/null
  print "  ✓ DIAG-sidecar-oldver (stamped VirtualDJ 2025.8800.stems2)"

  # Q4: capitalized role titles
  ffmpeg -y -loglevel error -i "$W/noise.wav" -c:a flac "$OUT/DIAG-sidecar-case.flac"
  ffmpeg -y -loglevel error \
    -i "$W/vocal.wav" -i "$W/hihat.wav" -i "$W/bass.wav" \
    -i "$W/instruments.wav" -i "$W/kick.wav" \
    -map 0:a -map 1:a -map 2:a -map 3:a -map 4:a \
    -c:a aac -b:a 320k -ar 44100 -ac 2 \
    -disposition:a:0 0 -disposition:a:1 0 -disposition:a:2 0 \
    -disposition:a:3 0 -disposition:a:4 0 \
    -metadata:s:a:0 title="Vocal" \
    -metadata:s:a:1 title="Hihat" \
    -metadata:s:a:2 title="Bass" \
    -metadata:s:a:3 title="Instruments" \
    -metadata:s:a:4 title="Kick" \
    -f matroska "$OUT/DIAG-sidecar-case.flac.vdjstems"
  mkvpropedit "$OUT/DIAG-sidecar-case.flac.vdjstems" --edit info \
    --set "writing-application=VirtualDJ 2026.9336.stems2" >/dev/null
  print "  ✓ DIAG-sidecar-case (titles Vocal/Hihat/Bass/Instruments/Kick)"
fi

# Q5: FLAC-in-MP4 standalone
print "→ Building DIAG-standalone-flacmp4.m4a…"
for s in kick instruments vocal bass hihat; do
  ffmpeg -y -loglevel error -i "$W/$s.wav" -c:a flac -strict experimental -f mp4 "$W/$s.flac.mp4"
done
ffmpeg -y -loglevel error -i "$W/noise.wav" -c:a flac -strict experimental -f mp4 "$W/mixedf.flac.mp4"
if ffmpeg -y -loglevel error \
  -i "$W/kick.flac.mp4" -i "$W/instruments.flac.mp4" -i "$W/vocal.flac.mp4" \
  -i "$W/bass.flac.mp4" -i "$W/hihat.flac.mp4" -i "$W/mixedf.flac.mp4" \
  -map 5:a -map 2:a -map 4:a -map 3:a -map 1:a -map 0:a \
  -c:a copy -strict experimental \
  -disposition:a:0 default -disposition:a:1 0 -disposition:a:2 0 \
  -disposition:a:3 0 -disposition:a:4 0 -disposition:a:5 0 \
  -metadata title="virtualdj" -metadata artist="output" \
  -brand isom \
  -f mp4 "$W/standalone-flac.m4a" 2>/dev/null; then
  MP4Box \
    -udta "1:type=name" -udta "1:type=name:str=mixed track" \
    -udta "2:type=name" -udta "2:type=name:str=vocal" \
    -udta "3:type=name" -udta "3:type=name:str=hihat" \
    -udta "4:type=name" -udta "4:type=name:str=bass" \
    -udta "5:type=name" -udta "5:type=name:str=instruments" \
    -udta "6:type=name" -udta "6:type=name:str=kick" \
    -itags "$W/itags.txt" \
    -flat -brand isom:512 -rb mp42 -ab mp41 \
    -out "$OUT/DIAG-standalone-flacmp4.m4a" "$W/standalone-flac.m4a" >/dev/null 2>&1 \
    && print "  ✓ $OUT/DIAG-standalone-flacmp4.m4a" \
    || print "  ⚠ MP4Box could not process FLAC-in-MP4 — probe skipped" >&2
else
  print "  ⚠ ffmpeg could not mux FLAC into MP4 — probe skipped" >&2
fi

print "\nListening key: noise=master · 100Hz=kick/Drums · 200Hz=bass · 400Hz=vocal · 800Hz=instruments · 1600Hz=hihat"
print "Files in: $OUT"
