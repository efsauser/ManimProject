from manimlib.imports import *
import os
import pyclbr

class Throw(Scene):
    def construct(self):
        axes = Axes(
            x_min=0, x_max=10,
            y_min=0, y_max=33,
            center_point=5*LEFT+3*DOWN,
            x_axis_config={
                "include_numbers":True,
            },
            y_axis_config={
                "label_direction":UP,
                "numbers_with_elongated_ticks":[10,20,30],
            "tick_frequency":1,
            "stroke_width":4,
            "unit_size":0.2,
            },
        )
        axes.y_axis.add_numbers(10, 20, 30, direction=LEFT)

        velo, angle = 10, 60*DEGREES
        dot = Dot()
        arc = Sector()
        velo_vec = Arrow()
        velo_vec_x = Arrow()
        velo_vec_y = Arrow()
        height_line = DashedLine()
        t = ValueTracker(0)
        theta = DecimalNumber(num_decimal_places=0).move_to(np.array([-3.8, -2.4, 0]))
        theta_value = ValueTracker(0)
        func = ParametricFunction(
            lambda t: np.array([
                velo*np.cos(angle)*t,
                velo*np.sin(angle)*t-5*t**2,
                0
            ]),color=BLUE, t_min=0, t_max=2*velo*np.sin(angle)/10
        ).shift(5*LEFT+3*DOWN)

        dot.add_updater(lambda a:a.move_to(np.array([velo*np.cos(angle)*t.get_value() -5,velo*np.sin(angle)*t.get_value()-5*t.get_value()**2 -3,0])))
        theta.add_updater(lambda a:a.set_value(int(theta_value.get_value())))
        arc.add_updater(lambda a:a.become(Sector(fill_color=GREY, fill_opacity=0.3, arc_center=np.array([-5, -3, 0]), stroke_width=3, stroke_color=GREY, angle=DEGREES*(theta_value.get_value()-1))))
        velo_vec_x.add_updater(
            lambda a:a.become(
                Arrow(np.array([velo*np.cos(angle)*t.get_value()-5, velo*np.sin(angle)*t.get_value()-5*t.get_value()**2-3, 0]),
                      np.array([velo*np.cos(angle)*t.get_value()-5+velo*0.1*np.cos(angle), velo*np.sin(angle)*t.get_value()-5*t.get_value()**2-3, 0]),
                color=RED, buff=0)
            )
        )
        velo_vec_y.add_updater(
            lambda a:a.become(
                Arrow(np.array([velo*np.cos(angle)*t.get_value()-5, velo*np.sin(angle)*t.get_value()-5*t.get_value()**2-3, 0]),
                      np.array([velo*np.cos(angle)*t.get_value()-5, velo*np.sin(angle)*t.get_value()-5*t.get_value()**2-3+velo*0.1*np.sin(angle)-10*0.1*t.get_value(), 0]),
                color=YELLOW, buff=0)
            )
        )
        velo_vec.add_updater(
            lambda a:a.become(
                Arrow(np.array([velo*np.cos(angle)*t.get_value()-5, velo*np.sin(angle)*t.get_value()-5*t.get_value()**2-3, 0]),
                      np.array([velo*np.cos(angle)*t.get_value()-5+velo*0.1*np.cos(angle), velo*np.sin(angle)*t.get_value()-5*t.get_value()**2-3+velo*0.1*np.sin(angle)-10*0.1*t.get_value(), 0]),
                buff=0)
            )
        )
        height_line.add_updater(
            lambda a:a.become(
                DashedLine(np.array([velo*np.cos(angle)*t.get_value()-5, -3, 0]),
                           np.array([velo*np.cos(angle)*t.get_value()-5, velo*np.sin(angle)*t.get_value()-5*t.get_value()**2-3, 0]),
                color=GREY, dash_length=0.1 ,positive_space_ratio=0.7)
            )
        )

        self.play(*[ShowCreation(mob) for mob in [axes.x_axis, axes.y_axis]], rate_func=smooth, run_time=3)
        self.add(theta, arc)
        self.play(theta_value.set_value, 1+angle/DEGREES)
        arc.clear_updaters()
        self.play(*[ShowCreation(mob) for mob in [dot, velo_vec_x, velo_vec_y, velo_vec, height_line]])
        self.play(*[FadeOut(mob) for mob in [theta, arc]])
        self.play(ShowCreation(func), t.set_value, 2*velo*np.sin(angle)/10, run_time=5)
        self.wait()

class Pendulum(Scene):
    def construct(self):
        mg = 1
        line = Line(np.array([0,2,0]),np.array([0,-1,0]))
        circle = Circle(radius=0.1, stroke_width=3)
        circle.next_to(line, DOWN, buff=0)
        # pendulum= VGroup(line, circle)
        # pendulum.rotate(45*DEGREES, axis=IN, about_point=np.array([0,2,0]))
        def rr(x,y,z,t):
            x=x+np.cos(100*t)
            y=y+np.sin(100*t)-mg
            z=0
            return [x,y,z] 
        self.play(Homotopy(rr,circle),run_time=10,rate_func=linear)
        # self.play(ShowCreation(pendulum))
        # self.play(Rotating(pendulum , radians=90*DEGREES,run_time=10,axis=OUT,about_point=2*UP),rate_func=there_and_back,run_time=1)
        self.wait()
