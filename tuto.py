from manim import*  # pylint: disable=unused-wildcard-import

MYPINK = "#E20851" # you can difine custom colors with their html code

class welcome(Scene): # every animation is a class that inherits from the a manim class (here Scene)
    def construct(self): # the construct function must be present in every scene
        
        sentence = Tex("Hello everybody and welcome to this intro to Manim") # Tex objects are typeset by Latex

        self.play(Write(sentence)) # Writing our sentence s, the default location is in the middle of the screen
        self.wait(1) # wait 1 second, always end a scene with this

class coordinates(Scene):
    def construct(self):

        dot = Dot() # by default the dot will appear at the center of the screen

        label = MathTex("(0,0)") # this is latex in math mode, more specifically the align* environment
        label.next_to(dot, DOWN) # position  the label below the dot

        self.add(dot)
        self.add(label)
        self.wait(1)

        # now let's move the dot around
        labdot = VGroup(dot, label) # call "labdot" the unified object of the labelled dot so that it gets moved around as a unit
        coords = [[0,1,0], [0,-1,0], [1,0,0], [-1,0,0], [3,4,0], [-4,1,0]] 
        
        coords = []
        for x in range(-6,6):
            for y in range(-3,3):
                coords += [[x,y,0]]
        #There are 3 coordinates for 3D drawings. Let's stick to 2 for now and always set the z-coordinate to 0.

        for pos in coords:
            newlabel = MathTex("(%d,%d)" %(pos[0], pos[1])) 
            newlabel.next_to(pos, DOWN) # move the new label to the right position
            self.play(
                ApplyMethod(dot.move_to, pos),  # move the dot to pos
                ReplacementTransform(label, newlabel) # replace the old label with the new label and deltete the old label
            )
            self.wait(1)
            label = newlabel


class plots(GraphScene):
    def __init__(self, **kwargs):
            GraphScene.__init__(    # initialize GraphScene attributes
                self,
                x_min=-5,
                x_max=5,
                y_min=-1,
                y_max=6,
                x_labeled_nums=[0,2,3], # ticks on the x-axis that get a label
                graph_origin = ORIGIN + 2*DOWN, # ORIGIN is the middle of the screen
                **kwargs)

    
    def construct(self):

        self.setup_axes(animate = True)

        f = self.get_graph(lambda x: x**2 + 1, x_min = -5, x_max = 5) # lambda is a pyhton conctruction that permits succint definitions of functions. 
        g = self.get_graph(lambda x: x**3, x_min = 0, x_max = 5)

        self.play(ShowCreation(f))
        self.play(ShowCreation(g))
        self.wait(1)