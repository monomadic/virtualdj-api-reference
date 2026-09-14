# Compiled Controller Definitions

`controllers.dat` is an encrypted ZIP container containing the original XML, including
comments and formatting. It is not a serialized tree requiring reconstruction into an
approximation of the device schema. The reader emits every member byte-for-byte.

## Read and query

```sh
just controllers-vendor        # decode the installed build into gitignored vendor/controllers/<key>/, verified against its manifest
just controllers-archives      # every archive with a committed manifest, and which are decoded here
just controllers-diff 18.0.9583 18.0.9598   # added / removed / changed members between two builds, from manifests alone
just script-corpus --verb effect_arm_select   # the factory mappings are a corpus source (`factory`)
just attested-tails --verb effect_arm_select  # tails and shapes Atomix wrote into them
just controllers-extract --output-dir /tmp/vdj-controllers --json /tmp/manifest.json   # ad-hoc decode, any layout
python3 tools/controller_schema_inventory.py /tmp/vdj-controllers/block-000.zip --output tests/controller-schema-inventory.json
just controllers
just controllers --device DDJGRV6
just controllers --path /device/settings
just controllers --path /device/slider
```

`just controllers-vendor` is the extraction the corpus tools read: `vendor/` is gitignored
because the decoded files are Atomix's copyright (the same reason the plugin SDK headers are
not committed), and `tools/extract_script_corpus.py` refuses a tree whose files do not match
its manifest's hashes, so an extraction from another build cannot attest anything under this
build's stamp.

**One archive, one key, one record.** An archive is named by the app build it shipped in
*and* its own final block revision — `18.0.9598-r2241` — because `controllers.dat` carries a
revision chain of its own (`blocks[].predecessor` → `revision`) and can move independently of
the bundle. The decoded tree lives at `vendor/controllers/<key>/` and its manifest at
[`tests/controllers-manifests/<key>.json`](../tests/controllers-manifests/); the helper that
derives the key and lists what is known is `tools/controller_archives.py`. Decoding on a new
build therefore *adds* a manifest instead of replacing the last one, and an existing key is
verified, never overwritten. Because a manifest carries a SHA-256, byte count and root
attributes per member, `just controllers-diff A B` compares two builds' archives on a machine
that has never held either tree; what changed *inside* a member needs both trees decoded, and
`--show-paths` names the pair. The corpus artifact stamps the archive it mined as
`summary.factory_archive`, and `--check` re-verifies that archive rather than whichever is
installed: on a machine holding a different build it reports the mismatch and skips, the same
way the skin-reader check does, instead of failing. To re-anchor the corpus to the installed
build, run `just controllers-vendor` and then `just script-corpus > tests/vdjscript-corpus.json`.

Extraction uses `uv` and the reader's pinned `pycryptodome` dependency. Offline inventory
queries need only Python's standard library. The output directory must not already exist;
no app files are changed. `--app` selects another bundle, `--input` a separate data file.
Each archive block gets its own directory and ZIP: no members are silently overwritten.
The reader rejects unsafe paths, duplicate names (case-insensitively), unexpected XML
roots, bad CRCs, invalid key envelopes, truncation, and broken block chains.

Manifest fields (`tests/controllers-manifests/<key>.json`) `roots`, `blocks[].member_count`,
`source_sha256`, and `bundle_version` answer counts and identify the exact input.
[Inventory](../tests/controller-schema-inventory.json) fields `paths`, `device_types`, and
`local_mapper_comparisons` expose the recovered vocabulary and reference comparisons.
Do not copy their totals into prose. Large recovered vendor files remain generated output,
not a second hand-maintained reference corpus.

## Container layout

Source: **Tier 2**, unstripped bundle **18.0.9246, x86_64** loader disassembly. The same
reader successfully decoded and CRC/XML-validated the **18.0.9598** bundle. Cryptographic
and structural validation is evidence of faithful extraction, not of hardware behavior.
The [loader excerpts and source hashes](../tests/controllers/loader-evidence/source.json)
identify the historical code used to recover the format.

Each block begins with three little-endian unsigned 32-bit words:

- Offset `0`: logical ZIP length `N` after decryption.
- Offset `4`: predecessor revision; the first block expects zero.
- Offset `8`: this block's revision, used to link the next block.
- Offset `12`: RSA envelope, `128` bytes.
- Offset `140`: Blowfish ECB ciphertext, `(N & ~7) + 8` bytes.

The next block starts at `offset + (N & ~7) + 0x94`. The loader's revision comparison
and stride were traced in `CControllersRepository::init`. Current sampled bundle files
have one block; synthetic tests exercise chained blocks. This reader preserves separate
blocks rather than claiming to reproduce every app-level override/merge rule.

`CControllersRepository::openEncryptedZip` applies RSA public recovery with PKCS#1
**type-1** padding. The recovered payload starts with ASCII `VDJ`; the remaining bytes
are the Blowfish key. This is public-key recovery, not a private-key or account credential.
The public modulus is embedded in the executable and the reader checks its presence in
the selected app. Key rotation fails explicitly. The key never needs to be printed or saved.
`CZip::openEncrypted` initializes Blowfish; `encrypted_zread` decrypts independent eight-byte
blocks with `BF_ecb_encrypt(..., BF_DECRYPT)`. Only the first `N` plaintext bytes belong to
the ZIP. Padding is not interpreted as PKCS#7.

## What the container adds to the schema summary

The archive has independent `<device>`, `<mapper>`, and `<audio>` documents. Device XML
contains MIDI/HID hardware definitions; mapper XML contains actions and control bindings.
Some device documents are empty placeholders. Preserve those and exact shipped spellings;
do not invent missing types/names or silently fix vendor typos.

The inventory compares vocabulary to the explicit summary in [Mapper XML](Mapper%20XML.md),
not to a complete normative XSD. The official
[MIDI page](https://www.virtualdj.com/wiki/ControllerDefinitionMIDI) and
[HID page](https://virtualdj.com/wiki/ControllerDefinitionHIDv8.html) were also checked on
2026-09-12: the literal syntax terms `settings`, `onchange`, `group`, `imagesysex`, `pitchout`,
and `packetdata` were absent from those two retrieved pages. This is a scoped documentation
gap, not a claim that Atomix has never documented them elsewhere.

Examples recovered from the bundle (**Tier 2; behavior untested unless separately noted**):

- `AKAI APC64.xml`: `<settings>` contains setting-named children, including an
  `AfterTouchVelocity` entry with `values`, `default`, and
  `onchange="sampler_volume 'all' 100"`. The old blanket claim that definitions contain no
  VDJScript is too broad. This proves the presence of callback text, not its execution.
- `Alpha Theta DDJ-GRV6.xml`: device settings, `brand`, `category`, `vendor`, `mixerorder`,
  `threadmodeoutput`, and `eq` metadata beyond the local root summary.
- `AllenHeath XONEK2.xml`: conditional `<group condition="2DECKS_MODE">` structure.
- `Denon DJ LC6000 Wheel Display.xml`: `<imagesysex>` display data and `<pitchout>` elements.
- HID paths expose packet transport vocabulary, including `packetdata`, `packetnumber`,
  `packettotal`, `packetisfirst`, and `packetislast`.

The lexical inventory deliberately retains suspicious spellings such as `hannel` and
`defualt`. A file being shipped does not establish that every attribute in it is consumed.
To promote a feature to behavior evidence, author a minimal fixture, vary the feature with
a nonsense/absent control, and read the effect independently in the running app.

## Mapper cross-check

The query discovers the current repository mapper tree recursively, including quarantined
personal examples, and labels their provenance. All physical controller IDs in that tree
resolve to recovered device definitions. Keyboard uses built-in key handling and has no
corresponding device XML. Factory DDJ-GRV6 map keys all occur in the recovered factory
mapper; the local DDJ-XP2 copy additionally contains `HOLD`. These are comparisons across
snapshots, not grounds to reject a local control.

Do not equate every `<map value>` with a literal child `name`: lifecycle hooks, shifted
controls, and auto-generated LED names can differ. Personal action text remains excluded
from existence/behavior evidence. The exact differences are query output, not prose tables.

## Live custom-definition validation

**Passed on build 18.0.9598 (2026-09-12):** the custom `SIMPLE_MIDI_0_0` definition
loaded and its named note button and CC slider fired the paired mapper. Wrong-address
and wrong-channel controls left the independent live variable readback unchanged.
[Fixture, exact bytes, observed values and cleanup](../tests/controllers/README.md).
This validates the reader's recovered XML shape against an authored loadable definition;
it does not establish runtime behavior for every extracted vendor definition.
