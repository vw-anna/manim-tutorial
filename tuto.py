from manim import*  # pylint: disable=unused-wildcard-import

MYPINK = "#E20851"

class welcome(Scene):
    def construct(self):
        
        s = Tex("Hello everybody and welcome to this intro to Manim")

        self.play(Write(s))
        self.wait(1)

class plots(GraphScene):
    def __init__(self, **kwargs):
            GraphScene.__init__(
                self,
                x_min=-5,
                x_max=5,
                y_min=-1,
                y_max=6,
                x_labeled_nums=[0,2,3],
                graph_origin = ORIGIN + 2*DOWN,
                **kwargs)

    
    def construct(self):

        self.setup_axes(animate = True)

        f = self.get_graph(lambda x: x**2 + 1, x_min = -5, x_max = 5)
        g = self.get_graph(lambda x: x**3)

        self.play(ShowCreation(f))
        self.play(ShowCreation(g))
        self.wait(1)