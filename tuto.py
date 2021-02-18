from manim import*  # pylint: disable=unused-wildcard-import
import math # we need this for the exponential function

MYPINK = "#E20851" # you can define custom colors with their html code
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
            newdot = Dot().move_to(dot.get_center()) # a new dot in the same position as dot
            newlabel = MathTex("(%d,%d)" %(pos[0], pos[1])) 
            newlabel.next_to(pos, DOWN) # move the new label to the right position
            self.play(
                newdot.animate.move_to(pos), # move the new dot   
                dot.animate.set_opacity(.3), # make the old dot transparant
                ReplacementTransform(label, newlabel), # replace the old label with the new label and delete the old label
                run_time = .7
            )
            dot = newdot
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
        self.play(circle.animate.shift(RIGHT)) # adds [1,0,0] to coordinates
        self.play(circle.animate.shift(DOWN))
        self.play(circle.animate.shift(LEFT))
        self.play(circle.animate.to_corner(UP + RIGHT))
        self.play(ShrinkToCenter(circle))

        self.wait(1)

        self.play(ShowCreation(poly), run_time = 3)
        self.play(poly.animate.to_edge(UP, buff = .5))
        self.play(Uncreate(poly), run_time = 3)

        self.wait(1)

class calculations(Scene):
    # we will animate the process of finding a primitive for sin(x)exp(x) by using integration by parts twice
    def construct(self):
        integral = MathTex(
            r"\int",r"\sin(x)",r"e^x", r"dx", r"&=",    #0,1,2,3,4
            r"\sin(x)e^x", r"-\int",r"\cos(x)",r"e^x", r"dx\\", #5,6,7,8,9
            r"&= \sin(x)e^x", #10 
            r"-\left(", r"\cos(x)e^x", #11,12
            r"-\int" , r"-\sin(x)e^x", r"dx\right)\\", #13, 14, 15
            r"&=", r"(\sin(x)-\cos(x))e^x", r"-", r"\int\sin(x)e^xdx", #16, 17, 18,19
            ).to_corner(UL) 
            # MathTex is the align* environment so always mathmode. 
            # Either use the r flag or double all \ symbols
        
        solution = MathTex(r"2",r"\int\sin(x)e^xdx", r"=", r"(\sin(x)-\cos(x))", r"e^x", r"\frac{1}{2}" ).shift(2.5*DOWN)
        expdivtwo = MathTex(r"\frac{e^x}{2}" )

        explain = Tex(r"Integral by parts:", r"$\int fg'dx = fg - \int f'g dx$").to_edge(DOWN) # regular Tex, centered. Do not forget math mode!

        part1 = MathTex(
            r"f(x)=", r"\sin(x)", r"&\Rightarrow", r"f'(x) =", r"\cos(x)\\",
            r"g'(x)=", r"e^x", r"&\Rightarrow", r"g(x)=", r"e^x"
            )
        boxs11 = VGroup(
            SurroundingRectangle(part1[1], buff = .1).set_color(WHITE),
            SurroundingRectangle(part1[9], buff = .1).set_color(WHITE)
            ) # VGroup unifies mobjects so that they can be manipulated as one
        boxs12 = VGroup(
            SurroundingRectangle(part1[4], buff = .1).set_color(WHITE),
            SurroundingRectangle(part1[6], buff = .1).set_color(WHITE)
            )

        part2 = MathTex(
            r"f(x)=", r"\cos(x)", r"&\Rightarrow", r"f'(x) =", r"-\sin(x)\\",
            r"g'(x)=", r"e^x", r"&\Rightarrow", r"g(x)=", r"e^x"
            ).shift(.5*DOWN)
        boxs21 = VGroup(
            SurroundingRectangle(part2[1], buff = .1).set_color(WHITE),
            SurroundingRectangle(part2[9], buff = .1).set_color(WHITE)
            ) # VGroup unifies mobjects so that they can be manipulated as one
        boxs22 = VGroup(
            SurroundingRectangle(part2[4], buff = .1).set_color(WHITE),
            SurroundingRectangle(part2[6], buff = .1).set_color(WHITE)
            )
        
        intbox = VGroup(
            SurroundingRectangle(integral[:4], buff = .1).set_color(MYPINK),       
            SurroundingRectangle(integral[19], buff = .1).set_color(MYPINK))
        solbox = SurroundingRectangle(integral[17], buff = .1).set_color(MYPINK)

        #setup
        self.play(Write(integral[:5]))
        self.play(Write(explain))
        self.wait(2)
        
        # first parts integral
        self.play(
            integral[1].animate.set_color(MYPINK),
            Write(part1[:2].set_color(MYPINK))
        ) # choose and highlight f
        self.wait(2)
        self.play(Write(part1[2:5])) # differentiate f
        self.wait(2)
        self.play(
            integral[2].animate.set_color(MYGREEN),
            Write(part1[5:7].set_color(MYGREEN))
            ) # choose and highlight g
        self.wait(2)
        self.play(Write(part1[7:])) # find a primitive for g
        self.wait(2)
        self.play(
            Write(integral[5]),
            FadeIn(boxs11)
            ) # first term of integration by parts
        self.wait(2)
        self.play(
            Write(integral[6]),
            FadeOut(boxs11)
            )
        self.play(
            Write(integral[7:10]),
            FadeIn(boxs12)
            ) # second term of integration by parts
        self.wait(2)
        self.play(FadeOut(boxs12), FadeOut(part1), integral[1:3].animate.set_color(WHITE))
        self.wait(2)

        # second parts integral
        self.play(Write(integral[10:12]))
        self.wait(2)
        self.play(
            integral[7].animate.set_color(MYPINK),
            Write(part2[:2].set_color(MYPINK))
        )
        self.wait(2)
        self.play(Write(part2[2:5]))
        self.wait(2)
        self.play(
            integral[8].animate.set_color(MYGREEN),
            Write(part2[5:7].set_color(MYGREEN))
            )
        self.wait(2)
        self.play(Write(part2[7:]))
        self.wait(2)

        self.play(
            Write(integral[12]),
            FadeIn(boxs21)
            )
        self.wait(2)
        self.play(
            Write(integral[13]),
            FadeOut(boxs21)
            )
        self.wait(2)
        self.play(
            FadeIn(boxs22),
            Write(integral[14:16])
            )
        self.wait(2)
        self.play(FadeOut(boxs22), FadeOut(part2), integral[7:9].animate.set_color(WHITE))
        self.wait(1)
        
        # we are done with integration by partts
        self.play(FadeOutAndShift(explain, DOWN))
        self.wait(2)

        # rearrange the equation
        self.play(Write(integral[16:]))
        self.wait(2)
        self.play(ShowCreation(intbox))
        self.wait(1)
        self.play(Write(solution[:3]))
        self.wait(2)
        self.play(FadeOut(intbox), ShowCreation(solbox))
        self.wait(1)
        self.play(Write(solution[3:5]))
        self.wait(2)
        self.play(FadeOut(integral), FadeOut(solbox), solution[:5].animate.move_to(ORIGIN))
        self.wait(2)
        self.play(FadeOut(solution[0]), Write(solution[5].next_to(solution[4], RIGHT))) 
        self.wait(2)
        self.play(Transform(solution[4:], expdivtwo.next_to(solution[3], RIGHT, buff = .05)))
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

        f = self.get_graph(lambda x: math.exp(x), x_min = -5, x_max = 5, color = MYGREEN) # graph of the exp function
        exp = self.get_graph_label(f, label = "e^x", x_val= 2) # TeX label
        
        self.play(ShowCreation(f))
        self.play(ShowCreation(exp))

        degree = 15 # degree to which the taylor expansions will be shown
        g = self.get_graph(lambda x:1, color = MYPINK) # 0-th order approximation
        polynomial = MathTex("1").scale(.7).to_corner(DOWN + RIGHT, buff= .3).set_color(MYPINK)
        
        self.play(ShowCreation(g), Write(polynomial[0]))
        self.wait(1)
        for i in range(1,degree + 1):
            next_g = self.get_graph(lambda x :  sum([self.term(x,j) for j in range(i+1)]),color = MYPINK) # graph of the i-th polynomial expansion
            
            if i == 1:
                # this case is necessary to print 1 + x instead of 1+x/1! for the first polynomial expansion
                polynomial_string = next_polynomial_string = "1 + x" 
            else:
                next_polynomial_string = polynomial_string + "+ \\frac{x^{%d}}{%d!}" %(i,i)
            
            next_polynomial = MathTex(next_polynomial_string).scale(.7).to_corner(DOWN + RIGHT,  buff= .3).set_color(MYPINK)   # make MathTex mobject out of string
            self.play(
                ReplacementTransform(g, next_g),
                ReplacementTransform(polynomial, next_polynomial)
                )
            self.wait(.7)
            g = next_g
            polynomial = next_polynomial
            polynomial_string = next_polynomial_string
        self.wait(1)
                