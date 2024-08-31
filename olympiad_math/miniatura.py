from manim import *


config.background_color = "#161616"
template = TexTemplate(preamble="""\\usepackage[spanish]{babel}
\\usepackage{amsmath}
\\usepackage{amssymb}
\\usepackage{mlmodern}""")
config.tex_template = template
config.preview = True


LOGO_COLOR = "#2484e3"


class Logo(VGroup):
    def __init__(self, color=LOGO_COLOR, icon=None):
        if icon is None:
            icon = MathTex("\\sum", color=WHITE)
        circ = Circle(color=WHITE).set_fill(color, opacity=1)
        super().__init__(circ, icon)


class Miniatura(Scene):
    def construct(self):
        title = Text("Lógica Proposicional", font_size=144, font="Roboto", weight=BOLD).scale(0.5)
        subtitle = Text("Teoría y práctica desde cero", font_size=144, font="Roboto", weight=BOLD).scale(0.3)
        g = VGroup(title, subtitle).arrange(DOWN).shift(UP)
        rect = SurroundingRectangle(g, color=WHITE, corner_radius=0.2, buff=0.5)
        logo = Logo().to_corner(DR)
        example = MathTex("\\neg p \\Rightarrow (q \\lor r)").scale(2).shift(1.5*DOWN)
        VGroup(g, rect, example).center()
        self.add(title, subtitle, logo, rect, example)


if __name__ == "__main__":
    Miniatura().render()
