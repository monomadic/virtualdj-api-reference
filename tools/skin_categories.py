"""Shared editorial categories for skin XML queries and reference navigation.

These labels are navigation metadata, never a claim of parser support or behavior.
Unknown names are intentionally uncategorized so corpus additions remain visible.
"""
from functools import lru_cache
import json
from pathlib import Path
import re

METADATA_PATH = Path(__file__).resolve().parents[1] / "docs" / "skin-element-categories.json"
SKIN_FAMILIES = frozenset(("skins", "video_skins"))


@lru_cache(maxsize=1)
def _metadata():
    return json.loads(METADATA_PATH.read_text(encoding="utf-8"))


def _resolved():
    """Validate metadata structure and return definitions and flattened mappings."""
    data = _metadata()
    definitions = {}
    for definition in data["categories"]:
        identifier = definition["id"]
        if not isinstance(identifier, str) or not re.fullmatch(r"[a-z]+(?:-[a-z]+)*", identifier):
            raise ValueError(f"Invalid skin category ID: {identifier!r}")
        if identifier in definitions:
            raise ValueError(f"Duplicate skin category ID: {identifier}")
        if not isinstance(definition.get("label"), str) or not definition["label"].strip():
            raise ValueError(f"Missing label for skin category: {identifier}")
        definitions[identifier] = {"id": identifier, "label": definition["label"]}
    if "uncategorized" not in definitions:
        raise ValueError("Missing uncategorized skin category")

    def flatten(groups, context):
        mapping = {}
        for identifier, names in groups.items():
            if identifier not in definitions:
                raise ValueError(f"Unknown skin category ID in {context}: {identifier}")
            if not isinstance(names, list):
                raise ValueError(f"Expected element list in {context}: {identifier}")
            for name in names:
                if not isinstance(name, str) or not name:
                    raise ValueError(f"Invalid element name in {context}: {name!r}")
                if name in mapping:
                    raise ValueError(f"Conflicting or duplicate assignment in {context}: {name}")
                mapping[name] = identifier
        return mapping

    shared = flatten(data["assignments"], "shared assignments")
    overrides = {}
    for family, groups in data.get("family_overrides", {}).items():
        if family not in SKIN_FAMILIES:
            raise ValueError(f"Invalid skin category family override: {family}")
        overrides[family] = flatten(groups, family)
    return definitions, shared, overrides


def category(name, family):
    """Return a fresh {id, label} record for a name in an XML family."""
    definitions, shared, overrides = _resolved()
    identifier = "uncategorized"
    if family in SKIN_FAMILIES:
        identifier = overrides.get(family, {}).get(name, shared.get(name, identifier))
    return dict(definitions[identifier])


def categories():
    """Return ordered category definitions, including the unknown-name fallback."""
    definitions, _, _ = _resolved()
    return [dict(definition) for definition in definitions.values()]


def validate(inventory):
    """Raise ValueError for invalid metadata or assignments absent from inventory.

    New inventory names are allowed and resolve to Uncategorized. A shared name
    need only occur in one skin family; an override must occur in its own family.
    """
    _, shared, overrides = _resolved()
    names = {
        family: set(inventory.get("families", {}).get(family, {}).get("elements", {}))
        for family in SKIN_FAMILIES
    }
    stale = set(shared) - set().union(*names.values())
    if stale:
        raise ValueError("Stale shared skin category names: " + ", ".join(sorted(stale)))
    for family, mapping in overrides.items():
        stale = set(mapping) - names[family]
        if stale:
            raise ValueError(f"Stale skin category names for {family}: " + ", ".join(sorted(stale)))
