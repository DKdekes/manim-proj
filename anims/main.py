from abc import ABC

from manim import *
import math

fast_run = False


class CircleArea(Scene):

    def construct(self):
        self.circle_shift = 1 * UP + 3.5 * LEFT
        self.tangle_shift = 2 * DOWN
        self.anim_time = 0.1
        self.opacity = 0.9
        self.circle = Circle()
        self.circle.scale(2)
        self.circle.shift(self.circle_shift)
        self.play(ShowCreation(self.circle))

        # simple
        rectangle_sections = self.create_sections(8)
        self.add_tangle_brace(rectangle_sections)
        self.wait(3)
        self.clear()

        # # moderate
        # rectangle_sections = self.create_sections(12)
        # self.add_tangle_brace(rectangle_sections)
        # self.wait(3)
        # self.clear()
        #
        # # full circle
        # rectangle_sections = self.create_sections(30)
        # self.add_tangle_brace(rectangle_sections)
        # self.wait(3)

    def add_final_equation(self):
        pass

    def add_tangle_brace(self, tangle_triangles):
        brace_line = Line(tangle_triangles[0].get_vertices()[0], tangle_triangles[-1].get_vertices()[2])
        tangle_brace = Brace(brace_line).shift(UP)
        tangle_brace.flip(LEFT)
        # todo: actual math. add = pi*r
        brace_tex = tangle_brace.get_tex("1/2 C")
        # todo: add vertical bracket
        self.play(ShowCreation(tangle_brace))
        self.add(tangle_brace, brace_tex)

    def remove_sections(self, sections):
        for section in sections:
            self.remove(section)

    def create_sections(self, num_sections):
        tangle_angles = []
        step_size = 2 * math.pi / num_sections
        radius = self.circle.get_width() / 2
        width = (2 * math.pi * radius) / num_sections
        circle_origin = Point()
        circle_origin.set_color()
        circle_origin.shift(self.circle_shift)
        self.add(circle_origin)
        print(circle_origin.points)

        for i in range(num_sections):
            # todo: add outline
            triangle = Triangle(fill_opacity=self.opacity)
            triangle.stretch_to_fit_height(radius)
            triangle.stretch_to_fit_width(width)
            if i % 2 == 0:
                triangle.set_color(YELLOW)
                triangle.set_fill(YELLOW)
                triangle.set_stroke(WHITE)
            else:
                triangle.set_fill(BLUE)
                triangle.set_stroke(WHITE)
            tangle_triangle = triangle.copy()

            # for the circle
            triangle.shift(self.circle_shift)
            triangle.align_to(circle_origin, direction=UP)
            triangle.rotate(i // 2 * step_size if i % 2 == 0 else (i // 2 + 1) * -step_size, about_point=circle_origin.points[0])

            self.play(ShowCreation(triangle), run_time=self.anim_time)

            # for the rectangle
            tangle_triangle.shift(self.tangle_shift)
            tangle_triangle.shift(0.5 * width * RIGHT * i)
            if i % 2 != 0:
                tangle_triangle.flip(LEFT)
                tangle_triangle.shift(UP * 0.2)
            self.play(ShowCreation(tangle_triangle), run_time=self.anim_time)
            tangle_angles.append(tangle_triangle)
            print(tangle_triangle.get_vertices())
            # self.play(ApplyMethod(triangle.rotate, i * step_size, about_point=self.origin.points[0]))
        return tangle_angles

    def anim(self, function, *args, **kwargs):
        if fast_run:
            function(args, kwargs)
        else:
            self.play(ApplyMethod(function, args, kwargs))


class Angles(Scene):
    def construct(self):
        # define the degrees you want to use
        degrees = [30, 180, 270, 66]
        radians = [x * ((2 * math.pi) / 360.) for x in degrees]
        line = Line()
        rot_line = Line()
        vertex = Point().move_to(LEFT)
        vertex.set_color()
        integer = Integer(
            0,
            unit="^o"
        )
        integer.add_updater(lambda d: d.next_to(rot_line.points[2], aligned_edge=UP))
        integer.add_updater(lambda d: d.set_value(self.radian_to_degree(rot_line.get_angle())))
        self.add(vertex)
        self.add(integer)
        self.play(ShowCreation(line))
        self.add(rot_line)
        for x in radians:
            self.play(ApplyMethod(rot_line.set_angle, x))
            self.wait(3)

    def radian_to_degree(self, rad):
        if rad < 0:
            rad = abs(rad) + math.pi
        return rad * (360 / (2 * math.pi))
