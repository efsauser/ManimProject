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

class Snow(Scene):
    def construct(self):
        def next(obj):
            old = t.get_value()
            if t.get_value()%2==0:
                t.set_value(old/2)
                obj.shift(0.1*RIGHT, (old/2-old)*0.0007*UP)
            else:
                t.set_value(t.get_value()*3+1)
                obj.shift(0.1*RIGHT, (old*3+1-old)*0.0007*UP)

        axes = Axes(
            x_min=0, x_max=10,
            y_min=0, y_max=33,
            center_point=5*LEFT+3*DOWN,
            y_axis_config={
                "label_direction":UP,
                "numbers_with_elongated_ticks":[10,20,30],
            "tick_frequency":1,
            "stroke_width":4,
            "unit_size":0.2,
            },
        )
        t = ValueTracker(27)
        dot = Dot(radius=0).move_to(6*LEFT+3*DOWN)
        path = TracedPath(dot.get_center, stroke_color=ORANGE)
        self.play(ShowCreation(axes.x_axis), ShowCreation(axes.y_axis))
        self.play(UpdateFromFunc(dot, next), ShowCreation(path), run_time=3)
        self.wait()
