#!/usr/bin/env python3
"""Apply KALLE – DRECKSBUDE 0.2 changes to the archived 0.1 Godot project."""
from pathlib import Path

project = Path(__file__).resolve().parent
game = project / "scripts" / "Game.gd"
export = project / "export_presets.cfg"
config = project / "project.godot"

def swap(text, before, after):
    if before not in text:
        raise RuntimeError("Expected source marker not found: " + before[:100])
    return text.replace(before, after, 1)

s = game.read_text(encoding="utf-8")
s = swap(s, "var muted: bool = false", "var muted: bool = false\nvar autonomous_pending: bool = false")
s = swap(s, "ambient_countdown = randf_range(10.0, 17.0)", "ambient_countdown = randf_range(3.0, 5.0)")
s = swap(s, 'button.size = Vector2(width, 51)', 'button.size = Vector2(width, 58)')
s = swap(s, 'button.add_theme_font_size_override("font_size", 17)', 'button.add_theme_font_size_override("font_size", 21)')
s = swap(s, 'title.add_theme_font_size_override("font_size", 27)', 'title.add_theme_font_size_override("font_size", 30)')
s = swap(s, 'status_label.add_theme_font_size_override("font_size", 12)', 'status_label.add_theme_font_size_override("font_size", 18)')
s = swap(s, 'speech_panel.position = Vector2(314, 93)', 'speech_panel.position = Vector2(265, 94)')
s = swap(s, 'speech_panel.custom_minimum_size = Vector2(650, 70)', 'speech_panel.custom_minimum_size = Vector2(750, 98)')
s = swap(s, 'speech_label.custom_minimum_size = Vector2(630, 56)', 'speech_label.custom_minimum_size = Vector2(728, 84)')
s = swap(s, 'speech_label.add_theme_font_size_override("font_size", 21)', 'speech_label.add_theme_font_size_override("font_size", 25)')
s = swap(s, 'speech_label.add_theme_color_override("font_color", Color(0.1, 0.08, 0.07))', 'speech_label.add_theme_color_override("font_color", Color(1.0, 0.96, 0.87))')
s = swap(s, 'info_panel.position = Vector2(365, 195)', 'info_panel.position = Vector2(280, 155)')
s = swap(s, 'info_panel.custom_minimum_size = Vector2(550, 330)', 'info_panel.custom_minimum_size = Vector2(720, 410)')
s = swap(s, 'info_label.custom_minimum_size = Vector2(535, 300)', 'info_label.custom_minimum_size = Vector2(700, 385)')
s = swap(s, 'info_label.add_theme_font_size_override("font_size", 22)', 'info_label.add_theme_font_size_override("font_size", 26)')
s = swap(s, 'info_label.add_theme_color_override("font_color", Color(0.1, 0.08, 0.07))', 'info_label.add_theme_color_override("font_color", Color(1.0, 0.96, 0.88))')
s = swap(s, '    speech_panel.add_child(speech_label)', '''    speech_panel.add_child(speech_label)
    var bubble_style: StyleBoxFlat = StyleBoxFlat.new()
    bubble_style.bg_color = Color(0.07, 0.065, 0.058, 0.94)
    bubble_style.border_color = Color(0.89, 0.64, 0.34, 0.94)
    bubble_style.set_border_width_all(2)
    bubble_style.set_corner_radius_all(12)
    speech_panel.add_theme_stylebox_override("panel", bubble_style)''')
s = swap(s, '    info_panel.add_child(info_label)', '''    info_panel.add_child(info_label)
    var info_style: StyleBoxFlat = StyleBoxFlat.new()
    info_style.bg_color = Color(0.06, 0.055, 0.05, 0.98)
    info_style.border_color = Color(0.91, 0.7, 0.43, 1.0)
    info_style.set_border_width_all(3)
    info_style.set_corner_radius_all(12)
    info_panel.add_theme_stylebox_override("panel", info_style)''')
s = swap(s, '    var hint: Label = Label.new()', '''    var footer: ColorRect = ColorRect.new()
    footer.position = Vector2(0.0, 669.0)
    footer.size = Vector2(1280.0, 51.0)
    footer.color = Color(0.035, 0.031, 0.032, 0.88)
    footer.mouse_filter = Control.MOUSE_FILTER_IGNORE
    ui_root.add_child(footer)

    var hint: Label = Label.new()''')
s = swap(s, 'hint.text = "TIPPE AUF KALLE ODER MÖBEL  •  TIPPE AUF DEN BODEN, DAMIT KALLE HINLÄUFT"', 'hint.text = "KALLE ANTIPPEN: REAKTION    •    MÖBEL ANTIPPEN: BENUTZEN    •    BODEN ANTIPPEN: LAUFEN"')
s = swap(s, 'hint.position = Vector2(26, 683)', 'hint.position = Vector2(26, 679)')
s = swap(s, 'hint.size = Vector2(1230, 24)', 'hint.size = Vector2(1230, 32)')
s = swap(s, 'hint.add_theme_font_size_override("font_size", 16)', 'hint.add_theme_font_size_override("font_size", 20)')
s = swap(s, 'hint.add_theme_color_override("font_color", Color(1.0, 0.9, 0.65))', 'hint.add_theme_color_override("font_color", Color(1.0, 0.95, 0.86))')
s = swap(s, '''    var p: Vector2 = get_global_mouse_position()
    # Character hit-testing''', '''    autonomous_pending = false
    ambient_countdown = randf_range(9.0, 14.0)
    var p: Vector2 = get_global_mouse_position()
    # Character hit-testing''')
s = swap(s, '''    pending_object = ""
    _interact_with_object(id)

func _interact_with_kalle''', '''    pending_object = ""
    if autonomous_pending:
        autonomous_pending = false
        _autonomous_interaction(id)
    else:
        _interact_with_object(id)

func _autonomous_interaction(id: String) -> void:
    # Self-directed activities never count as player discoveries.
    match id:
        "tv":
            tv_on = true
            screen_glow.visible = true
            _play("television")
        "radio":
            radio_on = true
            _play("radio")
        "lamp":
            lamp_on = true
            var tint: Color = night_tint.color
            tint.a = 0.17
            night_tint.color = tint
        _:
            _play("tap")
    _say(_random_line(id), 4.4)

func _interact_with_kalle''')
start = s.index('    if ambient_countdown <= 0.0:')
end = s.index('\nfunc _show_collection()', start)
s = s[:start] + '''    if ambient_countdown <= 0.0:
        ambient_countdown = randf_range(5.0, 9.0)
        if not info_panel.visible and pending_object.is_empty() and not bool(kalle.get("traveling")):
            _autonomous_activity()

func _autonomous_activity() -> void:
    # Within seconds Kalle picks a room activity without player input.
    var roll: float = randf()
    if roll < 0.62:
        var options: Array[String] = ["sofa", "tv", "radio", "trash", "window", "lamp", "table"]
        autonomous_pending = true
        _go_to_object(options.pick_random())
    elif roll < 0.92:
        autonomous_pending = false
        (kalle as Node2D).call("walk_to", randf_range(250.0, 1100.0))
    else:
        _say(_random_line("idle"), 4.2)
        (kalle as Node2D).call("emote", "dance")
        _reset_mood_later(2.0)
''' + s[end:]
s = swap(s, '"KALLE – DRECKSBUDE / V0.1', '"KALLE – DRECKSBUDE / V0.2')
s = swap(s, 'status_label.text = "CHAOS: %d   |   GEHEIMNISSE: %d/5   |   EIN RAUM, EINE VERDAMMTE WELT"', 'status_label.text = "CHAOS: %d   |   GEHEIMNISSE: %d/5"')
game.write_text(s, encoding="utf-8")

e = export.read_text(encoding="utf-8")
e = swap(e, 'package/unique_name="de.boyka.kalle.drecksbude"', 'package/unique_name="de.boyka.kalle.drecksbude.v02"')
e = swap(e, 'package/version_code=1', 'package/version_code=2')
e = swap(e, 'package/version_string="0.1.0"', 'package/version_string="0.2.0"')
e = swap(e, 'package/name="KALLE Drecksbude"', 'package/name="KALLE Drecksbude 0.2"')
export.write_text(e, encoding="utf-8")
print("Applied Kalle 0.2: improved readability, autonomous activity, smoother animation source.")
