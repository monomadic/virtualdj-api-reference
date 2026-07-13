# Effects Usage

A mental model for **VirtualDJ's different FX engines** and how to drive them from **skins** and **pad pages** without fighting the scripting model.

> Companion docs: [Effects Engines.md](Effects%20Engines.md) is the deep per-engine control reference (7 engines, verbs, patterns); [Native Effects.md](Native%20Effects.md) is the effect-name catalog. Start here for the mental model, go there for details.

---

## 0) The 3 FX “engines” you’ll interact with in skins

VirtualDJ has multiple effect systems that look similar in the UI, but are controlled differently in VDJScript:

1. **Deck FX Slots (Audio FX rack)**  
   Think “FX1/FX2/FX3 on a deck” (and sometimes Master FX).  
   - Select an effect into a slot
   - Turn slot on/off
   - Move parameter sliders

2. **ColorFX (aka the Filter engine)**  
   Think “the filter knob, but instead of just HP/LP it can be Echo/Noise/etc.”  
   - Select which ColorFX preset is attached
   - Drive the **amount** (`filter`), which effectively turns it on/off

3. **Video FX / Video Transitions / Visualizations**  
   Similar concepts but different targets (video decks, master video output, transitions between sources).

Most “why doesn’t this work?” moments happen when you use **deck FX slot verbs** on **ColorFX**, or vice versa.

---

## 1) Canonical control patterns (cheat sheet)

### A) Deck FX Slots (Audio FX rack)

You control **a slot**, not “an effect name globally”.

Name-based shortcuts such as `effect_active 'Echo'` are valid, but they are ambiguous as reference examples: they do not say which FX slot owns the effect, which sliders the pad is preparing, or whether the pad LED is reporting the visible rack state. Use them for quick personal shortcuts; use slots for copyable pad pages and controller mappings.

Use numbered deck FX slots 1-6 for supported slot-based examples. The manual exposes an `FX x6` view, hardware manuals describe six VirtualDJ FX slots, and `effect_bank_save` / `effect_bank_load` explicitly save/load deck FX slots 1 to 6.

**Typical pattern**
- choose effect in slot
- activate slot
- set sliders

Example (slot-based):
```vdjscript
effect_select 1 'Echo'
effect_active 1 on
effect_slider 1 1 50%
effect_slider 1 2 1bt
```

Toggle slot 1

```vdjscript
effect_active 1
```

Query if slot 1 is active

```vdjscript
effect_active 1 ? ...
```

Slot numbers and exact variants can differ across contexts (deck vs master), but the concept is always “slot owns activation + params”.

For pad pages there are three clean slot designs:

- Dedicated slot pads: each pad owns a different slot, so several effects can stay active together.
- Shared slot preset pads: many pads program the same slot, so the pads act as an effect picker with known parameter presets.
- Multi-effect slot pads: several pads intentionally share one slot, but use `effect_select_multi` so earlier effects stay loaded/active in that slot.

When a pad label names a specific effect, its query should check `get_effect_name <slot>` first, then nest the slot active check:

```vdjscript
get_effect_name 1 & param_lowercase & param_equal 'echo' ?
  effect_active 1 ? blink 500ms : off :
  off
```

Do not use bare `effect_select 1` for this check; in pad actions it can open the selector popup. Use `effect_select 1 'Echo'` only when loading Echo into the slot.

Turn a slot effect off with the slot activation verb:

```vdjscript
effect_active 1 off
```

For a same-pad toggle, use nested conditionals:

```vdjscript
get_effect_name 1 & param_lowercase & param_equal 'echo' ?
  effect_active 1 ?
    effect_active 1 off :
    effect_slider 1 1 75% & effect_slider 1 2 50% & effect_active 1 on :
  effect_select 1 'Echo' & effect_slider 1 1 75% & effect_slider 1 2 50% & effect_active 1 on
```

Official VDJScript documents `&&` for query chains, where the query should return true only when both commands are true. That is narrower than using `&&` inside complex pad action branches. Use nested conditionals for same-pad toggle actions, and keep `&&` to simple query expressions you have verified in the target surface.

For multiple effects in one slot, use `effect_select_multi` and query/toggle the named effect instance:

```vdjscript
effect_select_multi 1 'Echo Out' & effect_active 1 'Echo Out'
effect_select_multi 1 'Reverb' & effect_active 1 'Reverb'
```

### A.1) Stem FX Slots

Stems FX has three control paths that are easy to mix up:

- `effect_stems 'vocal'` routes the normal FX rack to a stem or stem group.
- `padfx 'reverb' 'stemfx:vocal'` triggers a pad effect on a stem.
- Named stem FX slots such as `vocals`, `bass`, `instru`, `rhythm`, `melody`, `hihat`, and `kick` can be used as the slot target for `effect_*` actions.

Example named vocal slot:

```vdjscript
effect_select 'vocals' 'Reverb'
effect_active 'vocals'
effect_slider 'vocals' 1 50%
effect_slider 'vocals' 'echo' 1 50%
effect_show_gui 'vocals' 'Reverb'
effect_select_multi 'vocals' 'Echo Out'
effect_active 'vocals' 'Echo Out'
```

Use `effect_select_multi 'vocals' '<effect>'` plus `effect_active 'vocals' '<effect>'` when several vocal effects should live on the same named vocal slot with separate pad LEDs. Use `vocals` for the separate vocal effect slot, but `stemfx:vocal` for the `padfx` stem target. `melovocal` and `melorhythm` may exist but still need local testing. Source: `Official`, `Official forum`, `Community`, `Local test`.

⸻

### B) ColorFX (Filter engine)

ColorFX is controlled by `filter_selectcolorfx` plus the deck `filter` amount.
Official VDJScript documents `filter_selectcolorfx` as the selector and `filter`
as center-off at `50%`.

Select which ColorFX

```vdjscript
filter_selectcolorfx 'Echo'
```

Set amount / reset to neutral

```vdjscript
filter 75%     // apply effect above center
filter 25%     // apply effect below center
filter 50%     // neutral, no effect
```

Activate/deactivate the ColorFX slot when you need an explicit on/off state

```vdjscript
effect_active 'colorfx' on
effect_active 'colorfx' off
```

Select + apply a deterministic amount

```vdjscript
filter_selectcolorfx 'Echo' & effect_active 'colorfx' on & filter 75%
```

Query: is this ColorFX selected and active?

```vdjscript
param_equal `filter_label 'name'` 'Echo' ? (effect_active 'colorfx' ? blink 500ms : off) : off
```

Don’t use effect_active with a ColorFX name. Treat ColorFX as “selected preset + amount”.

⸻

C) “Filter” vs “ColorFX” naming confusion
	•	filter is the amount control for the ColorFX engine.
	•	filter_selectcolorfx chooses which ColorFX preset the filter amount is driving.

So “turning ColorFX on” usually means selecting the preset, enabling the ColorFX slot if needed, and moving `filter` away from `50%`, not activating an effect by name.

⸻

2) How this maps into skins + pad pages

A) XML: where logic belongs
	•	Action body: what happens when you press the pad/button
	•	query=: what the UI uses to decide selected/down/blink/visibility
	•	color= / name text: can be dynamic depending on control type, but keep it simple first

Common gotchas:
	•	Use param_equal, not random compare verbs.
	•	Don’t quote backticked expressions ('…' turns them into literal strings).
	•	Always include the else side of ternaries in query (? ... : off) to avoid empty/undefined UI state.

⸻

B) Canonical pad patterns

1) “Select Echo ColorFX and apply it”

```
<pad1
  name="Echo"
  query="param_equal `filter_label 'name'` 'Echo' ? (effect_active 'colorfx' ? blink 500ms : off) : off"
>
  filter_selectcolorfx 'Echo' &amp; effect_active 'colorfx' on &amp; filter 75%
</pad1>

2) “Momentary ColorFX (hold = on, release = off)”
Use the down ? ... : ... pattern:

<pad1
  name="Echo (hold)"
  query="param_equal `filter_label 'name'` 'Echo' ? (effect_active 'colorfx' ? on : off) : off"
>
  down ? filter_selectcolorfx 'Echo' &amp; effect_active 'colorfx' on &amp; filter 75% : filter 50% &amp; effect_active 'colorfx' off
</pad1>

3) “Deck FX slot: Echo toggle on slot 1”

<pad1
  name="Echo FX1"
  query="effect_active 1 ? blink 500ms : off"
>
  effect_select 1 'Echo' &amp; effect_active 1
</pad1>
```

⸻

3) Audio Effects (native) — organized by how you usually use them

The lists below are still useful, but the control approach depends on whether you’re using FX slots or ColorFX.

Time & Rhythm (mostly FX slot-friendly)

Effect	Typical Use
BackSpin / VinylBrake / Brake	Turntable-style stops/backs
Slicer / BeatGrid / Recycler	Beat-chopping rhythmic FX
Loop Roll / Slip Roll	Temporary looping w/ release
Stutter Out	Exit/transition stutter
Riser / Scale Down	Build-ups / drops

Delay & Echo (FX slots + sometimes ColorFX variants)

Effect	Typical Use
Echo / MT Delay / Ping Pong	Transition tails, rhythmic repeats
Hold Echo	Freeze-style echo
Ducking Echo	Cleaner echo in busy mixes
Pitch/Up/Down Echo	Hype FX / ear-candy

Modulation

Effect	Typical Use
Flanger / Phaser	Sweeps, movement
Pan	Space / stereo motion
LFO Filter	Automated filtering

Filter-family

Effect	Typical Use
Filter (ColorFX)	HP/LP or ColorFX engine (depending on selection)
Wahwah / Sweep	Movement filter FX
Pumper / Rider	Sidechain-ish groove

Special / Utility

Effect	Typical Use
Reverb	Space, tail
Mute / Cut	Gates / kills
Stems / Vocals	Stem-scoped processing when mapped that way


⸻

4) Video Effects + Transitions (how to think about them)

Video has the same conceptual split as audio:
	•	“effects” applied to a source (a video deck, a camera input, etc.)
	•	“transitions” applied between sources

Video Effects

Transforms (post-processing)

Effect	Typical Use
Blur / Negative / Colorize	Looks + masking
Shake / Strobe	Energy / accent
Boom / Boom Auto	Beat zooms

Overlays (rendered on top)

Effect	Typical Use
Lyrics / Karaoke / Text / Title	UI overlays
Screen Grab	live capture overlay

Sources (generate video)

Effect	Typical Use
Camera	live input
Slideshow / Cover	media-driven visuals
Shader	custom pipeline

Video Transitions

Transition	Typical Use
Fade / Additive	clean blend
Cube / Doors / Blinds	obvious visual transitions
Dissolves / Droplets	texture transitions


⸻

5) Effect parameters: how to approach them in skins

A) Think in “presets” for pad pages

Pads want repeatable results. Instead of exposing 4 sliders, hardcode a “good preset”:

Example: “Echo 1bt, medium feedback”

effect_select 1 'Echo'
& effect_active 1 on
& effect_slider 1 1 50%
& effect_slider 1 2 1bt
& effect_slider 1 3 35%

B) For generic skin controls, ask the selected effect what it exposes

```vdjscript
effect_has_slider 1 1
get_effect_slider_label 1 1
get_effect_slider_text 1 1
get_effect_slider_default 1 1 0.5
effect_has_button 1
get_effect_button_shortname 1
```

Built-in skins use these helpers for deck FX, video FX, and transition controls. Use hardcoded parameter labels for known pad presets, not for a reusable FX panel.

C) Make the UI reflect state reliably
		•	FX slot: query effect_active <slot>
		•	ColorFX: query ``param_equal `filter_label 'name'` '<name>' ? (effect_active 'colorfx' ? on : off) : off``
		•	If you care about “which one is selected”, query label/name (when available) but avoid brittle string compares unless you’ve verified the exact returned label.

D) Avoid “half-on” UX

If you toggle ColorFX by amount, decide what “on” means:
		•	filter 50% is neutral
		•	filter 75% or 25% are deterministic on-values in opposite directions
		•	you can store/restore a previous amount using vars, but keep it deterministic for pads

⸻

6) Pre-fader vs post-fader (why skins should care)

This affects how tails behave when you cut volume/crossfader.
	•	Pre-fader: FX continues even if you cut audio? depends on routing; often tails are less “natural”
	•	Post-fader: more “DJ mixer-like” tails when cutting volume

If you’re designing pads for transitions (Echo Out, Reverb Out), you want to know what the user’s fxProcessing option implies.

⸻

7) Stems FX (mental model)

Stems adds a targeting layer (vocal/bass/etc.) to whatever control scheme you’re using.
In pad design:
	•	Decide if the pad affects whole mix or a stem
	•	Make the UI show “has stems / stems ready” so pads don’t feel broken

PadFX stem targets use a different target string than named stem FX slots:

```vdjscript
padfx 'echo' 50% 1bt 65% 75% 'stemfx:vocal'
padfx_single 'echo out' 80% 1bt 'stemfx:vocal'
effect_disable_all 'padfx'
```

`padfx` does not expose a native active-state query in the local examples, so momentary pad pages usually track visual state with variables. It also does not provide private per-pad ownership: another pad that calls the same effect/stem target can alter that active pad-FX identity's parameters. Keep `effect_disable_all 'padfx'` as a separate cleanup/reset action; user-provided testing found that chaining it immediately before fresh `padfx` calls can prevent those new effects from activating or lighting.

⸻

8) Advanced FX surfaces to document carefully

These are real VDJScript areas, but they should not be mixed into ordinary pad examples unless the page actually needs that workflow.

FX banks:

```vdjscript
effect_bank_save 1
effect_bank_load 1
```

Use banks for rack snapshots. Use explicit `effect_select` / `effect_slider` macros for repeatable pad presets.

Release FX:

```vdjscript
effect_releaseslider 50%
effect_releaseslider_active 50%
is_releasefx ? on : off
```

Treat this as its own release-FX path, not a normal deck slot slider.

Armed FX:

```vdjscript
effect_arm_deck master
effect_arm_select 'Echo'
effect_arm_slot 1
effect_arm_active
```

Use this for hardware/controller style "arm target, then activate" workflows. In pad pages, direct slot verbs are usually clearer.

Video FX:

```vdjscript
video_fx_select 'Blur'
video_fx
video_fx_slider 1 50%
video_transition_select 'Fade'
video_transition 1000ms
```

Video effects, sources, and transitions are related but separate paths. Use `deck master video_fx...` when targeting master video output.

Dynamic FX controls:

```xml
<slider action="effect_slider 1 1"
        dblclick="effect_slider_reset 1 1"
        disabled="not effect_has_slider 1 1"
        frommiddle="get_effect_slider_default 1 1 0.5"/>
<text action="get_effect_slider_label 1 1"/>
<button action="effect_button 1"
        visibility="effect_has_button 1"
        textaction="get_effect_button_shortname 1"/>
```

Use this pattern for generic panels where the selected plugin can change. Record effect-specific presets separately.

Current local evidence is not a full introspection table yet. The recorded run for [Reference - FX Introspection Test.xml](../Test/Pads/Reference%20-%20FX%20Introspection%20Test.xml) on VirtualDJ `v2026-m b9336` only confirms that Flanger loaded in deck FX slot 1 and its GUI showed `Strength 50%`, `Speed 8bt`, `Tone n/a`, `Feedback 50%`, and `LFO AMP 40%`. Counts, `effect_has_*` states, button labels, slider labels, defaults, and formatted text readbacks remain unknown until the shift-log pads are recorded.

Plugin commands:

```vdjscript
effect_command 'set 00'
effect_command 'get 00'
```

Treat `effect_command` strings as plugin-specific. BeatGrid-style commands are evidence for BeatGrid, not a universal command language.

⸻

9) Practical design rules for skins & pad pages
	1.	Pick your engine first
“Is this a ColorFX moment or an FX-slot moment?”
	2.	Pads should be deterministic
Avoid relying on whatever effect happens to already be loaded unless that’s intentional.
	3.	Always write query like it’s a state machine
... ? blink 500ms : off (don’t leave it empty)
	4.	Keep selection separate from activation
	•	FX slots: select effect vs activate slot
	•	ColorFX: select preset vs set amount
	5.	Don’t mix verbs between engines
If it feels like “it should work”, it’s probably the wrong engine.

⸻

Additional Resources
	•	VirtualDJ Skin SDK: https://www.virtualdj.com/wiki/Skin%20SDK
	•	VDJScript verbs reference: https://virtualdj.com/manuals/virtualdj/appendix/vdjscriptverbs.html
	•	Script params/variables/math: https://virtualdj.com/forums/251658/General_Discussion/Script_Param_Variable_Maths.html
	•	Plugins directory: https://virtualdj.com/plugins/
