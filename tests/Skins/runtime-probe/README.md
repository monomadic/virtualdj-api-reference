# Runtime skin probes

Skins served to VirtualDJ at runtime by the `VDJIntrospectSkin` plugin
(`tools/plugin/build.sh --skin --install`). The plugin re-reads its `skin.xml` on
every `OnGetUserInterface` call, so these are swapped in without a rebuild:

```sh
just plugin-skin-prepare tests/Skins/runtime-probe/<file>.xml
just plugin-skin-reload      # close + re-open the effect panel
just plugin-skin-log         # confirm VirtualDJ asked again
```

Results are recorded in the tracker's runtime-skin section.

> ## Two of these crash VirtualDJ
>
> `placeholder-condition.xml` and `condition-starred.xml` both instantiate a
> visual class onto a `<group>` (`<group class="..."/>`). Each took VirtualDJ down
> within about a second of the panel opening, and it relaunched itself as
> `VirtualDJ recover`. **They are kept deliberately** — they are the reproduction
> for that hazard — but do not load either one while anything is playing, and
> expect to restart the app afterwards. `just plugin-skin-prepare` with no
> argument restores the safe probe skin.
>
> Everything else here is safe and renders.

| File | Question | Safe? |
| --- | --- | --- |
| `placeholder-text.xml` | starred vs unstarred placeholder in `format=""` | yes |
| `placeholder-text-attr.xml` | the same through `text=""` | yes |
| `group-condition.xml` | does `<group>` / `condition=""` work with no `<define>` | yes — `<group>` renders nothing |
| `visibility-condition.xml` | starred placeholder inside a `visibility=""` condition | yes — this is the one that answered it |
| `placeholder-condition.xml` | first condition attempt, via `<group class="...">` | **CRASHES** |
| `condition-starred.xml` | second condition attempt, still via `<group class="...">` | **CRASHES** |

Each canary carries a row that must always render ("0 control") and, where a
condition is involved, a row that must *not* render. That way "nothing appeared"
is distinguishable from "the panel never opened", and an ignored condition is
distinguishable from an evaluated one.
