from manim import *


config.background_color = "#333333"


def set_gradient_by_x(
    mobject: VMobject,
    color1: ParsableManimColor,
    color2: ParsableManimColor
):
    mobject.set_sheen_direction(RIGHT)
    left = mobject.get_left()[0]
    right = mobject.get_right()[0]
    mobject.set_color_by_gradient(color1, color2)
    for sm in mobject:
        sm.set_color([interpolate_color(
            color1,
            color2,
            (sm.get_left()[0] - left) / (right - left)
        ), interpolate_color(
            color1,
            color2,
            (sm.get_right()[0] - left) / (right - left)
        )])
    return mobject


class ThanksForWatching(Scene):
    def construct(self):
        thanks = set_gradient_by_x(
            Text("¡Gracias por asistir!"),
            RED,
            YELLOW
        )
        self.play(Write(thanks))
        self.wait(10)
        self.play(FadeOut(thanks, scale=5))
        self.wait()
