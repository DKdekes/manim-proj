from abc import ABC

from manim import *
import math

fast_run = False


class CircleArea(Scene):
    def __init__(self):
        # sectioned circle
        self.circle = Circle()
        self.circle.scale(3)
        super().__init__()

    def construct(self):
        self.play(ShowCreation(self.circle))
        self.create_circles(10)

    def create_circles(self, num_sections):
        step_size = 2 * math.pi / num_sections
        radius = self.circle.get_width() / 2
        width = (2 * math.pi * radius) / num_sections
        origin = Point()
        origin.set_color()
        self.add(origin)

        for i in range(num_sections):
            triangle = Triangle()
            triangle.stretch_to_fit_height(radius)
            triangle.stretch_to_fit_width(width)
            triangle.align_to(origin, direction=UP)
            print(origin.points)
            triangle.rotate(i * step_size, about_point=origin.points[0])
            self.play(ShowCreation(triangle))
            # self.play(ApplyMethod(triangle.rotate, i * step_size, about_point=self.origin.points[0]))
        self.wait(3)

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
