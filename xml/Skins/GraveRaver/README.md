# GraveRaver Build Demo

This skin source is intentionally minimal. It is not a design reference and it
is not meant to model a complete VirtualDJ skin.

Use this folder to study the build system:

- `src/skin.xml` is the source entry point.
- `src/partials/*.xml` are small XInclude modules.
- `just lint` validates the source with XInclude enabled.
- `just build` writes a flattened installable `build/skin.xml`.
- `just install` copies the flattened skin and assets into VirtualDJ's skin
  folder.

VirtualDJ reads the flattened `skin.xml`, not this multi-file source tree.
