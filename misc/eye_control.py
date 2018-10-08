import eye_mouse
from talon.voice import Word, Context, Key, Rep, Str, press

ctx = Context("eye_control")
ctx.keymap(
    {
        "debug overlay": lambda m: eye_mouse.on_menu(
            "Eye Tracking >> Show Debug Overlay"
        ),
        "control mouse": lambda m: eye_mouse.on_menu("Eye Tracking >> Control Mouse"),
        "camera overlay": lambda m: eye_mouse.on_menu(
            "Eye Tracking >> Show Camera Overlay"
        ),
        "run calibration": lambda m: eye_mouse.on_menu("Eye Tracking >> Calibrate"),
    }
)
