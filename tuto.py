from manim import*  # pylint: disable=unused-wildcard-import
import math
import sympy

MYPINK = "#E20851" # you can difine custom colors with their html code
MYGREEN = "#51e208"

class welcome(Scene): # every animation is a class that inherits from the a manim class (here Scene)
    def construct(self): # the construct function must be present in every scene
        
        sentence = Tex("Hello everybody and welcome to this intro to Manim") # Tex objects are typeset by Latex

        self.play(Write(sentence)) # Writing our sentence s, the default location is in the middle of the screen
        self.wait(1) # wait 1 second, always end a scene with a pause

class coordinates(Scene):
    def construct(self):

        dot = Dot() # by default the dot will appear at the center of the screen aka ORIGIN aka [0,0,0]

        label = MathTex("(0,0)") # this is latex in math mode, more specifically the align* environment
        label.next_to(dot, DOWN) # position  the label below the dot

        self.add(dot)
        self.add(label)
        self.wait(1)

        # these are the visible integer coordinates
        # there are 3 coordinates for 3D drawings. Let's stick to 2 for now and always set the z-coordinate to 0.      
        coords = []
        for y in range(4,-5, -1):
            for x in range(-7,8):
                coords += [[x,y,0]]
       

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
    # This scene illustrates the definition of exp(x) by showing the different polynomial expansions
    def __init__(self, **kwargs):
            GraphScene.__init__(   
                self,
                x_min=-5,
                x_max=5,
                y_min=0,
                y_max=8,
                graph_origin = ORIGIN + 2.7*DOWN, # ORIGIN is the middle of the screen
                **kwargs)

    def term(self, x , i):
        # returns the i-th term of the Taylor expansion of exp(x) in the variable x
        return(x**(i)/math.factorial(i))
    
    def construct(self):
        self.setup_axes(animate = True)

        f = self.get_graph(lambda x: math.exp(x), x_min = -5, x_max = 5, color = MYPINK) # graph of the exp function
        exp = self.get_graph_label(f, label = "e^x", x_val= 2) # TeX label
        
        self.play(ShowCreation(f))
        self.play(ShowCreation(exp))

        degree = 15 # degree to which the taylor expansions will be shown
        g = self.get_graph(lambda x:1, color = MYGREEN) # 0-th order approximation
        polynomial = MathTex("1").scale(.7).to_corner(DOWN + RIGHT, buff= .3).set_color(MYGREEN)
        
        self.play(ShowCreation(g), Write(polynomial[0]))
        self.wait(1)
        for i in range(1,degree + 1):
            next_g = self.get_graph(lambda x :  sum([self.term(x,j) for j in range(i+1)]),color = MYGREEN) # graph of the i-th polynomial expansion
            
            if i == 1:
                # this case is necessary to print 1 + x instead of 1+x/1! for the first polynomial expansion
                polynomial_string = next_polynomial_string = "1 + x" 
            else:
                next_polynomial_string = polynomial_string + "+ \\frac{x^{%d}}{%d!}" %(i,i)
            
            next_polynomial = MathTex(next_polynomial_string).scale(.7).to_corner(DOWN + RIGHT,  buff= .3).set_color(MYGREEN)   # make MathTex mobject out of string
            self.play(
                ReplacementTransform(g, next_g),
                ReplacementTransform(polynomial, next_polynomial)
                )
            self.wait(.7)
            g = next_g
            polynomial = next_polynomial
            polynomial_string = next_polynomial_string
        self.wait(1)
                