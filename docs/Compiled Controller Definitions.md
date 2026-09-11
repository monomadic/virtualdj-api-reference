# Compiled Controller Definitions

`controllers.dat` is an encrypted ZIP container containing the original XML, including
comments and formatting. It is not a serialized tree requiring reconstruction into an
approximation of the device schema. The reader emits every member byte-for-byte.

## Read and query

```sh
just controllers-extract --output-dir /tmp/vdj-controllers --json tests/controllers-manifest.json
python3 tools/controller_schema_inventory.py /tmp/vdj-controllers/block-000.zip --output tests/controller-schema-inventory.json
just controllers
just controllers --device DDJGRV6
just controllers --path /device/settings
just controllers --path /device/slider
```

Extraction uses `uv` and the reader's pinned `pycryptodome` dependency. Offline inventory
queries need only Python's standard library. The output directory must not already exist;
no app files are changed. `--app` selects another bundle, `--input` a separate data file.
Each archive block gets its own directory and ZIP: no members are silently overwritten.
The reader rejects unsafe paths, duplicate names (case-insensitively), unexpected XML
roots, bad CRCs, invalid key envelopes, truncation, and broken block chains.

[Manifest](../tests/controllers-manifest.json) fields `roots`, `blocks[].member_count`,
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

The reproducible fixture and observed run are recorded in
[tests/controllers/README.md](../tests/controllers/README.md).
