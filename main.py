
import random
from math import sin, cos, pi, log
from tkinter import *

CANVAS_WIDTH = 640  # width of canvas
CANVAS_HEIGHT = 480  # height of canvas
CANVAS_CENTER_X = CANVAS_WIDTH / 2  # canter of canvas-x
CANVAS_CENTER_Y = CANVAS_HEIGHT / 2  # center of canvas-y
IMAGE_ENLARGE = 11  # enlarge ratio
HEART_COLOR = "#ff2121"  # color of heart


def heart_function(t, shrink_ratio: float = IMAGE_ENLARGE):
    """
    function to draw heart
    :param shrink_ratio: shrink ratio
    :param t: parameter
    :return: x, y
    """
    # heart function base is 0,0
    x = 16 * (sin(t) ** 3)
    y = -(13 * cos(t) - 5 * cos(2 * t) - 2 * cos(3 * t) - cos(4 * t))

    # enlarge the x,y to make it bigger
    x *= shrink_ratio
    y *= shrink_ratio

    # move the heart to center of canvas
    x += CANVAS_CENTER_X
    y += CANVAS_CENTER_Y

    return int(x), int(y)


def scatter_inside(x, y, beta=0.15):
    """
    random scatter inside the heart
    :param x: original x
    :param y: original y
    :param beta: ratio
    :return: new x, y
    """
    ratio_x = - beta * log(random.random())
    ratio_y = - beta * log(random.random())

    dx = ratio_x * (x - CANVAS_CENTER_X)
    dy = ratio_y * (y - CANVAS_CENTER_Y)

    return x - dx, y - dy


def shrink(x, y, ratio):
    """
    shrink the heart
    :param x: original x
    :param y: original y
    :param ratio: shrink ratio
    :return: new x, y
    """
    force = 1 / (((x - CANVAS_CENTER_X) ** 2 + (y - CANVAS_CENTER_Y) ** 2) ** 0.6)  
    dx = ratio * force * (x - CANVAS_CENTER_X)
    dy = ratio * force * (y - CANVAS_CENTER_Y)
    return x - dx, y - dy


def curve(p):
    """
    beating period
    :param p: 
    :return: 
    """
    
    return 2 * (2 * sin(4 * p)) / (2 * pi)


class Heart:


    def __init__(self, generate_frame=20):
        self._points = set()  # original heart points
        self._edge_diffusion_points = set()  # edge diffusion points
        self._center_diffusion_points = set()  # center diffusion points
        self.all_points = {}  # points for each frame
        self.build(3000)

        self.random_halo = 1000

        self.generate_frame = generate_frame
        for frame in range(generate_frame):
            self.calc(frame)

    def build(self, number):
        # heart points
        for _ in range(number):
            t = random.uniform(0, 2 * pi)  # random points for heart
            x, y = heart_function(t)
            self._points.add((x, y))

        # heart scatter inside
        for _x, _y in list(self._points):
            x, y = scatter_inside(_x, _y, 0.05)
            self._edge_diffusion_points.add((x, y))
            # for _ in range(3):
            #     x, y = scatter_inside(_x, _y, 0.05)
            #     self._edge_diffusion_points.add((x, y))

        # scatter inside further
        point_list = list(self._points)
        for _ in range(3000):
            x, y = random.choice(point_list)
            x, y = scatter_inside(x, y, 0.17)
            self._center_diffusion_points.add((x, y))

    @staticmethod
    def calc_position(x, y, ratio):
        
        force = 1 / (((x - CANVAS_CENTER_X) ** 2 + (y - CANVAS_CENTER_Y) ** 2) ** 0.520)  

        dx = ratio * force * (x - CANVAS_CENTER_X) + random.randint(-1, 1)
        dy = ratio * force * (y - CANVAS_CENTER_Y) + random.randint(-1, 1)

        return x - dx, y - dy

    def calc(self, generate_frame):
        ratio = 10 * curve(generate_frame / 10 * pi)  

        halo_radius = int(4 + 6 * (1 + curve(generate_frame / 10 * pi)))
        halo_number = int(3000 + 4000 * abs(curve(generate_frame / 10 * pi) ** 2))

        all_points = []

        # halo
        heart_halo_point = set()  
        for _ in range(halo_number):
            t = random.uniform(0, 2 * pi)  
            x, y = heart_function(t, shrink_ratio=11.6)  
            x, y = shrink(x, y, halo_radius)
            if (x, y) not in heart_halo_point:
                # new points
                heart_halo_point.add((x, y))
                x += random.randint(-14, 14)
                y += random.randint(-14, 14)
                size = random.choice((1, 2, 2))
                all_points.append((x, y, size))

        # shape
        for x, y in self._points:
            x, y = self.calc_position(x, y, ratio)
            size = random.randint(1, 3)
            all_points.append((x, y, size))

        
        for x, y in self._edge_diffusion_points:
            x, y = self.calc_position(x, y, ratio)
            size = random.randint(1, 2)
            all_points.append((x, y, size))

        for x, y in self._center_diffusion_points:
            x, y = self.calc_position(x, y, ratio)
            size = random.randint(1, 2)
            all_points.append((x, y, size))

        self.all_points[generate_frame] = all_points

    def render(self, render_canvas, render_frame):
        for x, y, size in self.all_points[render_frame % self.generate_frame]:
            render_canvas.create_rectangle(x, y, x + size, y + size, width=0, fill=HEART_COLOR)


def draw(main: Tk, render_canvas: Canvas, render_heart: Heart, render_frame=0):
    render_canvas.delete('all')
    render_heart.render(render_canvas, render_frame)
    main.after(160, draw, main, render_canvas, render_heart, render_frame + 1)


if __name__ == '__main__':
    root = Tk() 
    canvas = Canvas(root, bg='black', height=CANVAS_HEIGHT, width=CANVAS_WIDTH)
    canvas.pack()
    heart = Heart()  
    draw(root, canvas, heart)  
    root.mainloop()