# Create a simple animation WITHOUT LaTeX
python -c "
from manim import *

class NoLatexTest(Scene):
    def construct(self):
        circle = Circle(color=BLUE)
        square = Square(color=RED)
        self.play(Create(circle))
        self.play(Transform(circle, square))
        self.wait(1)

if __name__ == '__main__':
    scene = NoLatexTest()
    scene.render()
" > test_nolatex.py

manim -pql test_nolatex.py NoLatexTest