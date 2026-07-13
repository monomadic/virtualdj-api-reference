# Skin Waveforms

Curated reference for the waveform, rhythm, and song-position element family in VirtualDJ desktop/remote skin XML: `<rhythmzone>`, `<scratchwave>`, `<blockwave>`, `<beattunnel>`, `<songpos>`, `<scratch>`, and their sub-elements.

Evidence base:

- The six official wiki pages (`Skin Rhythmzone.html`, `Skin Scratchwave.html`, `Skin BlockWave.html`, `Skin BeatTunnel.html`, `Skin songpos.html`, `Skin scratch.html`), all linked from the official Skin SDK index and all live as of 2026-07-12. Source: `Official`.
- All 15 built-in skin XML files copied into this repo (`xml/Skins/Built-In/Desktop/*.xml`, `xml/Skins/Built-In/Lite/Lite.xml`, `xml/Skins/Built-In/Remote/*.xml`) plus `xml/Skins/SDK Example - Custom Browser Skin/skin.xml`. Source: `Built-in skin` / `Published skin` (SDK example).

Every attribute row below carries a source label. Attributes that appear only on the official page and never in shipped XML are marked `Official (not observed locally)`. Attributes that appear only in shipped XML are marked `Built-in skin`. Semantics this repo derived rather than read are marked `Inference`.

## The Two Waveform Mechanisms

VirtualDJ skins have two unrelated ways to draw a deck waveform:

1. **`<visual type="waveform">`** — the simple mechanism documented in [Skin SDK](Skin%20SDK.md) §`<visual>`. One deck's waveform in a box, no beat grid, no cue markers, no color scheme, no mouse behavior. Must sit inside a `<deck>` container. Source: `Official`.
2. **`<rhythmzone>` / `<scratchwave>`** — the full-featured mechanism every built-in skin actually uses. `<rhythmzone>` draws the classic multi-deck "rhythm wave" (two opposing curves approaching a center needle); `<scratchwave>` draws a per-deck scrolling scratch waveform with beat grid, cue markers, and mouse nudge/scratch behavior. Source: `Official`, `Built-in skin`.

No built-in skin in this repo's copies uses `<visual type="waveform">`; all use `<rhythmzone>` and `<scratchwave>`. Built-in desktop skins switch between the two displays with panels keyed to the `skinWaveformType` setting, e.g. `<panel name="horizontal_scratch_active" visibility="not setting skinWaveformType 0">` (`xml/Skins/Built-In/Lite/Lite.xml` ~line 884). Source: `Built-in skin`.

Usage counts across the 16 local skin XML files (15 built-in + SDK example):

| Element | Instances | Files | Notes |
| --- | --- | --- | --- |
| `<rhythmzone>` | 19 | 15 | Every skin except Vertical.xml (which is scratchwave-only) |
| `<scratchwave>` | 62 | 16 | Horizontal and vertical variants |
| `<songpos>` | 47 | 16 | 46 of 47 use the `class=` define-template pattern |
| `<scratch>` | 45 | 16 | Jog wheels; 43 contain `<mousecircle>` |
| `<blockwave>` | 0 | 0 | Official page only (VDJ 2018 default *video* skins, not copied here) |
| `<beattunnel>` | 0 | 0 | Official page only |

Source: `Built-in skin` (counts), `Official` (blockwave/beattunnel provenance).

---

## `<rhythmzone>`

Draws the multi-deck rhythm waveform. Per the official page it is the newer replacement for an older `rhythm` element, replacing mask/up images with `fade` and `<overlay>`. Source: `Official`.

**Syntax:** `<rhythmzone mirror="" upsidedown="" fade="" center="" deck1="" deck2="" visibility="" os="">`

**Attributes** (all optional):

| Attribute | Values | Description | Source |
| --- | --- | --- | --- |
| `mirror` | `true`\|`false` (default `false`) | Adds a mirrored wave below the current one (at the X axis) | `Official`; `Built-in skin` (19/19 instances set it, e.g. `mirror="true"` in SDK example skin.xml ~line 1322) |
| `upsidedown` | `true`\|`false` (default `false`) | Inverts the wave on the X axis | `Official`; `Built-in skin` (19/19) |
| `fade` | pixels | Width over which the waves fade to black at both sides | `Official`; `Built-in skin` (19/19, always `fade="200"` locally) |
| `center` | X position | X position of the wave center, for off-center rhythmzones | `Official (not observed locally)` |
| `deck1`, `deck2` | `left`\|`right` | Which deck feeds each wave slot; all 2-deck built-ins use `deck1="left" deck2="right"` | `Built-in skin` (15 files); slot-assignment semantics: `Inference` |
| `visibility` | bool or VDJScript | Standard conditional visibility | `Official`; `Built-in skin` (SDK example skin.xml ~line 1379: `visibility="not skin_panel 'horizontal_scratch_active'"`) |
| `os` | `mac`\|`pc` | OS-conditional display | `Official (not observed locally on this element)` |

**Children** (all observed in 19/19 built-in instances unless noted): `<pos>`, `<size>`, `<colors>`, `<rhythm>`, `<grid>`, `<gridlines>` (16/19), `<cue>`, `<overlay>`. The official page documents all of these except `<gridlines>`. Source: `Official`, `Built-in skin`.

### `<rhythm>` (child)

Vertical position and height of the waves inside the zone. Attributes: `y=""`, `height=""`. Both math expressions allowed (`height="173-30"`). Source: `Official`, `Built-in skin` (19/19).

### `<colors>` (child) — deck color scheme

Sets the wave color per deck. The official page names the attributes `chanX=""`, `chanX_left=""`, `chanX_right=""`, `chanX_active=""` and notes that `transparent`, `black`, and `#000000` waves are ignored. Its own example, however, uses `deck1=` / `deck1_active=` naming, and every built-in skin uses the `deckN` form exclusively. Source: `Official` (attribute set and ignore rule), `Built-in skin` (naming).

Observed attribute matrix (25 `<colors>` blocks: 19 in rhythmzones, 6 in `<define>` blocks):

| Attribute | Count | Meaning | Source |
| --- | --- | --- | --- |
| `deck1=`, `deck2=` | 19 each | Base (inactive/passive) wave color for that deck | `Official` example, `Built-in skin`; "base color" reading: `Inference` |
| `deck1_active=`, `deck2_active=` | 19 each | Wave color when the deck is active | `Official`, `Built-in skin` |
| `deck1_left=`, `deck2_right=` | 5 each | Side-variant color; official page lists `chanX_left`/`chanX_right` without explaining them | `Official` (names only), `Built-in skin` |
| `deck3=`, `deck3_active=`, `deck3_left=`, `deck4=`, `deck4_active=`, `deck4_right=` | 4 each | Same scheme extended to decks 3/4 in Pro.xml and Performance.xml 4-deck rhythmzones | `Built-in skin` |

Values may be hex colors, named skin colors (`waveform_active1`), or `0`. Pro.xml ships two parallel rhythmzones that differ only in which slots are `0` versus colored (lines 4672-4695 vs 4698-4721), and the official ignore rule says black/transparent waves are skipped — so `0` appears to be the "don't draw this variant" switch. Source: `Built-in skin`; interpretation: `Inference`.

Trimmed real example (`xml/Skins/Built-In/Desktop/Pro.xml` lines 4698-4706):

```xml
<colors
    deck1="waveform_passive1" deck1_active="waveform_active1" deck1_left="0"
    deck2="waveform_passive2" deck2_active="waveform_active2" deck2_right="0"
    deck3="waveform_passive3" deck3_active="waveform_active3" deck3_left="0"
    deck4="waveform_passive4" deck4_active="waveform_active4" deck4_right="0"
/>
```

Note the left/right pairing: odd decks get `_left`, even decks get `_right`, matching the sides those decks occupy in the rhythm display. Source: `Built-in skin`; pairing rationale: `Inference`.

### `<grid>` (child of rhythmzone)

Computed-beat-grid (CBG) markers under the wave.

| Attribute | Description | Source |
| --- | --- | --- |
| `height` | Marker height | `Official`, `Built-in skin` (19/19) |
| `width` | Marker width | `Official`, `Built-in skin` (19/19) |
| `mainwidth` | Width of the main (downbeat) marker | `Official`, `Built-in skin` (Lite.xml ~line 869, Remote skins) |
| `maxwidth` | Appears where `mainwidth` would (Pro.xml line 4682, SDK example ~line 1306); relationship to `mainwidth` unconfirmed | `Built-in skin` |

Child `<pos y1="" y2="" y3="" y4=""/>` gives the Y position of each deck's grid row (official page: `y1`, `y2`, `yX`). Source: `Official`, `Built-in skin`.

### `<gridlines>` (child of rhythmzone and scratchwave)

Vertical beat lines across the full wave. Not on the official rhythmzone page; the official scratchwave page lists a `<gridlines>` child with `height`, `y`, `deckcolor`, `mirrored` — none of which appear in shipped XML. All 74 local instances use exactly:

```xml
<gridlines width="1" color="darkgray" transparency="0.6"/>
```

| Attribute | Description | Source |
| --- | --- | --- |
| `width` | Line width in pixels | `Built-in skin` (74/74) |
| `color` | Line color (named or hex) | `Built-in skin` (74/74) |
| `transparency` | 0-1 opacity | `Built-in skin` (74/74) |
| `height`, `y`, `deckcolor`, `mirrored` | Listed on official scratchwave page only | `Official (not observed locally)` |

### `<cue>` (child of rhythmzone and scratchwave)

Cue/POI markers drawn on the wave. Attributes: `y=""`, `height=""` (`Official`, 81/81 local), plus `mirrored="true"` on 5 vertical-scratchwave instances (Pro.xml ~line 5874, Vertical.xml ~line 4617) — `Built-in skin` only.

Children:

- `<mask x="" y="" width="" height=""/>` — sprite coordinates in the skin graphic used as the marker flag. Source: `Official` (named, no attribute detail), `Built-in skin` (81 instances, all with x/y/width/height).
- `<text dx="" dy="" fontsize="" size="" weight="" color=""/>` — cue-name label offset and styling; `color="deckcolor"` is common. `size=` appears in the official examples, `fontsize=` in built-ins. Source: `Official` (named), `Built-in skin` (67 instances).

### `<overlay>` (child of rhythmzone and scratchwave)

The play-position needle/marker drawn over the wave. Children `<pos>`, `<size>`, `<background>`. Source: `Official`, `Built-in skin` (81/81 instances have all three).

`<background>` takes two mutually exclusive forms in real skins:

- Drawn shape: `<background color="needle" shape="square"/>` — modern built-ins. Source: `Built-in skin`.
- Skin-graphic coordinates: `<background x="715" y="1395"/>` — official example and SDK example skin. Source: `Official`, `Published skin`.

### Full example

`xml/Skins/Built-In/Lite/Lite.xml` lines 864-882 (trimmed indentation):

```xml
<rhythmzone mirror="false" upsidedown="false" fade="200" deck1="left" deck2="right">
  <pos x="0" y="44"/>
  <size width="1920" height="135"/>
  <colors deck1="waveform_passive1" deck2="waveform_passive2"
          deck1_active="waveform_active1" deck2_active="waveform_active2"/>
  <rhythm y="+0" height="115"/>
  <grid height="6" width="5" mainwidth="10">
    <pos y1="+117" y2="+125"/>
  </grid>
  <gridlines width="1" color="gridlines" transparency="0.5"/>
  <cue y="+0" height="115">
    <mask x="169" y="262" width="11" height="66+20"/>
    <text dx="+10" dy="+0" weight="bold" fontsize="12" color="deckcolor"/>
  </cue>
  <overlay>
    <pos x="960" y="+0"/>
    <size width="1" height="135"/>
    <background color="needle" shape="square"/>
  </overlay>
</rhythmzone>
```

Source: `Built-in skin`.

---

## `<scratchwave>`

Per-deck scrolling scratch waveform. Source: `Official`, `Built-in skin` (62 instances in all 16 files — the most-used element of the family).

**Syntax:** `<scratchwave deck="" orientation="" color="" color2="" nudge="" visibility="">`

**Attributes:**

| Attribute | Values | Description | Source |
| --- | --- | --- | --- |
| `deck` | `left`\|`right`\|`1`..`4` | Deck to display | `Official`, `Built-in skin` (62/62) |
| `orientation` | `horizontal`\|`vertical` | Waveform direction | `Official`, `Built-in skin` (62/62; vertical in Pro.xml ~line 5820 and Vertical.xml) |
| `color` | color | Primary waveform color (official: used when volume is "full") | `Official`, `Built-in skin` (58/62, typically `color="scratch1"`) |
| `color2` | color | Secondary color (official: when primary isn't full) | `Official`, `Built-in skin` (58/62) |
| `colorVocal`, `colorInstru`, `colorBeat` | colors | Stem-colored waveform colors | `Official (not observed locally)` |
| `colorNoVocal`, `colorNoInstru`, `colorNoBeat` | colors | Colors when that stem is muted; default to darkened versions | `Official (not observed locally)` |
| `nudge` | `yes`\|`no`\|`vinylmode` | Mouse behavior: nudge the song or scratch | `Official`; `Built-in skin` (`nudge="vinylmode"` in 4 Remote skin instances, e.g. `xml/Skins/Built-In/Remote/16x9T.xml` ~line 1712) |
| `visibility` | bool or VDJScript | Conditional visibility | `Built-in skin` (6 instances) |

**Children:** `<pos>`, `<size>`, `<grid>`, `<gridlines>` (see rhythmzone section above), `<cue>` (see above), `<overlay>` (see above). Source: `Official`, `Built-in skin`. Pro.xml also stacks multiple `<size ... condition="..."/>` children so the wave resizes per layout condition (Pro.xml ~lines 5822-5823). Source: `Built-in skin`.

### `<grid>` (child of scratchwave)

Different attribute set than the rhythmzone grid — flat attributes instead of a `<pos>` child:

| Attribute | Description | Source |
| --- | --- | --- |
| `size` | Regular beat marker size | `Official`, `Built-in skin` (60/62) |
| `mainsize` | Downbeat (4-beat) marker size | `Official`, `Built-in skin` (60/62) |
| `phrasesize`, `phrasecolor` | Phrase-boundary marker size/color | `Official (not observed locally)` |
| `height` | Marker height (width if vertical) | `Official`, `Built-in skin` (62/62) |
| `pos` | Position offset | `Official`, `Built-in skin` (62/62, often negative e.g. `pos="-10"`) |
| `maincolor` | Downbeat marker color (often `deckcolor`) | `Official`, `Built-in skin` (58/62) |
| `color` | Regular marker color | `Official`, `Built-in skin` (58/62) |
| `transparency` | 0-1 opacity | `Official (not observed locally on grid; observed on gridlines)` |
| `mirrored` | Mirror markers to the other side of the wave | `Official`, `Built-in skin` (62/62 among desktop skins) |
| `background` | Shade the background by beat (`yes`/`no`) | `Official`, `Built-in skin` (16 instances) |
| `backgroundcolor` | Shading color (default white) | `Official (not observed locally)` |
| `backgroundshaded` | Appears alongside `background="no"` | `Built-in skin` (16 instances, e.g. Pro.xml ~line 5824) |
| `shapepos`, `shapemirrored` | Position/mirror for the stem-"shape" marker row; `shapemirrored="down"` observed | `Built-in skin` (46 instances each) |

### Full example

`xml/Skins/Built-In/Desktop/Pro.xml` lines 4724-4738:

```xml
<scratchwave deck="1" orientation="horizontal" color="scratch1" color2="scratch2">
  <pos x="0" y="+45+12"/>
  <size width="1920" height="43-24"/>
  <grid size="1" mainsize="4" height="8" pos="-10" maincolor="deckcolor" color="darkgray"
        mirrored="true" shapepos="-12" shapemirrored="down"/>
  <gridlines width="1" color="darkgray" transparency="0.5"/>
  <cue y="-12" height="15">
    <mask x="307" y="0" width="15" height="15"/>
    <text dx="+12" dy="-2" weight="" fontsize="13" color="texton"/>
  </cue>
  <overlay>
    <pos x="960" y="-12"/>
    <size width="1" height="43"/>
    <background color="needle" shape="square"/>
  </overlay>
</scratchwave>
```

Source: `Built-in skin`.

---

## `<songpos>`

Whole-song position/overview bar with waveform, hot-cue markers, and POI markers. Source: `Official`, `Built-in skin` (47 instances in all 16 files).

**Attributes (on the element or its `<define>` template):**

| Attribute | Values | Description | Source |
| --- | --- | --- | --- |
| `deck` | deck id | Deck to display (`deck="sandbox"` observed in Pro.xml line 1615) | `Official`, `Built-in skin` |
| `class` | define name | References a `<define class="...">` template; 46/47 built-in instances use this | `Built-in skin` (define mechanism itself: `Official`, see Skin SDK §`<define>`) |
| `width`, `height` | expressions | Placeholder overrides passed into the define template | `Built-in skin` (36 and 12 instances) |
| `visibility` | bool or VDJScript | Conditional visibility (e.g. `visibility="leftdeck"` in Performance.xml ~line 7428) | `Built-in skin` (12 instances) |
| `half` | `YES`\|`NO` | Display waveform cut in half | `Official (not observed locally)` |
| `colorPlayed` | color | Color of the already-played portion | `Official`, `Built-in skin` (on every songpos define, e.g. `colorPlayed="darker"`) |
| `colorBass`, `colorMed`, `colorHigh` | colors | Frequency-band colors; optional, only used when `coloredWaveforms` is set to monochrome | `Official`, `Built-in skin` (on every songpos define) |
| `colorVocal`, `colorInstru`, `colorBeat`, `colorNoVocal`, `colorNoInstru`, `colorNoBeat` | colors | Stem colors (VirtualDJ 2021+) | `Official (not observed locally)` |
| `orientation` | `horizontal`\|`vertical`\|`circle`\|`round` | Bar orientation | `Official (not observed locally)` |

**Children:**

- `<pos>`, `<size>` — placement. Source: `Official`, `Built-in skin`.
- `<wave>` — inner waveform strip: `<size height=""/>` and `<pos y=""/>` only. Every built-in songpos define includes one (19 instances, 15 files). Source: `Official`, `Built-in skin`.
- `<cues>` — hot-cue markers. Element attributes `dy=""` and `shade=""` appear in both the official example and built-ins (`shade="0.2"` in Pro.xml line 1343) but neither source explains them. Children: `<size width="" height=""/>`, `<clipmask x="" y=""/>` (mask coordinates), `<up>`, `<down>`, `<over>` (sprite coordinates for default/active/hover states — official; `<down>`/`<over>` observed in SDK example skin.xml lines 19-26). Source: `Official`, `Built-in skin`, `Published skin`.
- `<loops>` — saved-loop markers, same structure as `<cues>` (`dy` observed, `shade` not). Source: `Official`, `Built-in skin` (18 instances).
- Special waveform-state children `<down>`, `<volume>`, `<selected>`, `<volumeselected>`, `<upselected>` (graphics for played/unplayed portions at min/max volume). Source: `Official (not observed locally as direct songpos children)`.

### The define-template pattern

Built-in skins never inline songpos styling at the call site. They declare one template and instantiate it per deck/panel:

`xml/Skins/Built-In/Desktop/Pro.xml` lines 1336-1350:

```xml
<define class="songpos" colorPlayed="darker" colorBass="colorbass" colorMed="colormed"
        colorHigh="colorhigh" placeholders="width=799-20-24-2-2-170">
  <pos x="+0" y="+0"/>
  <size width="[WIDTH]" height="34-2"/>
  <wave>
    <size height="34-2"/>
    <pos y="+0"/>
  </wave>
  <cues dy="0" shade="0.2">
    <size width="9" height="34-2"/>
    <clipmask x="277" y="0"/>
  </cues>
  <loops dy="0">
    <size width="5" height="34-2"/>
    <clipmask x="291" y="0"/>
  </loops>
</define>
```

Instantiation (Pro.xml lines 1615-1618):

```xml
<songpos class="songpos" deck="sandbox">
  <pos x="+35+1" y="+1"/>
  <size width="200-2" height="27-2"/>
</songpos>
```

Source: `Built-in skin`. The SDK example uses `classdeck="left"` / `classdeck="right"` on its songpos defines to make per-deck template variants (`xml/Skins/SDK Example - Custom Browser Skin/skin.xml` lines 19-33). Source: `Published skin`.

---

## `<scratch>`

Invisible interactive zone for mouse scratching — the hit area of a jog wheel. It draws nothing itself; built-ins layer it over `<slider orientation="round">` spinners and `<visual>` dome graphics. Source: `Official`; layering observation: `Built-in skin`.

**Syntax:** `<scratch visibility="" os="" panel="" deck="">`

All four attributes are the standard inherited/global ones; built-in instances inside `<define class="jogwheel...">` blocks omit them all. Source: `Official`, `Built-in skin` (45 instances in 16 files).

**Children:**

| Child | Description | Source |
| --- | --- | --- |
| `<pos x="" y=""/>` | Zone position | `Official`, `Built-in skin` (45/45) |
| `<size width="" height=""/>` | Zone dimensions | `Official`, `Built-in skin` (45/45) |
| `<mousecircle x="" y="" r=""/>` | Circular mouse-detection area | `Official`. Built-ins use it either empty (`<mousecircle/>`, inherit zone bounds — `Inference`) or as `<mousecircle width="184" height="184"/>` (Lite.xml ~line 558); the official `x`/`y`/`r` form is not observed locally |
| `<mouserect x="" y="" width="" height=""/>` | Rectangular mouse-detection area | `Official (not observed as a scratch child locally; the local mouserect hits are on other element types)` |
| `<mousemask x="" y=""/>` | Black/white graphic mask for mouse detection | `Official`, `Built-in skin` (2 instances; most local mousemask usage is on `<slider>`) |
| `<center x="" y=""/>` | Center point for circular mouse movement | `Official (not observed locally)` |

Real example (`xml/Skins/Built-In/Desktop/Pro.xml` lines 1203-1207, inside a jogwheel define):

```xml
<scratch>
  <pos x="+0" y="+0"/>
  <size width="164" height="164"/>
  <mousecircle/>
</scratch>
```

Source: `Built-in skin`. Note `<mousecircle>` also appears as a child of `<visual>` (25 local instances, e.g. Pro.xml ~line 1163) to give jog-dome visuals a circular hit area. Source: `Built-in skin`.

---

## `<blockwave>`

Block-style monochrome waveform with no skin graphics; per the official page it was introduced for VirtualDJ 2018's default video skins. **Zero instances in this repo's built-in skin copies** — everything below is official-page only. Source: `Official`.

**Syntax:** `<blockwave color="" blocksize="" zoom="" center="" deck="" panel="" visibility="" os="">`

| Attribute | Description | Source |
| --- | --- | --- |
| `color` | Block color (HTML, RGB, ARGB, or predefined names) | `Official` |
| `blocksize` | Block width in pixels (integer); gap between blocks is hard-coded 1:1 | `Official` |
| `zoom` | Samples per block (integer): `1` = 80 blocks/second, `2` = 40, etc.; `4` used in the 2018 video skins | `Official` |
| `center` | Centers the wave (current position in the middle); left-aligned if omitted | `Official` |
| `deck`, `panel`, `visibility`, `os` | Standard inherited attributes | `Official` |

**Children:** `<pos x="" y=""/>`, `<size width="" height=""/>`. Source: `Official`.

Official example:

```xml
<blockwave deck="left" blocksize="5" zoom="4" color="#0d86e3" center="middle">
  <pos x="5" y="10"/>
  <size width="1280" height="150"/>
</blockwave>
```

Source: `Official`.

---

## `<beattunnel>`

Beat-move "tunnel" visualization (concentric rings approaching on the beat), no skin graphics. **Zero instances in this repo's built-in skin copies.** Source: `Official`.

| Attribute | Description | Source |
| --- | --- | --- |
| `color` | Ring color (HTML, RGB, ARGB, or predefined names) | `Official` |
| `depth` | How far in the future the center ring is, in milliseconds (`4000` = 4 s ≈ 8 beats at 120 BPM) | `Official` |

**Children:** `<pos x="" y=""/>`, `<size width="" height=""/>` — equal width/height gives a round tunnel, unequal gives an oval. Source: `Official`.

```xml
<beattunnel depth="4000" color="#00AAFF">
  <pos x="30" y="200"/>
  <size width="250" height="250"/>
</beattunnel>
```

Source: `Official`.

---

## Related Elements That Are Not Part of This Family

- **`<zoomed x="" y="" width="" height=""/>`** — despite the waveform-sounding name, every local instance (8 in 5 files, e.g. `xml/Skins/Built-In/Lite/Lite.xml` line 1380) is a child of `<browser>` and defines the browser's zoomed-view rectangle. Not a waveform element. Source: `Built-in skin`.
- **`<songposbar>`** — does not exist. Not on the official Skin SDK index, no dedicated wiki page, zero hits in local skin XML. Source: `Official` (absence from index), `Built-in skin` (absence).
- **Legacy `<rhythm>` top-level element** — the official rhythmzone page says rhythmzone superseded an older rhythm element with mask/up images. Every local `<rhythm>` hit is the rhythmzone *child* described above; the legacy standalone form has no local evidence and no live wiki page found. Source: `Official` (mention), `Built-in skin` (absence).
- **`<visual type="waveform">` and `type="spectrum">`** — see [Skin SDK](Skin%20SDK.md) §`<visual>` and [VirtualDJ Reference](VirtualDJ%20Reference.md) §Skin SDK for the simple visual-based alternatives.

---

## Open Questions

Unresolved items; do not treat any of these as documented behavior.

1. **`chanX` vs `deckN` color naming.** The official rhythmzone prose names the `<colors>` attributes `chanX*` but its own example and all shipped XML use `deckN*`. Both may be accepted, or `chanX` may be stale wiki text. Needs local test.
2. **Semantics of `deckN_left` / `deckN_right`.** Names are official, usage is real (Pro.xml, Performance.xml 4-deck), but neither source explains when the `_left`/`_right` color is applied (crossfader side? screen side?). The odd/even pairing in Pro.xml suggests screen side, but that is `Inference` only.
3. **`deck1="0"` in `<colors>`.** Reading `0` as "suppress this wave variant" (via the official black/transparent-ignored rule) is `Inference`; not officially stated.
4. **`grid maxwidth` vs `mainwidth`.** Both appear in shipped rhythmzone grids (Lite/Remote use `mainwidth`, Pro/SDK example use `maxwidth`); only `mainwidth` is on the official page. Are they synonyms, or does `maxwidth` cap marker growth? Needs local test.
5. **`<gridlines>` attribute mismatch.** Official scratchwave page lists `height`, `y`, `deckcolor`, `mirrored`; all 74 local instances use only `width`, `color`, `transparency`. Both sets may be valid; unverified.
6. **`<cues shade="" dy="">` semantics.** Present in official examples and built-ins, explained by neither. `shade` plausibly dims markers in the played region; `Inference` only.
7. **`shapepos` / `shapemirrored` / `backgroundshaded` on scratchwave `<grid>`.** Heavily used in built-ins (46/46/16 instances), absent from the official page. "Shape" likely refers to the stem-shape waveform row (cf. official `colorVocal`/`colorInstru`/`colorBeat` "shape waveform" wording); exact behavior unverified.
8. **`<mousecircle>` forms.** Official documents `x`/`y`/`r`; built-ins use empty `<mousecircle/>` or `width`/`height`. Whether the empty form inherits the parent zone bounds is `Inference`.
9. **songpos `orientation="circle|round"`** and the special waveform-state children (`<down>`, `<volume>`, `<selected>`, `<volumeselected>`, `<upselected>`): official only, no shipped usage found, no rendering verified.
10. **Stem colors (`colorVocal` etc.) on scratchwave/songpos.** Official (2021+), zero local usage — the built-in skins presumably get stem coloring from app settings rather than skin XML. Unverified.
11. **`<blockwave>` / `<beattunnel>` behavior.** Official pages only; the 2018 video skins that used blockwave are not among this repo's copies, so nothing has been cross-checked.
12. **`<rhythmzone center="">`** — official only, never used in shipped XML.
13. **`<size condition="...">` stacking** inside scratchwave (Pro.xml ~lines 5822-5823): the first matching conditional size appears to win, consistent with the repo's conditional-structure notes in [Skin SDK](Skin%20SDK.md) §Conditional Structure vs Visibility, but this specific element's behavior is untested.

---

## Notes

- All line numbers are approximate (files may drift when re-copied from newer VirtualDJ versions).
- Built-in skin XML is not strictly well-formed XML (unescaped `&` in scripts, duplicate attributes such as repeated conditional `<pos>`/`<size>`); parsers need to be lenient. Source: `Built-in skin` (parse attempts on all 15 files failed under a strict XML parser).
- Counts in this document were generated by regex scans over `xml/Skins/Built-In/**/*.xml` plus the SDK example skin on 2026-07-12.
