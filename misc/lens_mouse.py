"""
Control your mouse cursor with your tobii eye tracker. This is an alternative to the default "Eye Tracking > Control Mouse" method.

It shows a dim circle (that looks kind of like a lens) wherever you look, instead of always moving the mouse cursor where you look. Only when you "click" does it move the mouse cursor to where the circle is, and do a mouse click. I found having the mouse cursor always moving to be distracting, and so prefer this mode.

By default, pressing F3 does the click. I did it this way because I use a separate noise recognition tool to make my clicking sound. You may want to map the click() method in this file to the "pop" sound (see https://github.com/dwiel/talon_community/blob/master/noise/pop.py)
"""

import time
import math

from talon import canvas, ctrl, tap, ui
from talon.track.geom import Point2d, EyeFrame
from talon.track.filter import DwellFilter, LowPassFilter, MultiFilter, OneEuroFilter
from talon.skia import Shader
from talon_plugins.eye_mouse import tracker

screen = ui.main_screen()
size_px = Point2d(screen.width, screen.height)

# Shows crazy circles
def smooth_location():

    # Calculate smooth location of point
    x = mouse.origin.x
    y = mouse.origin.y
    n = 75
    if len(mouse.xy_hist) < n:
        n = len(mouse.xy_hist)
    total = 1
    minimum_group = 4
    for i in range(n):
        x2 = mouse.xy_hist[-1 - i].x
        y2 = mouse.xy_hist[-1 - i].y

        # If there are at least 5 points (so there's some smoothness)
        if i > minimum_group:
            # Don't use if points are really far away, so long moves are fast
            if abs(x2 - mouse.origin.x) > 60:
                continue
            if abs(y2 - mouse.origin.y) > 60:
                continue

        x += x2
        y += y2
        total += 1

    x /= total
    y /= total
    return [x, y]


class LensMouse:
    def __init__(self):

        tracker.register("gaze", self.on_gaze)

        self.xy_hist = [Point2d(0, 0)]
        self.origin = Point2d(0, 0)

        canvas.register("overlay", self.draw)
        self.enabled = True

    def draw(self, canvas):

        if mouse.origin == None:
            print("Is the tobii disconnected?")
            return

        pos = smooth_location()

        # Append the smoothed dot to history > to smooth it some more
        mouse.xy_hist.append(Point2d(pos[0], pos[1]))
        mouse.xy_hist.append(Point2d(pos[0], pos[1]))

        if pos == None:
            return

        paint = canvas.paint

        paint.stroke_width = 1
        paint.style = paint.Style.STROKE
        paint.color = "44444444"

        canvas.draw_circle(pos[0], pos[1], 7)

        paint.style = paint.Style.FILL
        paint.color = "99999944"
        canvas.draw_circle(pos[0], pos[1], 7)

    def on_gaze(self, b):

        l = b["Left Eye 2D Gaze Point"]["$point2d"]
        r = b["Right Eye 2D Gaze Point"]["$point2d"]

        x = (l["x"] + r["x"]) / 2
        y = (l["y"] + r["y"]) / 2

        # Don't pass edges of screen
        if x < 0:
            x = 0
        if y < 0:
            y = 0

        # Multiply by screen width
        x *= size_px.x
        y *= size_px.y

        self.origin = Point2d(x, y)
        self.xy_hist.append(self.origin)
        self.xy_hist = self.xy_hist[-200:]


def click():
    pos = smooth_location()
    ctrl.mouse_move(pos[0], pos[1])
    ctrl.mouse_click(button=0, hold=16000)


def on_key(tap, e):

    # Only do something on key down
    if not e.down:
        return

    # F3 means click
    if e == "f3":
        e.block()
        click()

    # option+= means toggle tobii on and off.
    elif e == "alt-=":
        e.block()

        if mouse.enabled:
            print("    unregister")
            tracker.unregister("gaze", mouse.on_gaze)
        else:
            print("    register")
            tracker.register("gaze", mouse.on_gaze)

        mouse.enabled = not mouse.enabled


tap.register(tap.KEY | tap.HOOK, on_key)

# Uncomment to enable
# mouse = LensMouse()
