set shell := ["zsh", "-eu", "-o", "pipefail", "-c"]

skin_name := "DeathDisco Grave Raver v1"
src_dir := "src"
assets_dir := "assets"
build_dir := "build"

default: install

lint:
    xmllint --noout --xinclude "{{src_dir}}/skin.xml"

build: lint
    mkdir -p "{{build_dir}}"
    if [[ -d "{{assets_dir}}" ]]; then rsync -a --delete "{{assets_dir}}/" "{{build_dir}}/"; fi
    xmllint --format --xinclude "{{src_dir}}/skin.xml" --output "{{build_dir}}/skin.xml"

install: build
    install_root="$HOME/Library/Application Support/VirtualDJ/Skins"; \
    install_path="$install_root/{{skin_name}}"; \
    mkdir -p "$install_path"; \
    if [[ -d "{{assets_dir}}" ]]; then rsync -a --delete "{{assets_dir}}/" "$install_path/"; fi; \
    cp -f "{{build_dir}}/skin.xml" "$install_path/skin.xml"

watch:
    watchexec \
      --clear \
      --watch "{{src_dir}}" \
      --watch "{{assets_dir}}" \
      --exts xml,png,jpg,jpeg,bmp,svg \
      --ignore "{{build_dir}}" \
      --ignore .git \
      -- just install

clean:
    rm -rf "{{build_dir}}"
