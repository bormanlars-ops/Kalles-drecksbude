#!/usr/bin/env python3
"""Run after v0.2/apply_patch.py; preserve previous APK as parallel install."""
from pathlib import Path
p=Path(__file__).resolve().parent
f=p/"export_presets.cfg"
s=f.read_text(encoding="utf-8")
replacements={
    'package/unique_name="de.boyka.kalle.drecksbude.v02"':'package/unique_name="de.boyka.kalle.drecksbude.v021"',
    'package/name="KALLE Drecksbude 0.2"':'package/name="KALLE Drecksbude 0.2.1"',
    'package/version_code=2':'package/version_code=3',
    'package/version_string="0.2.0"':'package/version_string="0.2.1"',
}
for a,b in replacements.items():
    assert a in s, "Missing preset marker: " + a
    s=s.replace(a,b,1)
f.write_text(s,encoding="utf-8")
print("Applied v0.2.1 package/version hotfix.")
