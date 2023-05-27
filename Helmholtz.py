from manim import *
from manim_physics import *
import numpy as np

class Device(Scene):
    def construct(self):
        #Constructing axes and plane
        coil_left = Line(start=[-1.5,1.5,0], end=[-1.5,-1.5,0], color=WHITE)
        coil_right = Line(start=[1.5,1.5,0], end=[1.5,-1.5,0], color=WHITE)
        axes = Axes(
            x_length=14, y_length=8,
            x_axis_config={"label_direction":0.5*DOWN+0.5*RIGHT},
            y_axis_config={"label_direction":0.5*DOWN+0.5*RIGHT},
            ).add_coordinates()
        plane = NumberPlane()
        x_axis = NumberLine(
            x_range=[-7, 7, 1],
            length=14,
            include_tip=True,
            include_ticks=False,
            color=YELLOW,
            # label_direction = 0.5*DOWN+0.5*RIGHT,
            font_size = 24,
            tip_shape = StealthTip
        )

        # Constructing current
        cur_UL = Current(1.5*LEFT+1.5*UP, direction=OUT)
        cur_DL = Current(1.5*LEFT+1.5*DOWN, direction=IN)
        cur_UR = Current(1.5*RIGHT+1.5*UP, direction=OUT)
        cur_DR = Current(1.5*RIGHT+1.5*DOWN, direction=IN)
        field = MagneticField(cur_UL, cur_DL, cur_UR, cur_DR)

        cur_UL.generate_target()
        cur_DL.generate_target()
        cur_UR.generate_target()
        cur_DR.generate_target()

        cur_UL.target.shift(1.5*LEFT)
        cur_DL.target.shift(1.5*LEFT)
        cur_UR.target.shift(1.5*RIGHT)
        cur_DR.target.shift(1.5*RIGHT)

        new_field = MagneticField(cur_UL.target, cur_DL.target, cur_UR.target, cur_DR.target)
        Matters = Group(new_field, cur_UL, cur_DL, cur_UR, cur_DR, coil_left, coil_right)

        #Constucting distance line and valuetracker
        distance = Line(start=ORIGIN, end=1.5*RIGHT)
        distance.set_opacity(0.5)
        radius = Line(start=1.5*RIGHT, end=1.5*RIGHT+1.5*UP)
        brace_dis = Brace(distance, direction=0.5*DOWN, sharpness=1)
        brace_rad = Brace(radius, direction=0.5*RIGHT, sharpness=1)
        dis_text = Text(f"d=R/2", font_size=24).next_to(brace_dis, 0.5*DOWN)
        rad_text = Text(f"R/2", font_size=24).next_to(brace_dis, 2*RIGHT+3*UP)
        new_dis_text = Text(f"d=R", font_size=24).next_to(brace_dis, 0.5*DOWN).shift(0.75*RIGHT)
        
        #Animating
        self.play(Create(cur_UL), Create(cur_UR))
        self.play(Create(coil_left), Create(coil_right))
        self.play(Create(cur_DL), Create(cur_DR))
        self.play(Create(x_axis), rate_func=smooth)
        self.play(
            Create(distance),
            Create(radius),
            GrowFromCenter(brace_dis),
            FadeIn(dis_text),
            GrowFromCenter(brace_rad),
            FadeIn(rad_text)
        )
        self.play(*[GrowArrow(vec) for vec in field])
        self.wait(1)
        self.play(FadeOut(x_axis))
        self.wait(3)
        self.play(
            ReplacementTransform(field, new_field),
            MoveToTarget(cur_UL),
            MoveToTarget(cur_DL),
            MoveToTarget(cur_UR),
            MoveToTarget(cur_DR),
            coil_left.animate.shift(1.5*LEFT),
            coil_right.animate.shift(1.5*RIGHT),
            distance.animate.put_start_and_end_on(start=[0,0,0], end=[3,0,0]),
            brace_dis.animate.stretch(2, dim=0).shift(0.75*RIGHT),
            radius.animate.shift(1.5*RIGHT),
            brace_rad.animate.shift(1.5*RIGHT),
            rad_text.animate.shift(1.5*RIGHT),
            ReplacementTransform(dis_text, new_dis_text),
            run_time=2
        )
        self.wait(3)

class Formula(Scene):
    def construct(self):
        #formulas
        B_x = MathTex(r"\vec{B}(x)=\frac{\mu_0I}{2}\frac{R^2}{(x^2+R^2)^{3/2}}\hat{x}\\").shift(1.5*DOWN)
        B_two_coil = MathTex(r"B(x)=\frac{\mu_0I}{2}\left (\frac{R^2}{(x^2+R^2)^{3/2}}+\frac{R^2}{((x-d)^2+R^2)^{3/2}}  \right )\\").shift(1.5*DOWN)
        B_half_R = MathTex(r"B(\frac{R}{2})=\frac{\mu_0I}{2}\left(\frac{R^2}{((R/2)^2+R^2)^{3/2}}+\frac{R^2}{((R/2)^2+R^2)^{3/2}}\right)\\").shift(1.5*DOWN)
        B_half_R_reduce = MathTex(r"B(\frac{R}{2})=\frac{8}{\sqrt{125}}\frac{\mu_0NI}{R}").shift(1.5*DOWN)
        T_expand = MathTex(r"B(x)=B(\frac{R}{2})+\left(x-\frac{R}{2} \right )\frac{dB}{dx}\bigg|_{x=\frac{R}{2}}+\frac{1}{2}\left(x-\frac{R}{2} \right )^2\frac{d^2B}{dx^2}\bigg|_{x=\frac{R}{2}}+...").shift(1.5*DOWN)
        eq_zero = MathTex(r"\frac{dB}{dx}\bigg|_{x=\frac{R}{2}}=\frac{d^2B}{dx^2}\bigg|_{x=\frac{R}{2}}=\frac{d^3B}{dx^3}\bigg|_{x=\frac{R}{2}}=0\\").shift(2.5*DOWN)
        final = MathTex(r"B(x)\approx B(\frac{R}{2})\left [ 1-\frac{144}{125}\left ( \frac{x-R/2}{R} \right )^4 \right ],\frac{\Delta B}{B}<\frac{1.5}{10000}").shift(1.5*DOWN)

        # Constructing current and coil
        cur_UL = Current(1.5*LEFT+2*UP, direction=OUT)
        cur_DL = Current(1.5*LEFT+2*DOWN, direction=IN)
        cur_UR = Current(1.5*RIGHT+2*UP, direction=OUT)
        cur_DR = Current(1.5*RIGHT+2*DOWN, direction=IN)
        coil_left = Line(start=[-1.5,2,0], end=[-1.5,-2,0], color=WHITE)
        coil_right = Line(start=[1.5,2,0], end=[1.5,-2,0], color=WHITE)

        #axis and line
        axes = Axes(
            x_range=[-5.25, 8.75, 1],
            y_range=[-4, 4, 1],
            axis_config={"color":YELLOW},
            y_axis_config={"length":2}
        )
        distance = Line(start=1.5*LEFT, end=1.5*RIGHT)
        brace = Brace(distance, direction=0.5*DOWN, sharpness=1)
        dis_text = Text(f"d=R", font_size=24).next_to(brace, 0.5*DOWN)

        shapes = Group(cur_UL, cur_DL, cur_UR, cur_DR, coil_left, coil_right, axes ,distance, brace, dis_text)

        self.play(Create(cur_UL), Create(cur_UR))
        self.play(Create(coil_left), Create(coil_right))
        self.play(Create(cur_DL), Create(cur_DR))
        self.play(Create(axes), run_time=2, rate_func=smooth)
        self.play(Create(distance), GrowFromCenter(brace), FadeIn(dis_text))
        self.wait(2)

        self.play(shapes.animate.scale(0.5).shift(2*UP), run_time=1)
        self.wait(2)

        self.play(Write(B_x))
        self.wait(1.5)
        self.play(ReplacementTransform(B_x, B_two_coil))
        self.wait(1.5)
        self.play(ReplacementTransform(B_two_coil, B_half_R))
        self.wait(1.5)
        self.play(ReplacementTransform(B_half_R, B_half_R_reduce))
        self.wait(2)
        self.play(FadeOut(B_half_R_reduce))
        self.play(Create(T_expand))
        self.play(T_expand.animate.shift(0.5*UP))
        self.wait(1.5)
        self.play(FadeIn(eq_zero, shift=UP))
        self.wait(1)
        self.play(FadeOut(eq_zero, shift=DOWN))
        self.play(T_expand.animate.shift(0.5*DOWN))
        self.wait(1)
        self.play(FadeOut(T_expand))
        self.play(Write(final))
        self.wait(3)

class B_graph(Scene):
    def construct(self):
        d, R = 3, 3
        axes = Axes(
            x_range=[-5, 5, 1],
            y_range=[0, 7, 1],
            color=WHITE
        )
        B1 = FunctionGraph(
            lambda x: 80*( ((x+d/2)**2+R**2)**-1.5 + ((x-d/2)**2+R**2)**-1.5 ),
            color=BLUE,
        ).shift(3*DOWN)

        B2 = FunctionGraph(
            lambda x: 80*( ((x+d*2/2)**2+R**2)**-1.5 + ((x-d*2/2)**2+R**2)**-1.5 ),
            color=BLUE,
        ).shift(3*DOWN)

        B_two_coil = MathTex(r"B(x)=\frac{\mu_0I}{2}\left (\frac{R^2}{(x^2+R^2)^{3/2}}+\frac{R^2}{((x-d)^2+R^2)^{3/2}}  \right )\\", color=BLUE).shift(3.5*LEFT+1.5*UP).scale(0.5)
        distance = Line(start=[0,1.3,0], end=[1.5,1.3,0], color=YELLOW, stroke_width=2.5)
        brace = Brace(distance, direction=UP, sharpness=1).shift(0.1*DOWN)
        dis_text = Text(f"d=R/2", font_size=24).next_to(brace, UP).shift(0.1*DOWN)
        new_dis_text = Text(f"d=R", font_size=24).next_to(brace, UP).shift(0.75*RIGHT+1.1*DOWN)

        self.play(Create(axes))
        self.play(Create(B1), Write(B_two_coil))
        self.wait(1.5)
        self.play(FadeOut(B_two_coil))
        self.play(Create(distance), GrowFromCenter(brace), FadeIn(dis_text))
        self.wait(1.5)
        self.play(
            ReplacementTransform(B1, B2),
            distance.animate.stretch(2, dim=0).shift(0.75*RIGHT+DOWN),
            brace.animate.stretch(2, dim=0).shift(0.75*RIGHT+DOWN),
            ReplacementTransform(dis_text, new_dis_text),
            run_time=3, rate_func=smooth
        )
        self.wait(1)
        
