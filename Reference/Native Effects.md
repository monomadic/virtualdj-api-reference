# VirtualDJ Native Effects Reference

Comprehensive list of all native audio and video effects, video transitions, and visualizations included with VirtualDJ.

## Audio Effects

### Time & Rhythm Effects

| Effect             | Description                                            |
| ------------------ | ------------------------------------------------------ |
| **BackSpin**       | Simulates a vinyl record spinning backward             |
| **Beat Brake**     | Applies a brake/slowdown effect synchronized to beats  |
| **BeatGrid**       | Beat-synchronized slicer effect using the beatgrid     |
| **Brake**          | Simulates slowing down/stopping like a turntable brake |
| **Break Start**    | Jump start effect for track beginnings                 |
| **Flippin Double** | Doubles every beat for rapid-fire transitions          |
| **Loop Out**       | Creates a loop that fades out                          |
| **Loop Roll**      | Temporary loop that releases back to original position |
| **Mobius**         | Continuous reverse/forward time manipulation           |
| **Mobius Saw**     | Sawtooth wave time manipulation effect                 |
| **Mobius Tri**     | Triangle wave time manipulation effect                 |
| **Recycler**       | Rhythmic stuttering and repeat effect                  |
| **Riser**          | Pitch rise effect typically used for buildups          |
| **Scale Down**     | Pitch-shift down effect                                |
| **Scratch DNA**    | Automated scratch patterns                             |
| **Slicer**         | Chops audio into rhythmic slices                       |
| **Slip Roll**      | Loop roll effect in slip mode                          |
| **Spiral**         | Spiraling time manipulation effect                     |
| **Stutter Out**    | Stuttering effect that fades out                       |
| **VinylBrake**     | Vinyl-style brake effect with customizable parameters  |

### Delay & Echo Effects

| Effect           | Description                                          |
| ---------------- | ---------------------------------------------------- |
| **Down Echo**    | Echo with pitch-shifting downward                    |
| **Ducking Echo** | Echo that ducks the dry signal                       |
| **Echo**         | Standard delay/echo effect with beat synchronization |
| **Hold Echo**    | Echo that holds and repeats a section                |
| **Low Cut Echo** | Echo with high-pass filtering                        |
| **MT Delay**     | Multi-tap delay effect                               |
| **Pitch Echo**   | Echo with pitch shifting                             |
| **Rev Delay**    | Reverse delay effect                                 |
| **Up Echo**      | Echo with pitch-shifting upward                      |

### Modulation Effects

| Effect         | Description                                |
| -------------- | ------------------------------------------ |
| **Cyclone**    | Rotating modulation effect                 |
| **Flanger**    | Classic flanging effect with feedback      |
| **Helix**      | Spiral modulation effect                   |
| **LFO Filter** | Low-frequency oscillator controlled filter |
| **Matrix**     | Complex modulation matrix                  |
| **Pan**        | Auto-panning effect                        |
| **Phaser**     | Classic phaser effect with multiple stages |
| **Ping Pong**  | Ping-pong delay/echo effect                |

### Filter Effects

| Effect     | Description                                   |
| ---------- | --------------------------------------------- |
| **Filter** | Resonant high-pass/low-pass filter (Color FX) |
| **Pumper** | Rhythmic volume pumping/ducking effect        |
| **Sweep**  | Filter sweep effect                           |
| **Wahwah** | Auto-wah effect                               |

### Pitch & Tone Effects

| Effect         | Description                             |
| -------------- | --------------------------------------- |
| **Distortion** | Adds distortion/overdrive to the signal |
| **Noise**      | Noise generator effect                  |
| **Pitch**      | Pitch shifting effect                   |
| **Pitch Down** | Dedicated pitch-down effect             |

### Special Effects

| Effect      | Description                           |
| ----------- | ------------------------------------- |
| **Cut**     | Beat-synchronized gate/cutting effect |
| **MergeFX** | Merges/combines effects together      |
| **Mute**    | Mute/unmute effect                    |
| **Reverb**  | Reverb/room ambience effect           |
| **Rider**   | Side-chain style ducking effect       |
| **Stems**   | Stems-based effect processing         |
| **Stretch** | Time-stretching effect                |
| **Vocals**  | Vocal isolation/processing effect     |

## Video Effects

### Transforms

| Effect              | Description                          |
| ------------------- | ------------------------------------ |
| **Blur**            | Blurs the video output               |
| **Blur Black Bars** | Blur with black bars overlay         |
| **Boom**            | Zoom/boom effect                     |
| **Boom Auto**       | Automatic zoom synchronized to beats |
| **Colorize**        | Changes video colors/hue             |
| **Negative**        | Inverts video colors                 |
| **Shake**           | Camera shake effect                  |
| **Spectral**        | Spectral visualization effect        |
| **Strobe**          | Strobe light effect                  |

### Overlays

| Effect          | Description             |
| --------------- | ----------------------- |
| **Karaoke**     | Karaoke display overlay |
| **Lyrics**      | Lyrics text overlay     |
| **Screen Grab** | Screen capture overlay  |
| **Text**        | Custom text overlay     |
| **Title**       | Title card overlay      |

### Sources

| Effect        | Description                  |
| ------------- | ---------------------------- |
| **Camera**    | Webcam/camera input source   |
| **Cover**     | Album cover art display      |
| **Lottery**   | Random visual lottery/picker |
| **Shader**    | Custom shader effects        |
| **Slideshow** | Image slideshow display      |

## Video Transitions

| Transition         | Description                     |
| ------------------ | ------------------------------- |
| **Additive**       | Additive blending transition    |
| **Blinds**         | Venetian blinds wipe            |
| **Cloud Dissolve** | Cloud-based dissolve            |
| **Color Swap**     | Color channel swap transition   |
| **Cube**           | 3D cube rotation transition     |
| **Doors**          | Door opening/closing transition |
| **Drain**          | Drain effect transition         |
| **Drain Light**    | Lighter drain effect            |
| **Droplets**       | Water droplet transition        |
| **Extreme Cut**    | Hard cut with effects           |
| **Fade**           | Standard crossfade              |
| **Fixed Grid**     | Grid-based transition           |

## Effect Parameters

Most effects support multiple parameters that can be adjusted:

### Common Parameters

1. **Strength/Dry-Wet** - Controls effect intensity (usually 0-100%)
2. **Length/Speed** - Controls timing, usually in beats (e.g., 1bt, 2bt, 4bt)
3. **Feedback** - Controls effect repetition/resonance
4. **Additional Controls** - Effect-specific parameters (filters, stages, modes, etc.)

Use the effect introspection helpers when building a generic control surface:

```vdjscript
effect_has_slider 1 1
get_effect_slider_label 1 1
get_effect_slider_text 1 1
get_effect_slider_default 1 1 0.5
effect_has_button 1
get_effect_button_shortname 1
```

Those helpers are safer than assuming every native effect has the same slider count, button count, labels, or default values.

### Observed Parameter Examples

These examples are known working forms from local reference pad pages and built-in pad pages. They are not a complete native effect parameter map.

**Slot FX presets:**

| Effect | Working form | Source |
| --- | --- | --- |
| Echo | `effect_select 1 'Echo' & effect_slider 1 1 75% & effect_slider 1 2 50%` | `Local test`: `Pads/Reference - Slot FX.xml` |
| Echo Out | `effect_select 1 'Echo Out' & effect_slider 1 1 80% & effect_slider 1 2 50%` | `Local test`: `Pads/Reference - Slot FX.xml` |
| Reverb | `effect_select 2 'Reverb' & effect_slider 2 1 45% & effect_slider 2 2 50%` | `Local test`: `Pads/Reference - Slot FX.xml` |
| Delay | `effect_select 3 'Delay' & effect_slider 3 1 75% & effect_slider 3 2 50%` | `Local test`: `Pads/Reference - Slot FX.xml` |
| Flanger | `effect_select 4 'Flanger' & effect_slider 4 1 50%` | `Local test`: `Pads/Reference - Slot FX.xml` |
| Loop Roll | `effect_select 1 'Loop Roll' & effect_slider 1 1 50%` | `Local test`: `Pads/Reference - Slot FX.xml` |
| Phaser | `effect_select 1 'Phaser' & effect_slider 1 1 50%` | `Local test`: `Pads/Reference - Slot FX.xml` |
| BeatGrid | `effect_select 1 'BeatGrid' & effect_slider 1 1 75%` | `Local test`: `Pads/Reference - Slot FX.xml` |

**PadFX presets:**

| Effect | Working form | Source |
| --- | --- | --- |
| Cut | `padfx 'cut' 50% 0.5bt` | `Local test`: `Pads/PUSH FX.xml` |
| Cut | `padfx 'cut' 40% 1bt` | `Local test`: `Pads/PUSH FX.xml` |
| Flanger | `padfx 'flanger' 70% 1bt` | `Local test`: `Pads/PUSH FX.xml` |
| BeatGrid | `padfx 'beatgrid'` | `Local test`: `Pads/PUSH FX.xml` |
| Echo on vocal stem | `padfx 'echo' 50% 1bt 65% 75% 'stemfx:vocal'` | `Local test`: `Pads/PUSH FX.xml` |
| Reverb on vocal stem | `padfx 'reverb' 55% 2bt 'stemfx:vocal'` | `Local test`: `Pads/PUSH FX.xml` |
| Echo Out on vocal stem | `padfx_single 'echo out' 80% 1bt 'stemfx:vocal'` | `Local test`: `Pads/PUSH FX.xml` |
| Echo Out on vocal stem | `padfx "echo out" 80% 1bt "stemfx:vocal"` | `Built-in pad page`: `pads_stems+fx.xml` |
| Reverb on vocal stem | `padfx "Reverb" 80% "stemfx:vocal"` | `Built-in pad page`: `pads_stems+fx.xml` |
| BeatGrid on instrumental/melorhythm stem | `padfx "Beat Grid" "stemfx:MeloRhythm"` | `Built-in pad page`: `pads_stems+fx.xml` |

These `padfx` forms are good quick-trigger examples, but they do not imply private pad ownership. User-provided local testing found that another pad using the same effect/stem target can alter the active pad-FX parameters, and that `effect_disable_all 'padfx'` should be kept as a separate cleanup action rather than chained immediately before new `padfx` calls.

BeatGrid also has a plugin-specific UI command surface in the built-in plugin XML:

```vdjscript
effect_command 'set 00'
effect_command 'get 00'
effect_command 'cur 0'
```

Treat those strings as BeatGrid-specific until another plugin UI or local test proves otherwise.

## Effect Usage

### VDJScript Control

Effects can be controlled via VDJScript:

```
effect_select 1 'Echo'
effect_slider 1 1 50%
effect_slider 1 2 1bt
effect_active 1 on
```

### Mix FX Routing

Mix FX is not a separate native effect name. It is a crossfader-linked control path that can select native effects for assisted transitions.

Official VDJScript exposes:

```
effect_mixfx_select 'Echo'
effect_mixfx_select 'Loop Roll'
effect_mixfx_activate
```

The Denon Prime 4 Deluxe skin uses Mix FX buttons for:

- Filter
- Echo
- Loop Roll
- Reverb
- Noise

Those names should be treated as native effects/presets usable through the Mix FX selector, not as proof that every native effect is Mix-FX-compatible. Test candidate names in VirtualDJ and record results in `Published Skin Findings.md`.

### Beat Synchronization

Many effects support beat synchronization:

- `1bt` = 1 beat
- `2bt` = 2 beats
- `4bt` = 4 beats
- Negative values possible for some effects (e.g., `-1bt`)

### Effect Slots

VirtualDJ supports multiple effect slots:

- FX1, FX2, FX3 (deck effects)
- Master FX (master output effects)
- Each slot can have its own effect with independent parameters
- `effect_select_multi` can keep more than one effect instance in the same slot/channel; query/toggle a specific instance with `effect_active <slot> '<effect>'`

## Pre-Fader vs Post-Fader

Effects can be processed:

- **Pre-Fader**: Before volume fader and crossfader (default)
- **Post-Fader**: After volume fader and crossfader (requires supported hardware)

Set in Options: `fxProcessing` - `pre-fader` or `post-fader`

## Stems Effects

Effects can be applied to individual stems:

- Vocal
- HiHat
- Bass
- Instru
- Kick

Activated via Stems FX Pad on the Stems Pad Page.

## Effect Lists

VirtualDJ allows organizing effects into custom lists for easier access:

- Create multiple lists for different genres or use cases
- Manage lists via Audio Effects List Editor
- Access by scrolling to bottom of Effects List and clicking "More..." or "Manage..."

## Notes

- All native effects are included with VirtualDJ (no additional purchase required)
- Additional effects can be downloaded from VirtualDJ's plugin directory
- Effect availability and parameters may vary by VirtualDJ version
- Some effects have graphical user interfaces (GUIs) for advanced parameter control
- Effects can be combined and chained for complex sound design
- Exact slider/button maps are only partially documented locally. Prefer tested examples for effect-specific pad presets, and record new parameter findings with the VirtualDJ build and effect version when possible.

---

## Additional Resources

- **VDJScript Verbs**: See VDJScript reference for programmatic effect control
- **Pads Editor**: Customize pad pages to trigger effects
- **Effect GUIs**: Click effect name or gear icon to open detailed controls
- **VirtualDJ Forums**: Community-created effects and tips
- **Plugin Directory**: https://virtualdj.com/plugins/
