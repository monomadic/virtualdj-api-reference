# Effects Engines

Comprehensive guide to VirtualDJ's multiple effect systems, how they work, and practical usage patterns.

> Companion docs: [Effects Usage.md](Effects%20Usage.md) is the shorter mental-model overview; [Native Effects.md](Native%20Effects.md) is the effect-name catalog.

---

## Overview

VirtualDJ provides multiple independent effect engines that serve different purposes:

| Effect Engine | Purpose                             | Location                  | Number of Slots           |
| ------------- | ----------------------------------- | ------------------------- | ------------------------- |
| **ColorFX**   | Quick filter/effect control         | Filter knob per deck      | 1 per deck (special slot) |
| **Mix FX**    | Crossfader-linked transition effect | Mixer / supported skins   | 1 selected Mix FX         |
| **Deck FX**   | Standard deck effects               | FX panel per deck         | 3-6 slots per deck        |
| **Master FX** | Global effects on master output     | Master panel              | 3-6 slots                 |
| **Video FX**  | Video effects and transitions       | Video panel               | Multiple slots            |
| **Stems FX**  | Effects applied to individual stems | Stems pads, Pad FX, named stem slots | Shared routing plus stem-specific slots |
| **Pad FX**    | Quick-trigger effects with presets  | Pads pages                | Temporary effect triggers |

A useful state model is persistent rack versus volatile performance FX. FX1-FX6 behave like the persistent deck rack: they are meant to be selected, shown, saved, restored, and then triggered or adjusted. Pad FX and named stem FX slots behave more like volatile pad-owned performance state: pads can assign them on demand, they survive normal track changes/current-session use, and they eventually clear rather than becoming the performer's saved rack.

---

## ColorFX (Filter Slot)

### What is ColorFX?

ColorFX is VirtualDJ's **special effect slot** integrated with the filter knob on each deck. It provides one-knob control for quick effects that work well with a single parameter.

### Key Characteristics

- **One knob control**: Designed for filter knobs on mixers
- **Pre-fader only**: ColorFX is integrated with the EQ engine and always processes pre-fader
- **Curated effect list**: Only effects designated as "ColorFX-compatible" appear in the selection menu
- **Center position**: Knob at 50% (12 o'clock) = no effect, move left/right to apply

### ColorFX vs Regular Filter

Starting with VirtualDJ 8.4+ builds, the traditional filter and ColorFX system were unified:

- **Filter** is now a ColorFX effect (the default)
- Use `filter_selectcolorfx` to choose different ColorFX
- The knob action `filter` automatically works with whatever ColorFX is selected
- Filter resonance can be adjusted via `filterDefaultResonance` option or `filter_resonance` action

### Available ColorFX Effects

Common ColorFX-compatible effects include:

- Filter (High-pass/Low-pass with resonance)
- Echo
- Flanger
- Phaser
- Noise
- Pan
- Wahwah
- And others marked as ColorFX-compatible

### VDJScript Commands

**Select a ColorFX:**

```
filter_selectcolorfx 'echo'
filter_selectcolorfx 'flanger'
```

**Control the ColorFX knob:**

```
filter                          # Main filter/colorFX control
filter 50%                      # Reset to center (no effect)
filter 75%                      # Set to specific position
filter_resonance 50%            # Adjust filter resonance
```

**Activate/deactivate ColorFX:**

```
effect_active 'colorfx'         # Toggle on/off
effect_active 'colorfx' on      # Turn on
effect_active 'colorfx' off     # Turn off
```

**Show ColorFX GUI:**

```
effect_show_gui 'colorfx'       # Open effect parameters window
```

**Get ColorFX label:**

```
filter_label                    # Returns name of selected ColorFX
```

### Practical Usage

**Basic filter control:**

```xml
<slider action="filter" frommiddle="true">
  <pos x="100" y="100" />
  <size width="60" height="60" />
</slider>
```

**Button to select and activate:**

```xml
<button
  action="effect_active 'colorfx' & filter 50% & effect_show_gui 'colorfx'"
  rightclick="filter_selectcolorfx"
>
  <text action="filter_label" />
</button>
```

### Important Notes

- ColorFX is **always pre-fader** (cannot be changed to post-fader)
- Only one ColorFX can be active per deck at a time
- Some effects work better as ColorFX than others (check by testing parameter response)
- Filter effect has special integration and may behave differently than other ColorFX

---

## Mix FX (Crossfader-Linked FX)

### What is Mix FX?

Mix FX is a transition-oriented effect path tied to crossfader movement. Official docs expose it through the `effect_mixfx*` verb family, and VirtualDJ forum context describes it as applying an effect to both decks with strength linked to the crossfader.

This is **not** the same engine as ColorFX, Deck FX slots, or Master FX:

- **ColorFX** is per-deck and driven by the deck filter amount.
- **Deck FX** is slot-based and driven by `effect_select`, `effect_active`, and `effect_slider`.
- **Master FX** is applied to the master output.
- **Mix FX** selects a transition effect associated with crossfader movement.

### VDJScript Commands

**Select the Mix FX:**

```
effect_mixfx_select 'filter'
effect_mixfx_select 'echo'
effect_mixfx_select 'loop roll'
effect_mixfx_select 'reverb'
effect_mixfx_select 'noise'
```

**Toggle Mix FX on/off:**

```
effect_mixfx_activate
effect_mixfx_activate ? on : off
```

**Select and activate:**

```
effect_mixfx_select 'echo' & effect_mixfx_activate
```

Published skin note: the Denon Prime 4 Deluxe skin uses the reverse order:

```xml
<panel
  action="effect_mixfx_activate &amp; effect_mixfx_select 'FILTER'"
  query="effect_mixfx_select 'FILTER' ? effect_mixfx_activate"/>
```

Current local testing on VirtualDJ 8.5.9307 / 850.9336.mac.2224 confirmed direct and indirect selected-state queries in pad XML `query`/`color`, skin button `query`, and skin `visibility`. Keep the select-then-activate action order in examples because it is clearer, even though published skins sometimes use the reverse order.

### Querying the Selected Mix FX

The no-parameter form can be used as a value-returning query:

```
effect_mixfx_select
```

For pad LED/color logic, older forum examples recommend comparing that returned value instead of relying on direct boolean parameter queries:

```
param_equal "`effect_mixfx_select`" "echo" ? blink 500ms : off
```

The Denon skin uses direct skin queries such as:

```
effect_mixfx_select 'FILTER' ? effect_mixfx_activate
```

Both direct and indirect selected-state forms work in current local pad and skin tests. The direct form is easier to read when the query is only "is this Mix FX selected"; the `param_equal` form remains useful when you need to compare the returned display value or document older-build-compatible examples.

### Source Status

- `Official`: current VDJScript verbs appendix lists `effect_mixfx`, `effect_mixfx_activate`, and `effect_mixfx_select`.
- `Official`: DDJ-FLX2 hardware manual recommends `effect_mixfx_select` for assigning Mix FX in skins without native Mix FX controls.
- `Published skin`: Denon Prime 4 Deluxe skin uses `effect_mixfx_activate` and `effect_mixfx_select` for named Mix FX buttons.
- `Community`: forum examples document query caveats and `param_equal` comparison patterns.
- `Local test`: direct and indirect `effect_mixfx_select` selected-state queries work in pad XML and skin contexts on VirtualDJ 8.5.9307 / 850.9336.mac.2224.

See [Published Skin Findings](Published%20Skin%20Findings.md) for the provenance log and local test matrix.

---

## Deck FX Slots (FX1, FX2, FX3, etc.)

### What are Deck FX Slots?

Standard effect slots on each deck that provide **full multi-parameter control** with up to 6 parameters and 3 buttons per effect.

FX1-FX6 are the persistent deck rack. Skins and controller pages can show, trigger, and tweak whatever the performer has loaded there. A pad page can still select effects into these slots, but that should be treated as a deliberate rack-owning preset action because it changes persistent slot state.

### Slot Configuration

VirtualDJ skins can display effects in different layouts:

| Layout                | Slots   | Parameters per Effect          |
| --------------------- | ------- | ------------------------------ |
| **FX x1** (Single FX) | 1 slot  | Up to 6 parameters + 3 buttons |
| **FX x3** (Multi FX)  | 3 slots | Up to 2 parameters per slot    |
| **FX x6** (Advanced)  | 6 slots | 1-2 parameters per slot        |

Treat numbered deck FX slots **1-6** as the supported range. The current manual exposes an `FX x6` deck view, hardware manuals describe six VirtualDJ FX slots, and the official `effect_bank_save` / `effect_bank_load` summaries explicitly cover deck FX slots 1 to 6. User-provided local observation on 2026-06-01 also found that FX1-FX6 keep their loaded effect across a VirtualDJ quit/reopen, while FX7 and higher keep their loaded effect during the current session/across track loads but reset after restart. Do not rely on numeric slots above 6 unless you have a local build-specific test and are comfortable with unsupported behavior.

### VDJScript Commands

**Effect Selection:**

```
effect_select 1 'echo'          # Load Echo into slot 1
effect_select 2 'flanger'       # Load Flanger into slot 2
effect_select 3 'reverb'        # Load Reverb into slot 3
effect_select_multi 1 'reverb'  # Add Reverb to slot 1 without clearing earlier effects
```

Unlike `padfx`, `effect_select` does not accept inline effect parameter values. A persistent slot preset is an explicit chain:

```
effect_select 1 'cut' &
effect_slider 1 1 90% &
effect_slider 1 2 0.5bt &
effect_slider 1 3 50% &
effect_active 1 on
```

This writes the selected effect and slider values into the persistent FX1-FX6 rack. It does not have Pad FX's automatic "return parameters when stopped" behavior.

**Effect Activation:**

```
effect_active 1                 # Toggle slot 1 on/off
effect_active 2 on              # Turn slot 2 on
effect_active 3 off             # Turn slot 3 off
```

**Effect Parameters (Sliders):**

```
effect_slider 1 1 50%           # Slot 1, parameter 1 = 50%
effect_slider 1 2 1bt           # Slot 1, parameter 2 = 1 beat
effect_slider 2 1               # Control slot 2, param 1 (pass-through from knob)
```

**Effect Buttons:**

```
effect_button 1 1               # Press button 1 on slot 1 effect
effect_button 1 2               # Press button 2 on slot 1 effect
effect_button 1 3               # Press button 3 on slot 1 effect
```

**Effect GUI:**

```
effect_show_gui 1               # Show full GUI for slot 1 effect
```

**Selecting next/previous effect:**

```
effect_select 1 +1              # Next effect in list for slot 1
effect_select 1 -1              # Previous effect in list for slot 1
```

### Checking if Effects are Active

**Query if effect slot is active:**

```
effect_active 1 ? action_if_true : action_if_false
```

**Example button with visual feedback:**

```xml
<button action="effect_active 1">
  <pos x="100" y="100" />
  <size width="80" height="40" />
  <off color="#404040" />
  <on color="#00FF00" />
  <text text="FX1" />
</button>
```

**LED indicator for effect active:**

```xml
<led brightness="`effect_active 1`">
  <pos x="50" y="50" />
  <size width="20" height="20" />
  <off x="0" y="100" />
  <on x="20" y="100" />
</led>
```

### Effect by Name (Convenience Shortcut)

You can reference effects **by name** instead of slot number:

```
effect_active 'echo'            # Activate Echo (wherever it is)
effect_slider 'echo' 1 75%      # Control Echo param 1 directly
effect_active 'reverb' on       # Turn on Reverb effect
```

This is valid VDJScript and can be the right choice for quick personal mappings or a deliberate "toggle Echo wherever Echo is" shortcut.

For reference pad pages and controller-style examples, prefer slot addressing when the pad needs reliable state. If the page respects the user's persistent FX rack, trigger/control the existing slot with `effect_active`, `effect_slider`, and `effect_button` without changing the loaded effect. If the page is a self-contained preset page, it may use `effect_select` to write its own effect into the slot; document that as rack-owning behavior.

Three reliable rack-owning pad designs:

- Dedicated slot pads:
  Each pad owns one slot, such as Echo on slot 1 and Reverb on slot 2. Use this when several effects should be able to stay active together.

- Shared slot preset pads:
  Many pads program one slot, often slot 1. Pressing a pad replaces the slot's current effect, applies a known parameter preset, and activates the slot. Use this when pads are an effect picker.

- Multi-effect slot pads:
  Several pads intentionally share one slot but call `effect_select_multi` so earlier effect instances stay loaded/active. Use an effect-name argument in `effect_active` for pad state, for example `effect_active 1 'echo out'`, so Echo Out and Reverb can light independently even though they share slot 1.

For LED/query state, avoid checking only `effect_active 1` on a pad labeled with an effect name. If slot 1 is active with Reverb, a pad labeled Echo should not blink. Check `get_effect_name <slot>` first, then nest the slot active check:

```
get_effect_name 1 & param_lowercase & param_equal 'echo' ?
  effect_active 1 ? blink 500ms : off :
  off
```

For a dedicated off control, call the slot activation verb with `off`:

```
effect_active 1 off
```

For intentional multiple effects in the same slot, use `effect_select_multi` and query/toggle the named instance:

```
effect_select_multi 1 'echo out' & effect_active 1 'echo out'
effect_select_multi 1 'reverb' & effect_active 1 'reverb'
```

For same-pad toggles, check that the slot already contains the named effect, then nest the active check:

```
get_effect_name 1 & param_lowercase & param_equal 'echo' ?
  effect_active 1 ?
    effect_active 1 off :
    effect_slider 1 1 75% & effect_slider 1 2 50% & effect_active 1 on :
  effect_select 1 'Echo' & effect_slider 1 1 75% & effect_slider 1 2 50% & effect_active 1 on
```

Do not use bare `effect_select 1` for a state check. In pad actions, it can open the effect selector. Use `effect_select 1 'Echo'` only when deliberately loading Echo into slot 1.

Official VDJScript documents `&&` for query chains, where the query should return true only when both commands are true. That does not make it a good fit for complex pad action branches that also load effects, set sliders, and toggle state. Use nested conditionals for same-pad toggle actions, and keep `&&` to simple query expressions you have verified in the target surface.

### Effect Chaining

Effects process in the order they were activated:

```
effect_select 1 'filter' & effect_active 1 on       # First in chain
effect_select 2 'echo' & effect_active 2 on         # Processes after filter
effect_select 3 'reverb' & effect_active 3 on       # Processes last
```

Result: Signal → Filter → Echo → Reverb → Output

### Practical Usage Patterns

**Simple toggle button:**

```
effect_active 1
```

**Hold-to-use effect:**

```
effect_active 1 on while_pressed
```

**Effect with auto-reset:**

```
effect_active 1 on & wait 4bt & effect_active 1 off
```

**Select and activate in one action:**

```
effect_select 1 'echo' & effect_active 1 on
```

**Temporary effect (release to deactivate):**

```
down ? effect_active 1 on : effect_active 1 off
```

---

## Master FX

### What is Master FX?

Effects applied to the **master output** after all decks are mixed together. Affects the entire audio output.

### Targeting Master Deck

Use `deck master` to target master FX slots:

```
deck master effect_select 1 'reverb'
deck master effect_active 1
deck master effect_slider 1 1 50%
```

### Master FX Use Cases

- **Room/venue simulation**: Reverb on master for ambience
- **Overall compression/limiting**: Master processing
- **Broadcast effects**: Effects for live streams
- **Emergency effects**: Quick transitions or drops

### Practical Example

**Master effect that stays active:**

```
# In controller ONINIT or custom button:
deck master effect_select 2 'MyVSTEffect' & 
deck master effect_active 2 on
```

**Temporary master effect:**

```xml
<button action="deck master effect_active 1 on while_pressed">
  <text text="MASTER VERB" />
</button>
```

---

## Video FX

### What are Video FX?

Effects that modify, transform, or overlay video output.

### Video FX Categories

1. **Video Effects** - Applied to video sources (Blur, Colorize, Spectral, etc.)
2. **Video Transitions** - Crossfade effects (Cube, Doors, Fade, etc.)
3. **Video Transforms** - Modifications (Shake, Strobe, Negative, etc.)
4. **Video Overlays** - Text, titles, karaoke, etc.
5. **Video Sources** - Camera, slideshow, shader inputs

### VDJScript Commands

**Select video effect:**

```
deck master video_fx_select 'spectral'
video_fx_select 'blur'          # On current deck
```

**Activate or clear video effects:**

```
video_fx                       # Toggle selected video effect on current deck/context
deck master video_fx           # Toggle selected master video effect
video_fx_clear                 # Deactivate all video effects for this context
```

**Control video effect parameters:**

```
deck master video_fx_slider 1 50%
deck master video_fx_slider 2 75%
video_fx_button 1
get_videofx_name
get_video_fx_slider_label 1
```

**Video transitions:**

```
video_transition 1000ms         # Crossfade with 1 second transition
video_transition_select 'cube'  # Select Cube transition
video_transition 2000ms         # Run selected transition over 2 seconds
video_transition_slider 1 50%
get_videotrans_name
```

**Check video availability:**

```
is_video ? action_if_video : action_if_audio_only
```

### Practical Usage

**Map video FX to filter knobs:**

```
# Left filter = parameter 1, Right filter = parameter 2
device_side left ? deck master video_fx_slider 1 : deck master video_fx_slider 2
```

**Built-in skin-style video FX panel:**

```xml
<panel class="fxdrop_shorter"
       action1="video_fx"
       action2="video_fx_select"
       textaction="get_videofx_name &amp; param_uppercase"/>
<slider action="video_fx_slider 1"
        dblclick="video_fx_slider_reset 1"
        disabled="not effect_has_slider 'video' 1"/>
```

Built-in desktop skins use the same pattern for deck video FX and `deck master video_fx...` for master video FX. Use `effect_has_slider 'video' <n>` and `get_video_fx_slider_label <n>` to keep controls tied to the selected plugin's actual capabilities.

Source: `Official`, `Built-in skin`

---

## Stems FX

### What is Stems FX?

Effects applied to **individual stems** (Vocal, Melody, Bass, Drums, etc.) rather than the entire track.

### How Stems FX Works

VirtualDJ exposes three related Stems FX patterns:

1. **Shared FX-rack routing** - `effect_stems <stem>` tells the normal deck FX rack which stem(s) to process.
2. **Named stem FX slots** - stem names such as `vocals`, `bass`, `instru`, `rhythm`, `melody`, `hihat`, and `kick` can be used as slot targets for `effect_*` actions, separate from numeric slots 1/2/3.
3. **Pad FX stem targets** - `padfx ... 'stemfx:<stem>'` triggers a pad effect on a stem without changing the normal rack routing.

The named slot model is easy to miss. In official forum guidance, Adion described `vocals` as its own slot, separate from slots 1/2/3, and usable with the broader `effect_*` action family.

### Stem Selection Options

- **Vocal** - Lead vocals only
- **Melody** - Instruments and harmonies (Instru + Bass)
- **Rhythm** - Percussion (HiHat + Kick)
- **MeloRhythm** - Everything except vocals
- **Acapella** - Vocals only (alternative term)
- **Instrumental** - Everything except vocals (alternative term)
- **Individual stems**: Vocal, HiHat, Bass, Instru, Kick

### VDJScript Commands

**Shared FX-rack routing:**

```
effect_stems 'vocal'            # Apply effects to vocals only
effect_stems 'melody'           # Apply effects to melody only
effect_stems 'rhythm'           # Apply effects to drums only
effect_stems 'melorhythm'       # Apply effects to everything except vocals
effect_stems off                # Disable stems FX (back to full track)
```

**Check if Stems FX is active:**

```
effect_stems ? action_if_active : action_if_not_active
```

**Combine with regular effects:**

```
effect_stems 'vocal' & effect_active 1 'echo'
```

**Named stem FX slots:**

```
effect_select 'vocals' 'Reverb'     # Load Reverb into the vocal stem FX slot
effect_active 'vocals'              # Toggle the vocal stem FX slot
effect_select_multi 'vocals' 'Echo Out' # Add Echo Out without clearing other vocal effects
effect_active 'vocals' 'Echo Out'   # Toggle/query the named effect in the vocal slot
effect_slider 'vocals' 1 50%        # Move parameter 1 for the vocal stem FX slot
effect_slider 'vocals' 'echo' 1 50% # Move Echo param 1 in the vocal slot
effect_show_gui 'vocals' 'Reverb'   # Show the vocal Reverb GUI
effect_show_gui 'rhythm' 'Beat Grid'
```

`vocals` is plural in the stem-slot examples. This differs from the `effect_stems 'vocal'` and `padfx ... 'stemfx:vocal'` target strings.
Current known named stem FX slots are `vocals`, `bass`, `instru`, `rhythm`, `melody`, `hihat`, and `kick`. `melovocal` and `melorhythm` may exist, but need local testing before they are treated as confirmed. Do not assume aggregate names such as `instrumental` or `acapella` are valid named stem FX slots unless tested.

User-provided local observation on 2026-06-01 found that named stem FX slots keep their loaded effect during the current session and across track loads, but reset after a VirtualDJ restart. Treat this as loaded-effect selection behavior only; active state, slider values, and multi-effect contents still need a recorded build-specific persistence pass.

That restart boundary makes named stem FX slots a good fit for pad-assigned, stateful performance effects. They let a pad own a vocal/rhythm/bass effect choice without overwriting the persistent FX1-FX6 rack.

Pad XML selected-state pattern:

```xml
<pad name="REVERB - Vocals"
     color="stem_color 'vocal'"
     query="effect_select 'vocals' 'reverb' ? effect_active 'vocals' : off">
  effect_select 'vocals' 'Reverb' &amp; effect_active 'vocals'
</pad>
```

Unlike the normal numeric-slot reference examples, this uses `effect_select <stem-slot> <effect-name>` as the selected-effect check because that is the observed working stem-slot pad pattern.

Pad XML multi-effect vocal slot pattern:

```xml
<pad1 name="FX-VOCALS\nECHO OUT"
      color="stem_color 'vocal'"
      query="effect_active 'vocals' 'echo out'">
  effect_select_multi 'vocals' 'echo out' &amp; effect_active 'vocals' 'echo out'
</pad1>
<pad2 name="FX-VOCALS\nREVERB"
      color="stem_color 'vocal'"
      query="effect_active 'vocals' 'reverb'">
  effect_select_multi 'vocals' 'reverb' &amp; effect_active 'vocals' 'reverb'
</pad2>
```

Both pads address the `vocals` stem FX slot, but the query/action includes the effect name. They can therefore light independently while both effects play through the same vocal slot. This is not the `padfx ... 'stemfx:vocal'` path; it is the regular `effect_*` stem-slot path with `effect_select_multi`.

The full list of accepted named stem FX slots is not published in the official appendix, so keep new target strings tied to local tests or forum evidence.

### Stems FX from GUI

In the FX dropdown menu, toggle Stems FX mode:

- **Vocal** button - Apply effects to vocals
- **Melody** button - Apply effects to melody
- **Rhythm** button - Apply effects to rhythm

When enabled, a small **"S" icon** appears next to effects indicating Stems FX mode.

### Stems FX Pad Page

The **Stems FX** pad page provides quick access:

- **StemsFX Toggle** - Cycles through Vocal/Melody/Rhythm/Off
- **Standard FX Pads** - Trigger effects with StemsFX mode active

### Practical Usage

**Vocal-only echo out:**

```
effect_stems 'vocal' & 
effect_active 'echo out' & 
wait 4bt & 
mute_stem 'vocal'
```

**Instrument beatgrid effect:**

```
effect_stems 'melorhythm' & 
effect_active 'beatgrid'
```

**Toggle stems FX on/off:**

```xml
<button
  action="toggle '$stemfx' & 
                var '$stemfx' ? effect_stems 'vocal' : effect_stems off"
>
  <text text="STEMS FX" />
</button>
```

### Limitations and Notes

- **Pre-fader recommended**: Stems FX works best with `fxProcessing` set to `pre-fader`
- **Some hardware incompatible**: Controllers with hardware FX sends may not support Stems FX properly
- **ColorFX/stems behavior**: Older forum guidance and local findings have been build-sensitive; test exact ColorFX-plus-stems behavior before relying on it
- **Reset options**: Use `resetStemsOnLoad` and `resetFXOnLoad` options to auto-reset
- **Slot spelling**: The vocal named stem FX slot is `vocals`, while the official `padfx` target is `stemfx:vocal`
- **Aggregate names**: `melovocal` and `melorhythm` may exist as named stem FX slots, but need testing; `instrumental` and `acapella` are useful stem concepts but are not confirmed as named stem FX slots

### Source Status

- `Official`: VDJScript appendix documents `effect_stems`, `effect_arm_stem`, and `padfx ... 'stemfx:stemname'`.
- `Official forum`: Adion documented `effect_show_gui "rhythm" "Beat Grid"` and said the same syntax can be used with other `effect_*` actions; he also described `vocals` as a separate effect slot.
- `Community`: moderator examples use `effect_show_gui vocals echo & padfx echo 'stemfx:vocal'` to inspect a vocal padfx mapping.
- `Local test`: vocal Reverb pad pattern with `effect_select 'vocals' 'reverb' ? effect_active 'vocals'`; user-provided multi-effect vocal pad pattern with `effect_select_multi 'vocals' 'echo out'` and `effect_select_multi 'vocals' 'reverb'` (build not recorded); user-provided restart-persistence observation that named stem FX slots reset their loaded effect after restart; current named slot list in local notes is `vocals`, `bass`, `instru`, `rhythm`, `melody`, `hihat`, and `kick`.

---

## Pad FX

### What is Pad FX?

**Quick-trigger effects** with pre-configured parameters, designed for single-button effect execution.

### Pad FX Characteristics

- **Preset parameters**: Effects are called with specific parameter values
- **Temporary by design**: Intended to trigger and release, not save settings
- **Independent from slots**: Can run alongside regular FX slots
- **Shared by effect/target identity**: `padfx 'reverb' ... 'stemfx:vocal'` is not a private instance owned by the pad that called it
- **Volatile pad-owned state**: Good when the pad should assign its own effect without rewriting FX1-FX6
- **Perfect for performance**: Quick creative effects without knob adjustment

### VDJScript Commands

**Basic Pad FX:**

```
padfx 'echo' 50% 1bt            # Echo at 50% strength, 1 beat length
padfx 'beatgrid'                # Trigger beatgrid effect
padfx 'flanger' 75% 2bt         # Flanger at 75%, 2 beat speed
```

**Single Pad FX (one-shot):**

```
padfx_single 'echo out' 80% 1bt
```

**Pad FX with Stems:**

```
padfx 'echo' 50% 1bt 'stemfx:vocal'
padfx 'reverb' 75% 'stemfx:melorhythm'
padfx 'echo out' 85% 70% 62.5% 20% 'stemfx:vocal'
padfx 'echo out' 80% 1bt 25% 75% 'stemfx:vocal'
```

Official `padfx` stem modifiers:

```
padfx 'echo out' 80% 'solostem:vocal'   # Only let vocal be audible during the effect
padfx 'echo out' 'mutestem:rhythm'      # Mute rhythm during the effect
padfx 'reverb' 'stemfx:vocal'           # Apply effect only to vocal
```

Official `padfx` stem names are `Vocal`, `HiHat`, `Bass`, `Instru`, `Kick`, `Melody`, `Rhythm`, `MeloVocal`, and `MeloRhythm`. Existing local pad pages normally use lowercase strings.

**Full Pad FX syntax:**

```
padfx 'effectname' param1 param2 param3 param4 'stemfx:stemname'
```

This compact "effect plus parameter list plus optional stem/switch modifier" form is specific to Pad FX. For regular persistent slot FX, the closest equivalent is an explicit `effect_select` / `effect_slider` / `effect_button` / `effect_active` chain, and that chain changes the rack state until something else changes it.

### Pad FX Parameter Order

Parameters depend on the effect. Common patterns:

**Echo:**

```
padfx 'echo' strength% length_beats feedback% wetdry%
padfx 'echo' 50% 1bt 65% 75%
```

**Echo Out:**

```
padfx 'echo out' strength% length_beats
padfx 'echo out' 80% 1bt
```

**Beatgrid:**

```
padfx 'beatgrid'                # No parameters needed
```

**Vinyl Brake:**

```
padfx 'vinylbrake' multiplier length_beats echo% repeat%
padfx 'vinylbrake' 1bt 50% 50% 0%
```

### Working Pad FX Parameter Examples

Treat these as working examples, not a complete effect-parameter specification. `padfx` arguments are effect-specific, and VirtualDJ does not publish a full native parameter map.

| Effect | Working form | Source |
| --- | --- | --- |
| Cut | `padfx 'cut' 50% 0.5bt` | `Local test`: `examples/Pads/PUSH FX.xml` |
| Cut | `padfx 'cut' 40% 1bt` | `Local test`: `examples/Pads/PUSH FX.xml` |
| Flanger | `padfx 'flanger' 70% 1bt` | `Local test`: `examples/Pads/PUSH FX.xml` |
| BeatGrid | `padfx 'beatgrid'` | `Local test`: `examples/Pads/PUSH FX.xml` |
| Echo on vocal stem | `padfx 'echo' 50% 1bt 65% 75% 'stemfx:vocal'` | `Local test`: `examples/Pads/PUSH FX.xml` |
| Reverb on vocal stem | `padfx 'reverb' 55% 2bt 'stemfx:vocal'` | `Local test`: `examples/Pads/PUSH FX.xml` |
| Echo Out on vocal stem | `padfx_single 'echo out' 80% 1bt 'stemfx:vocal'` | `Local test`: `examples/Pads/PUSH FX.xml` |
| Echo Out on vocal stem | `padfx "echo out" 80% 1bt "stemfx:vocal"` | `Built-in pad page`: `pads_stems+fx.xml` |
| Reverb on vocal stem | `padfx "Reverb" 80% "stemfx:vocal"` | `Built-in pad page`: `pads_stems+fx.xml` |
| BeatGrid on instrumental/melorhythm stem | `padfx "Beat Grid" "stemfx:MeloRhythm"` | `Built-in pad page`: `pads_stems+fx.xml` |

The local `PUSH FX` page clears temporary pad effects with:

```vdjscript
effect_disable_all 'padfx'
```

That is useful for separate reset/cleanup controls on momentary performance pages that track their own pad state with variables. User-provided testing found that chaining `effect_disable_all 'padfx'` immediately before new `padfx` calls in the same pad action can prevent the new pad FX from activating or lighting, while the same chained `padfx` calls work when the inline clear is removed. Treat `effect_disable_all 'padfx'` as a cleanup command, not as a deterministic initializer for a new pad-FX chain.

`padfx` is deterministic about the values passed at the moment it starts, but it does not appear to provide per-pad ownership. Another pad that calls the same effect and stem target, for example another `padfx 'reverb' ... 'stemfx:vocal'`, can reuse or retune that shared pad-FX identity. Use `padfx` for volatile performance gestures. If the performer needs a restart-persistent rack or a visible stable chain, reserve numbered deck FX slots 1-6; if a pad writes those slots with `effect_select`, document that it owns/reprograms the rack.

### Checking Pad FX Status

Pad FX don't have a built-in "active" query. Track status with variables:

```
# Set variable when activating
set 'padfx_active' 1 & padfx 'echo' 50% 1bt

# Check variable
var 'padfx_active' ? visual_feedback_on : visual_feedback_off
```

### Show Pad FX GUI

```
effect_show_gui 'stemname' 'effectname'
effect_show_gui 'vocals' 'echo'
effect_show_gui 'rhythm' 'beatgrid'
```

For GUI calls, source examples use the stem-slot style (`vocals`) rather than the `padfx` modifier style (`stemfx:vocal`).

### Practical Usage

**Simple pad effect:**

```xml
<button action="padfx 'echo out' 75% 1bt">
  <text text="ECHO OUT" />
</button>
```

**Stems-specific pad effect:**

```xml
<button
  action="effect_stems 'vocal' & 
                padfx_single 'echo out' 80% 1bt & 
                wait 4bt & 
                mute_stem 'vocal' & 
                effect_stems off"
>
  <text text="VOCAL OUT" />
</button>
```

**Advanced stems + effect combo:**

```xml
<!-- Mute melody, echo it out, then mute it -->
<button
  action="var 'stemsnfx' 1 ? 
                  toggle 'stemsnfx' & mute_stem 'melody' off : 
                  toggle 'stemsnfx' & 
                  effect_stems 'melody' & 
                  padfx_single 'echo out' 75% 1bt & 
                  wait 1bt & 
                  mute_stem 'melody' & 
                  effect_stems off"
>
</button>
```

---

## Pre-Fader vs Post-Fader

### What's the Difference?

- **Pre-fader**: Effects process **before** volume faders and crossfader
- **Post-fader**: Effects process **after** volume faders and crossfader

### Signal Flow

**Pre-fader:**

```
Deck → Effects → EQ → Volume Fader → Crossfader → Master
```

**Post-fader:**

```
Deck → EQ → Volume Fader → Crossfader → Effects → Master
```

### When to Use Each

**Use Pre-fader when:**

- Effects should continue playing even when fader is down (echo tails)
- Using effects with stems (Stems FX requires pre-fader)
- Most creative DJ effects work

**Use Post-fader when:**

- Effects should stop immediately when fader is down
- Using effects during transitions
- Hardware requires it (some mixers)

### Setting FX Processing Mode

**Global setting:**

```
setting 'fxProcessing' 'pre-fader'
setting 'fxProcessing' 'post-fader'
```

**Temporary change:**

```
setting 'fxProcessing' 'post-fader' & 
padfx 'echo out' 1bt 50% & 
wait 5000ms & 
setting 'fxProcessing' 'pre-fader'
```

**Option in Settings:**

- Settings → Audio → `fxProcessing` → Pre-fader / Post-fader

### Important Notes

- **ColorFX is always pre-fader** (cannot be changed)
- **Hardware effects**: Some controllers have hardware post-fader sends
- **Stems FX**: Works best in pre-fader mode
- **Default**: Pre-fader is the default and most common setting

---

## Effect Queries and Conditionals

### Checking Effect Status

**Is any effect active on slot:**

```
effect_active 1 ? blink : off
```

**Is specific effect active:**

```
get_effect_name 1 & param_lowercase & param_equal 'echo' ?
  effect_active 1 ? action_if_echo_active : action_if_echo_loaded_off :
  action_if_other_effect_loaded
```

**Are stems FX active:**

```
effect_stems ? show_stems_indicator : hide_indicator
```

**Multiple effect check:**

```
effect_active 1 | effect_active 2 | effect_active 3 ? led_on : led_off
```

### Visual Feedback Examples

**Button color based on effect state:**

```xml
<button action="effect_active 1">
  <size width="80" height="40" />
  <up color="#404040" radius="4" />
  <selected color="#00FF00" radius="4" />
  <text text="FX 1" />
</button>
```

**LED indicator:**

```xml
<visual source="`effect_active 1`" type="onoff">
  <pos x="100" y="50" />
  <size width="10" height="10" />
  <off color="black" />
  <on color="red" />
</visual>
```

**Text showing effect name:**

```xml
<textzone>
  <pos x="100" y="100" />
  <size width="200" height="30" />
  <text text="`get_effect_name 1`" />
</textzone>
```

**Blink when effect active:**

```
effect_active 1 & blink 500ms
```

### Effect Introspection and Dynamic Controls

For generic FX panels, skins do not need to hardcode every slider and button. VirtualDJ exposes helpers that ask the selected plugin what it supports:

```vdjscript
effect_has_slider 1 1              # Does slot 1 have slider/parameter 1?
effect_slider 1 1                  # Move/query slot 1 slider 1
effect_slider_reset 1 1            # Reset slot 1 slider 1 to default
get_effect_slider_default 1 1 0.5  # Default/center hint (see reliability note below: returned `off` on v2026-m b9482)
get_effect_slider_label 1 1        # Display label for slot 1 slider 1
get_effect_slider_text 1 1         # Display formatted current value
effect_has_button 1                # Does the selected effect expose button 1?
effect_button 1                    # Press button 1 in single-FX layout
get_effect_button_shortname 1      # Compact label for button 1
get_effect_slider_count            # Number of sliders in the current context
get_effect_button_count            # Number of buttons in the current context
```

**Helper reliability** (`Local test`: VirtualDJ `v2026-m b9482`, [Reference - FX Introspection Test.xml](../tests/Pads/Reference%20-%20FX%20Introspection%20Test.xml), deck FX slot 1, Backspin). These returns were read live and cross-checked against the effect's GUI:

| Helper | Returns | Reliable? |
| --- | --- | --- |
| `get_effect_name <slot>` | effect name (`Backspin`) | Yes — matches GUI |
| `get_effect_slider_count` / `get_effect_button_count` | slider/button count (`2` / `0`) | Yes |
| `effect_has_slider <slot> <n>` / `effect_has_button <n>` | on/off for each index | Yes — lit correctly per position |
| `get_effect_slider_text <slot> <n>` | formatted current value (`0%`, `4 bt`) | Yes — matches GUI value |
| `get_effect_slider_label_full` / `get_effect_slider_name` | full label (`Strength`, `Length`) | Yes — matches GUI label |
| `get_effect_slider_label` / `get_effect_slider_shortname` | short label (`STR`, `LEN`) | Yes — short form |
| `get_effect_slider_default <slot> <n> <fallback>` | **`off`** for real and empty sliders | **No — not a usable default; the fallback is not returned either** |

Guidance from the above:

- For a GUI-matching parameter label use `get_effect_slider_label_full` (or `get_effect_slider_name`); for a compact label use `get_effect_slider_label` (or `get_effect_slider_shortname`). They are two distinct forms, not aliases.
- For live values use `get_effect_slider_text`. Counts and `effect_has_*` are safe to drive dynamic panels.
- **Do not rely on `get_effect_slider_default`** — it returned `off` on this build. To capture an actual default, `effect_slider_reset <slot> <n>` and then read `get_effect_slider_text`.
- `debug` cannot print a computed value: it logs the literal backtick expression (same computed-argument behavior as `loop`/`beatjump`/`phrase_sync`). Read helper strings through a pad/skin `name=`/`text=` interpolation instead.

**Per-effect parameter map** (`Local test`: VirtualDJ `v2026-m b9482`, deck FX slot 1). Growing as effects are swept; absence of a row means "not yet recorded", not "no parameters".

| Effect | Sliders (full / short — unit) | Buttons |
| --- | --- | --- |
| Backspin | S1 `Strength` / `STR` (%), S2 `Length` / `LEN` (beats) | 0 |
| Flanger | GUI (labels only, `v2026-m b9336`): `Strength`, `Speed` (beats), `Tone`, `Feedback`, `LFO AMP` | helper counts not captured |

Built-in desktop skins use this pattern for slot controls:

```xml
<slider action="effect_slider 1 1"
        dblclick="effect_slider_reset 1 1"
        disabled="not effect_has_slider 1 1"
        frommiddle="get_effect_slider_default 1 1 0.5"/>
<textzone>
  <text action="get_effect_slider_label 1 1"/>
</textzone>
<button action="effect_button 1"
        visibility="effect_has_button 1"
        textaction="get_effect_button_shortname 1"/>
```

Use the no-slot form in single-FX layouts where the selected plugin owns the current control bank:

```xml
<slider action="effect_slider 1"
        dblclick="effect_slider_reset 1"
        disabled="not effect_has_slider 1"
        frommiddle="get_effect_slider_default 1 0.5"/>
<textzone>
  <text action="get_effect_slider_label 1"/>
</textzone>
```

Video FX and transition panels use the same idea with special targets:

```xml
<slider action="video_fx_slider 1"
        dblclick="video_fx_slider_reset 1"
        disabled="not effect_has_slider 'video' 1"
        frommiddle="get_video_fx_slider_default 1 0.5"/>
<text action="get_video_fx_slider_label 1"/>

<slider action="video_transition_slider 1"
        dblclick="video_transition_slider_reset 1"
        disabled="not effect_has_slider 'transition' 1"
        frommiddle="get_effect_slider_default 'transition' 1 0.5"/>
<text action="get_effect_slider_label 'transition' 1"/>
```

This is the preferred way to build a reusable FX surface. Hardcoded parameter labels are fine for a known pad preset, but generic panels should follow the selected plugin's actual slider/button count and labels. Until the fixture logs more native effects, keep effect-specific labels in examples tied to the recorded effect/build, and leave missing counts or helper strings as unknown.

Source: `Official`, `Built-in skin`, `Local test`, `Inference`

---

## Practical Effect Workflows

### Workflow 1: Echo Out Transition

Gradually remove track with echo tail:

```
effect_stems off & 
effect_select 1 'echo out' & 
effect_slider 1 1 80% & 
effect_slider 1 2 1bt & 
effect_active 1 on & 
wait 4bt & 
volume 0% 2000ms
```

### Workflow 2: Beatgrid Breakdown

Create a breakdown using beatgrid:

```
effect_select 1 'beatgrid' & 
effect_active 1 on & 
wait 16bt & 
effect_active 1 off
```

### Workflow 3: Vocal Echo with Stems

Echo only the vocals:

```
effect_stems 'vocal' & 
padfx 'echo' 50% 1bt & 
wait 8bt & 
effect_stems off
```

### Workflow 4: Build Up with Multiple Effects

Chain effects for a build-up:

```
# Start with light flanger
effect_select 1 'flanger' &
effect_slider 1 1 25% &
effect_active 1 on &

# Add echo
wait 8bt &
effect_select 2 'echo' &
effect_slider 2 1 50% &
effect_active 2 on &

# Add reverb
wait 8bt &
effect_select 3 'reverb' &
effect_active 3 on &

# Drop - remove all
wait 8bt &
effect_active 1 off &
effect_active 2 off &
effect_active 3 off
```

### Workflow 5: Acapella Out with Reverb

Remove everything but vocals with reverb tail:

```
effect_stems 'vocal' & 
padfx 'reverb' 75% 4bt & 
wait 2bt & 
mute_stem 'vocal' & 
effect_stems off
```

---

## Effect Lists and Organization

### Creating Effect Lists

VirtualDJ allows organizing effects into **custom lists** for quick access.

### Managing Effect Lists

1. Open Effects dropdown
2. Scroll to bottom
3. Click **"More..."** or **"Manage..."**
4. **Audio Effects List Editor** opens

### List Editor Functions

- **Search bar**: Find effects quickly
- **Current list**: Switch between lists
- **Add/Remove**: Build custom effect collections
- **New list**: Create specialized collections
- **Delete list**: Remove unwanted lists

### Practical List Examples

**"Quick FX" list:**

- Filter
- Echo
- Reverb
- Beatgrid
- Brake

**"Build Up FX" list:**

- Flanger
- Phaser
- Echo
- Reverb
- Riser

**"Stems FX" list:**

- Echo Out
- Reverb
- Beatgrid
- Vinyl Brake

---

## Advanced Effect Techniques

### Effect Banks

VirtualDJ exposes built-in bank helpers for saving and loading the current deck FX slots. Prefer these when the goal is "store this FX rack and recall it later":

```
effect_bank_save 1
effect_bank_load 1
```

The official summary says banks cover deck FX slots 1-6. Treat bank contents as persistent rack-level snapshots. If a pad needs to guarantee Echo at 1 beat and Reverb at 40% by writing FX1-FX6, document that it is intentionally reprogramming the saved rack; otherwise leave bank/slot selection alone and only trigger or adjust the existing rack.

Use variables only for custom behavior the bank helpers do not model, such as remembering one slot name inside a larger macro:

```
set 'fx_return_slot1' `get_effect_name 1`
effect_select 1 `get_var 'fx_return_slot1'`
```

Source: `Official`, `Inference`

### FX Layout, Lists, and Selectors

These helpers are UI/rack helpers rather than effect-processing engines:

```vdjscript
effect_3slots_layout              # Toggle 1-slot / 3-slot FX panel layout
effect_select_popup 1             # Open/select from the slot 1 effect popup
effect_select_toggle 1 'Echo'     # Select effect while keeping activation continuity
effect_list 1 +1                  # Cycle effect list for slot/list context
effect_list_edit 1                # Open editor for an effect list
effect_clone                      # Clone FX slots from another deck
```

Built-in and SDK example skins use `effect_3slots_layout` for switching single-FX and multi-FX panels. Reference pad pages use `effect_select_popup <slot>` for parameter buttons that should open the native slot selector.

Use these to expose VirtualDJ's existing FX UI model. For deterministic pads, prefer explicit slot actions.

Source: `Official`, `Built-in skin`, `Local test`

### Armed FX

The `effect_arm_*` family models hardware-style workflows: choose a target deck/path, choose an effect, choose participating slots, then activate or move the armed effect.

```vdjscript
effect_arm_deck master
effect_arm_select 'Echo'
effect_arm_slot 1
effect_arm_active
effect_arm_slider 1 50%
effect_arm_beats 1
```

Use this family for controller mappings that already have an "armed FX" mental model. In skins and pad pages, direct slot actions are usually clearer:

```vdjscript
deck master effect_select 1 'Echo' & deck master effect_active 1
```

Do not confuse `effect_arm_stem Vocal` with named stem FX slots such as `vocals`. `effect_arm_stem` selects stems for the special `stems` slot used by the armed/direct `effect_*` model; `vocals` is a separate named stem FX slot.

Source: `Official`, `Inference`

### Release FX

Release FX uses a separate slider path from normal deck FX sliders:

```vdjscript
effect_releaseslider 50%
effect_releaseslider_active 50%
is_releasefx ? on : off
```

Use `effect_releaseslider_active` when moving the release control should also activate the release effect. Use `effect_slider` / `effect_slider_active` for ordinary deck FX slots. Exact release-FX slot selection and plugin-specific behavior still needs a focused local fixture before this becomes a canonical pad pattern.

Source: `Official`

Status: Needs local test.

### FX Send/Return

Send/return helpers are for hardware-style routing paths where effects are applied to a selected source rather than a normal deck slot:

```vdjscript
effect_fxsendreturnenable
deck 1 effect_fxsendreturndeck
deck 2 effect_fxsendreturndeck_multi master
deck 2 effect_fxsendreturndeck_multi mic
```

Keep these out of ordinary pad-page examples unless the target controller or skin exposes an FX send/return workflow. The official appendix names the helpers, but local behavior depends on routing and hardware/software mixer context.

Source: `Official`

Status: Needs local test.

### Plugin-Specific Commands

`effect_command` sends commands to the currently targeted effect/plugin. Built-in plugin UI XML for BeatGrid uses strings such as `set 00`, `get 00`, and `cur 0`:

```xml
<button action="effect_command 'set 00'"
        query="effect_command 'get 00'"/>
<visual source="effect_command 'cur 0'"/>
```

The same file also shows context-dependent shortcuts around the selected plugin:

```xml
<button action="effect_show_gui"/>
<button action="effect_dock_gui"/>
<button action="effect_active"/>
<text action="get_effect_title"/>
<button action="effect slider 1 +0.143"/>
<text format="`get_effect_slider_text 1` / 8"/>
<button action="effect_button 1 on"/>
```

This is useful evidence that a plugin UI can be a fixed bitmap control surface with hardcoded plugin commands, direct coordinate arithmetic such as `x="4*20+9+3"`, and repeated controls without `<define>`, `<deck>`, or `<panel>` containers. It is not evidence for a universal `effect_command` language, a reusable generic FX rack, or the recommended structure for desktop/Remote skins. Generic skins should still prefer slot/target-qualified controls and introspection helpers such as `effect_has_slider`, `get_effect_slider_label`, and `get_effect_button_shortname`.

Source: `Built-in skin` (`examples/Skins/Built-In/Plugin-UI/AFX_beatgrid.xml`), `Inference`

### Effect Presets with Parameters

Save effect + parameters:

```
# Preset: Heavy Echo
effect_select 1 'echo' & 
effect_slider 1 1 75% & 
effect_slider 1 2 2bt & 
effect_slider 1 3 80% & 
effect_active 1 on

# Preset: Light Reverb
effect_select 2 'reverb' & 
effect_slider 2 1 30% & 
effect_slider 2 2 50% & 
effect_active 2 on
```

### Macro Effects

Combine multiple actions:

```
# "Drop" macro: Kill all effects, reset filter, cut bass momentarily
effect_active 1 off & 
effect_active 2 off & 
effect_active 3 off & 
filter 50% & 
eq_low 0% & 
wait 1bt & 
eq_low 100%
```

### Effect Automation

Use `repeat_start` for automated effect patterns:

```
# Auto-toggle filter every 4 beats
repeat_start 'auto_filter' 4bt 0 & 
  filter `filter ? 75% : 25%`

# Stop automation
repeat_stop 'auto_filter'
```

---

## Troubleshooting Common Issues

### Effects Not Working

**Check:**

1. Effect is selected in slot: `get_effect_name 1`
2. Effect is activated: `effect_active 1`
3. Parameters are not at 0: `effect_slider 1 1 50%`
4. Pre/post-fader setting matches hardware
5. Audio routing is correct

### Effects Sound Wrong

**Check:**

1. Parameter values are appropriate for the effect
2. Multiple effects aren't conflicting
3. Effect is suitable for the material (some effects work better on certain genres)
4. Stems separation quality (if using Stems FX)

### Stems FX Issues

**Check:**

1. Stems are analyzed/prepared
2. `fxProcessing` is set to `pre-fader`
3. Hardware supports software effects (not hardware sends)
4. `effect_stems` is active: `effect_stems ? on : off`
5. Correct stem name is used (Vocal, Melody, Rhythm, etc.)

### ColorFX Not Responding

**Check:**

1. Effect is ColorFX-compatible (not all effects are)
2. Using `filter` action, not `effect_slider 'colorfx'`
3. Filter knob is mapped correctly: `filter` with `frommiddle="true"`
4. Effect is actually selected: `filter_selectcolorfx 'effectname'`

### Mix FX Not Responding

**Check:**

1. The skin or custom button exposes Mix FX activation: `effect_mixfx_activate`
2. The selected Mix FX is set with `effect_mixfx_select '<name>'`
3. Query logic is using a tested form for the current context:
   - `effect_mixfx_activate ? on : off` for activation state
   - `param_equal "\`effect_mixfx_select\`" "<name>" ? on : off` for selected-name comparisons until direct queries are locally verified
4. Crossfader movement is part of the intended behavior; Mix FX is not a normal static deck FX slot

### Effect Parameters Not Changing

**Check:**

1. Correct slot number: `effect_slider 1 1` vs `effect_slider 2 1`
2. Correct parameter number (1-6)
3. Value format matches parameter type (% for dry/wet, bt for beats, ms for time)
4. Effect GUI isn't overriding controller values

---

## Quick Reference

### Effect Commands Cheat Sheet

```
# SELECTION
effect_select 1 'echo'              # Select effect for slot 1
effect_select_multi 1 'reverb'      # Add effect to slot 1 without clearing earlier effects
effect_select 'vocals' 'reverb'     # Select effect for vocal stem FX slot
effect_select 'colorfx' 'filter'    # Select ColorFX
filter_selectcolorfx 'echo'         # Select ColorFX (alternative)
effect_mixfx_select 'echo'          # Select Mix FX

# ACTIVATION
effect_active 1                     # Toggle slot 1
effect_active 1 on                  # Turn on slot 1
effect_active 'echo'                # Shortcut: toggle Echo by name
effect_active 'vocals'              # Toggle vocal stem FX slot
effect_active 'colorfx'             # Toggle ColorFX
effect_mixfx_activate               # Toggle Mix FX

# PARAMETERS
effect_slider 1 1 50%               # Slot 1, param 1 = 50%
effect_slider 1 2 1bt               # Slot 1, param 2 = 1 beat
effect_slider 'vocals' 1 50%        # Vocal stem FX slot, param 1 = 50%
effect_slider 'echo' 1 75%          # Shortcut: Echo param 1 by name
filter 50%                          # ColorFX/filter = 50%

# BUTTONS
effect_button 1 1                   # Press button 1 on slot 1
effect_button 'echo' 2              # Press button 2 on Echo

# DYNAMIC CONTROLS
effect_has_slider 1 1               # Does slot 1 expose slider 1?
get_effect_slider_label 1 1         # Label for slot 1 slider 1
get_effect_slider_default 1 1 0.5   # Default/center hint
effect_has_button 1                 # Does selected effect expose button 1?
get_effect_button_shortname 1       # Compact button label

# GUI
effect_show_gui 1                   # Show GUI for slot 1
effect_show_gui 'colorfx'           # Show ColorFX GUI
effect_show_gui 'vocals' 'echo'     # Show stems FX GUI

# STEMS FX
effect_stems 'vocal'                # Apply to vocals
effect_stems 'melorhythm'           # Apply to instruments
effect_stems off                    # Disable stems FX
effect_select 'vocals' 'reverb'     # Load Reverb in the vocal stem FX slot

# PAD FX
padfx 'echo' 50% 1bt                # Trigger echo
padfx_single 'echo out' 80% 1bt     # One-shot echo out
padfx 'reverb' 75% 'stemfx:vocal'   # Reverb on vocals

# MASTER FX
deck master effect_select 1 'reverb'
deck master effect_active 1
deck master effect_slider 1 1 50%

# VIDEO FX
deck master video_fx_select 'spectral'
deck master video_fx
deck master video_fx_slider 1 50%
video_transition_select 'fade'
video_transition 1000ms

# ADVANCED FX HELPERS
effect_bank_save 1                  # Save deck FX slots 1-6 to bank 1
effect_bank_load 1                  # Load deck FX bank 1
effect_3slots_layout                # Toggle 1-slot / 3-slot layout
effect_releaseslider_active 50%     # Move release-FX slider and activate
effect_fxsendreturnenable           # Enable/query send-return path

# QUERIES
effect_active 1                     # Is slot 1 active?
effect_active 1 'echo out'          # Is Echo Out active in slot 1?
effect_stems                        # Is stems FX active?
get_effect_name 1                   # Get name of effect in slot 1
get_effect_slider_count             # Count sliders in the current FX context
get_effect_button_count             # Count buttons in the current FX context
filter_label                        # Get ColorFX name
effect_mixfx_select                 # Get selected Mix FX name
get_videofx_name                    # Get selected video FX name
is_releasefx                        # Is the release-FX slot/state active?
```

### Common Effect Values

**Strength/Dry-Wet:**

- 0% = No effect
- 50% = Half mix
- 100% = Full effect

**Beat Values:**

- `0.25bt` = 1/4 beat
- `0.5bt` = 1/2 beat
- `1bt` = 1 beat
- `2bt` = 2 beats
- `4bt` = 1 bar

**Time Values:**

- `100ms` = 0.1 seconds
- `500ms` = 0.5 seconds
- `1000ms` = 1 second

---

## Summary

VirtualDJ's effect system is powerful and flexible:

1. **ColorFX** - Quick one-knob filter/effects
2. **Mix FX** - Crossfader-linked transition effects
3. **Deck FX Slots** - Full multi-parameter effects (3-6 slots)
4. **Master FX** - Global effects on master output
5. **Video FX** - Visual effects and transitions
6. **Stems FX** - Effects on individual stems
7. **Pad FX** - Quick-trigger preset effects

**Key Principles:**

- Effects can be controlled by **slot number** or **by name**
- FX1-FX6 are persistent rack state; Pad FX and named stem FX slots are volatile performance state
- **Pre-fader** is default and recommended for most use cases
- **Stems FX** requires pre-fader processing
- **ColorFX** is always pre-fader (integrated with EQ engine)
- **Mix FX** is selected with `effect_mixfx_select` and toggled with `effect_mixfx_activate`; test direct selection queries before using them for skin state
- Effects can be **chained** for creative combinations
- Use **variables** to track complex effect states

**Best Practices:**

- Organize effects into custom lists
- Learn your most-used effects thoroughly
- Use Stems FX for creative vocal/instrument manipulation
- Combine Pad FX with variables for complex workflows
- Check `resetFXOnLoad` option to avoid effect carryover
- Test effects with different audio material

This guide covers the core effect engines in VirtualDJ. Experiment with combinations to develop your signature sound!
