from manim import *

class Derivatives(Scene):
    def construct(self):
        # --- 1. AXES AND GRAPH ---
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-10, 10, 5],
            x_length=6,
            y_length=7,
            axis_config={'color': WHITE, 'include_tip': False},
        )
        
        # Define the function
        def cubic_function(x):
            return x**3
            
        graph = axes.plot(cubic_function, color=BLUE, x_range=[-2.15, 2.15])
        graph_label = Text("f(x)", font_size=32).next_to(
            axes.c2p(-2.15, cubic_function(2.15)), UR, buff=0.1
        )

        graph_group = VGroup(axes, graph, graph_label)

        # --- 2. INTRO ANIMATION ---
        self.play(Create(axes), run_time=1.5)
        self.play(Create(graph), Write(graph_label), run_time=2)
        self.wait(0.5)
        self.play(graph_group.animate.shift(LEFT * 3), run_time=2)
        self.wait(1)

        # --- 3. VALUE TRACKER, DOT, TANGENT ---
        t = ValueTracker(-2.15)

        # Dot on the cubic graph
        dot = always_redraw(lambda: Dot(
            point=axes.c2p(t.get_value(), cubic_function(t.get_value())),
            color=WHITE
        ))

        # --- 4. DERIVATIVE AXES AND LABEL ---
        deriv_axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[0, 15, 3],
            x_length=3.5,
            y_length=3.5,
            axis_config={'color': WHITE, 'include_tip': False},
        ).to_corner(UR).shift(LEFT*0.5)
        deriv_label = Text("f'(x)", font_size=28).next_to(deriv_axes, UL, buff=0.1)
        deriv_group = VGroup(deriv_axes, deriv_label)

        # Derivative graph
        deriv_function = lambda x: 3 * x**2
        deriv_graph = deriv_axes.plot(deriv_function, color=RED, x_range=[-2.15, 2.15])
        
        # Dot on derivative graph
        deriv_dot = always_redraw(lambda: Dot(
            point=deriv_axes.c2p(t.get_value(), deriv_function(t.get_value())),
            color=WHITE
        ))

        # Tangent on f(x) - grey
        def get_tangent_f():
            x = t.get_value()
            y = cubic_function(x)
            slope = deriv_function(x)  # 3*x**2
            
            # Create tangent line using point-slope form
            length = 2
            point1 = axes.c2p(x - length/2, y - slope * length/2)
            point2 = axes.c2p(x + length/2, y + slope * length/2)
            
            return Line(point1, point2, color=GREY, stroke_width=3)
        
        tangent_f = always_redraw(get_tangent_f)

        # --- 6. SECOND DERIVATIVE (THIRD GRAPH) ---
        deriv2_axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-15, 15, 5],
            x_length=3.5,
            y_length=3.5,
            axis_config={'color': WHITE, 'include_tip': False},
        ).next_to(deriv_axes, DOWN, buff=0.25)
        deriv2_label = Text("f''(x)", font_size=28).next_to(deriv2_axes, UL, buff=0.1)
        deriv2_group = VGroup(deriv2_axes, deriv2_label)

        # Second derivative graph
        deriv2_function = lambda x: 6 * x
        deriv2_graph = deriv2_axes.plot(deriv2_function, color=ORANGE, x_range=[-2.15, 2.15])

        # Dot on second derivative graph
        deriv2_dot = always_redraw(lambda: Dot(
            point=deriv2_axes.c2p(t.get_value(), deriv2_function(t.get_value())),
            color=WHITE
        ))
        
        # FIXED: Tangent on f'(x) - grey - CORRECTLY POSITIONED
        def get_tangent_f_prime():
            x = t.get_value()
            y = deriv_function(x)  # This is the y-value on f'(x) graph
            slope = deriv2_function(x)  # 6*x - this is the slope of f'(x)
            
            # IMPORTANT: Create line in DERIVATIVE AXES coordinates
            length = 1.5
            point1 = deriv_axes.c2p(x - length/2, y - slope * length/2)
            point2 = deriv_axes.c2p(x + length/2, y + slope * length/2)
            
            return Line(point1, point2, color=GREY, stroke_width=3)
        
        tangent_f_prime = always_redraw(get_tangent_f_prime)
        
        # --- 5. ANIMATION SEQUENCE ---

        # PART 1: Show f(x) and its derivative
        self.play(Create(deriv_group), Create(deriv_graph), run_time=1)
        
        # Add the first tangent (on f(x)) and dots
        deriv_trace = TracedPath(deriv_dot.get_center, stroke_color=RED, stroke_width=3)
        self.add(dot, tangent_f, deriv_dot, deriv_trace)
        
        # Animate the first pass
        self.play(t.animate.set_value(2.15), run_time=8, rate_func=linear)
        self.wait(1)

        # PART 2: Show f'(x) and its derivative f''(x)
        # Reset the tracker
        t.set_value(-2.15)
        
        # FIXED: Clear the previous tangent and trace
        self.remove(tangent_f, deriv_trace)
        
        # Show the second derivative graph
        self.play(Create(deriv2_group), Create(deriv2_graph))
        
        # FIXED: Add the second tangent (on f'(x))
        self.add(tangent_f_prime)
        
        deriv2_trace = TracedPath(deriv2_dot.get_center, stroke_color=ORANGE, stroke_width=3)
        self.add(deriv2_dot, deriv2_trace)
        self.wait(0.5)

        # Animate the tracker again
        self.play(t.animate.set_value(2.15), run_time=8, rate_func=linear)
        self.wait(1)

        # Final cleanup
        self.play(
            FadeOut(dot, deriv_dot, deriv2_dot, tangent_f_prime),
            run_time=0.5
        )
        self.wait(2)