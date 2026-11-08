#!/usr/bin/env python3
"""After v0.2/apply_patch.py, switch to independently installable v0.2.2."""
from pathlib import Path
project = Path(__file__).resolve().parent
f = project / "export_presets.cfg"
s = f.read_text(encoding="utf-8")
replace = {
    'package/unique_name="de.boyka.kalle.drecksbude.v02"': 'package/unique_name="de.boyka.kalle.drecksbude.v022"',
    'package/name="KALLE Drecksbude 0.2"': 'package/name="KALLE Drecksbude 0.2.2"',
    'package/version_code=2': 'package/version_code=4',
    'package/version_string="0.2.0"': 'package/version_string="0.2.2"',
}
for before, after in replace.items():
    if before not in s:
        raise RuntimeError("Missing expected config: " + before)
    s = s.replace(before, after, 1)
f.write_text(s, encoding="utf-8")
print("Applied Kalle v0.2.2 update: hands attached to jacket sleeves.")
