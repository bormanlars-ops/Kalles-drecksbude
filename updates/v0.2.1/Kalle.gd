extends Node2D
## Kalle 0.2.1 - corrected anatomical left/right shoulder attachment.

signal arrived

const SPEED: float = 133.0
const MIN_X: float = 155.0
const MAX_X: float = 1150.0
var target_x: float = 690.0
var traveling: bool = false
var mood: String = "idle"
var clock: float = 0.0
var stride_phase: float = 0.0
var gait_strength: float = 0.0
var parts: Dictionary = {}
var facing_right: bool = true

# Floor-relative positions. Arms attach high on the torso, boots follow each leg.
const BASE: Dictionary = {
    "leg_left": Vector2(-21, -92),
    "leg_right": Vector2(23, -92),
    "boot_left": Vector2(-30, -23),
    "boot_right": Vector2(34, -23),
    "body": Vector2(0, -200),
    # Anatomical: Kalle faces the camera; HIS left is screen-right.
    "arm_left": Vector2(57, -232),
    "arm_right": Vector2(-57, -232),
    "head": Vector2(-3, -294)
}

func _ready() -> void:
    _part("leg_left", "leg_a", BASE["leg_left"], Vector2(0.225, 0.225), -2)
    _part("leg_right", "leg_b", BASE["leg_right"], Vector2(0.225, 0.225), -1)
    _part("boot_left", "boot", BASE["boot_left"], Vector2(0.115, 0.115), -1)
    _part("boot_right", "boot", BASE["boot_right"], Vector2(0.115, 0.115), 1)
    _part("arm_right", "arm", BASE["arm_right"], Vector2(0.198, 0.198), 1)
    _part("body", "body", BASE["body"], Vector2(0.34, 0.34), 0)
    _part("arm_left", "arm", BASE["arm_left"], Vector2(0.198, 0.198), -1)
    _part("head", "head", BASE["head"], Vector2(0.265, 0.265), 2)
    # Texture center is not the shoulder, so move local origin near attachment point.
    (parts["arm_left"] as Sprite2D).offset = Vector2(15, 85)
    (parts["arm_right"] as Sprite2D).offset = Vector2(15, 85)
    target_x = position.x

func _part(key: String, filename: String, pos: Vector2, size: Vector2, depth: int) -> void:
    var sprite: Sprite2D = Sprite2D.new()
    sprite.name = key
    sprite.texture = load("res://assets/characters/%s.png" % filename) as Texture2D
    sprite.position = pos
    sprite.scale = size
    sprite.z_index = depth
    sprite.texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR
    if key == "arm_right":
        # The single source sleeve points right; mirror ONLY the screen-left sleeve.
        sprite.flip_h = true
    add_child(sprite)
    parts[key] = sprite

func walk_to(x: float) -> void:
    target_x = clampf(x, MIN_X, MAX_X)
    traveling = absf(target_x - position.x) > 6.0
    if traveling:
        facing_right = target_x > position.x
        scale.x = 1.0 if facing_right else -1.0
        mood = "walk"
    else:
        mood = "idle"
        arrived.emit()

func emote(which: String) -> void:
    if not traveling:
        mood = which

func _process(delta: float) -> void:
    clock += delta
    var was_traveling: bool = traveling
    if traveling:
        position.x = move_toward(position.x, target_x, SPEED * delta)
        if absf(target_x - position.x) <= 1.0:
            position.x = target_x
            traveling = false
            mood = "idle"
    gait_strength = move_toward(gait_strength, 1.0 if traveling else 0.0, delta * 3.6)
    stride_phase += delta * 7.6 * gait_strength
    var s: float = sin(stride_phase)
    var opposite: float = -s
    var w: float = gait_strength

    # Two coherent step phases. Feet follow the same leg phase; no separate wild sine.
    (parts["leg_left"] as Sprite2D).position = BASE["leg_left"] + Vector2(s * 4.0 * w, -maxf(0.0, s) * 3.0 * w)
    (parts["leg_right"] as Sprite2D).position = BASE["leg_right"] + Vector2(opposite * 4.0 * w, -maxf(0.0, opposite) * 3.0 * w)
    (parts["leg_left"] as Sprite2D).rotation = s * 0.055 * w
    (parts["leg_right"] as Sprite2D).rotation = opposite * 0.055 * w
    (parts["boot_left"] as Sprite2D).position = BASE["boot_left"] + Vector2(s * 4.8 * w, -maxf(0.0, s) * 6.0 * w)
    (parts["boot_right"] as Sprite2D).position = BASE["boot_right"] + Vector2(opposite * 4.8 * w, -maxf(0.0, opposite) * 6.0 * w)
    (parts["boot_left"] as Sprite2D).rotation = s * 0.018 * w
    (parts["boot_right"] as Sprite2D).rotation = opposite * 0.018 * w

    # Torso and head barely move: weight and breathing, not jitter.
    var breathe: float = sin(clock * 1.6) * 0.6 * (1.0 - w)
    (parts["body"] as Sprite2D).position = BASE["body"] + Vector2(0.0, -absf(s) * 1.1 * w + breathe)
    (parts["head"] as Sprite2D).position = BASE["head"] + Vector2(0.0, breathe * 0.7 - absf(s) * 0.7 * w)
    (parts["head"] as Sprite2D).rotation = s * 0.006 * w

    var left_arm: float = s * 0.065 * w
    var right_arm: float = -s * 0.065 * w
    if not traveling:
        if mood == "angry":
            left_arm = -0.28
            right_arm = 0.28
            (parts["head"] as Sprite2D).rotation = -0.035
        elif mood == "dance":
            left_arm = -0.28 + sin(clock * 3.0) * 0.09
            right_arm = 0.28 - sin(clock * 3.0) * 0.09
            (parts["head"] as Sprite2D).rotation = sin(clock * 2.5) * 0.02
    (parts["arm_left"] as Sprite2D).rotation = left_arm
    (parts["arm_right"] as Sprite2D).rotation = right_arm

    if was_traveling and not traveling:
        arrived.emit()
