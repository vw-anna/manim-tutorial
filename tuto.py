from manim import*  # pylint: disable=unused-wildcard-import
import math
import sympy

MYPINK = "#E20851" # you can difine custom colors with their html code

class welcome(Scene): # every animation is a class that inherits from the a manim class (here Scene)
    def construct(self): # the construct function must be present in every scene
        
        sentence = Tex("Hello everybody and welcome to this intro to Manim") # Tex objects are typeset by Latex

        self.play(Write(sentence)) # Writing our sentence s, the default location is in the middle of the screen
        self.wait(1) # wait 1 second, always end a scene with a pause

class coordinates(Scene):
    def construct(self):

        dot = Dot() # by default the dot will appear at the center of the screen

        label = MathTex("(0,0)") # this is latex in math mode, more specifically the align* environment
        label.next_to(dot, DOWN) # position  the label below the dot

        self.add(dot)
        self.add(label)
        self.wait(1)

        # now let's move the dot around        
        coords = []
        for y in range(4,-5, -1):
            for x in range(-7,8):
                coords += [[x,y,0]]
        #There are 3 coordinates for 3D drawings. Let's stick to 2 for now and always set the z-coordinate to 0.

        for pos in coords:
            newlabel = MathTex("(%d,%d)" %(pos[0], pos[1])) 
            newlabel.next_to(pos, DOWN) # move the new label to the right position
            self.play(
                dot.animate.move_to(pos),  # move the dot to pos
                ReplacementTransform(label, newlabel), # replace the old label with the new label and delete the old label,
                run_time = .5
            )
            label = newlabel

class geometry(Scene):
    def construct(self):

        circle = Circle(radius = .5, color = MYPINK, fill_opacity = .5)
        poly = Polygon([-3,0,0], [2,1,0], [3,-3,0], [0,-1,0], color = GREEN)

        # we add coordinate dots as a reference
        for x in range(-7,8):
            for y in range(-4,5):
                self.add(Dot([x,y,0]).set_opacity(.1))

        self.play(GrowFromCenter(circle))
        self.play(circle.animate.shift(UP)) # adds [0,1,0] to coordinates
        self.play(circle.animate.shift(RIGHT)) # adds [0,1,0] to coordinates
        self.play(circle.animate.shift(DOWN))
        self.play(circle.animate.shift(LEFT))
        self.play(circle.animate.to_corner(UP + RIGHT))
        self.play(ShrinkToCenter(circle))

        self.wait(1)

        self.play(ShowCreation(poly), run_time = 3)
        self.play(poly.animate.to_edge(UP))
        self.play(Uncreate(poly), run_time = 3)

        self.wait(1)



class plots(GraphScene):
    # This scene illustrates the definition of exp(x)
    def __init__(self, **kwargs):
            GraphScene.__init__(    # initialize GraphScene attributes
                self,
                x_min=-5,
                x_max=5,
                y_min=-1,
                y_max=5,
                #x_labeled_nums=[1],
                graph_origin = ORIGIN + 2*DOWN, # ORIGIN is the middle of the screen
                **kwargs)

    def term(self, x , i):
        # returns the i-th term of the Taylor expansion of exp(x) in the variable x
        return(x**(i)/math.factorial(i))
    
    def construct(self):
        self.setup_axes(animate = True)

        f = self.get_graph(lambda x: math.exp(x), x_min = -5, x_max = 5, color = MYPINK) # lambda is a pyhton conctruction that permits succint definitions of functions. 
        exp = self.get_graph_label(f, label = "e^x", x_val= 2) 
        
        taylor = [] # will contain the Taylor expansions of exp(x) of different degrees
        labelstring = ["1", "1 + x"] # will contain the LaTeX-strings for the labels
        gtaylor = dict() # will contain the graph Mobjects
        labels = dict() # will contain the label Mobjects
        
        y = sympy.symbols("y")

        degree = 7
        for i in range(degree):
            taylor += [lambda x :  sum([self.term(x,j) for j in range(i+1)])]
            print(taylor[i](y))
            gtaylor["t%d" %i] = self.get_graph(taylor[i], color = GREEN)
            if i > 1:
                labelstring += [labelstring[i-1] + "+ \\frac{x^{%d}}{%d!}" %(i,i)]
            labels["l%d" %i] = self.get_graph_label(gtaylor["t%d" %i], label = labelstring[i], x_val = 1, direction = RIGHT + DOWN).scale(.7)

        final = self.get_graph(lambda x :  sum([self.term(x,j) for j in range(degree+1)]))
        final_label = self.get_graph_label(final, label = labelstring[degree-1] + "+ \\frac{x^{%d}}{%d!}" %(degree,degree)).scale(.6)

        self.play(ShowCreation(f))
        self.play(ShowCreation(exp))
        for tay, lab in zip(gtaylor.values(), labels.values()):
            self.play(ShowCreation(tay), ShowCreation(lab))
            self.wait(1)
            self.play(FadeOut(tay), FadeOut(lab))
        self.play(ShowCreation(final), ShowCreation(final_label))    
        self.wait(1)
        