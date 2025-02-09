import math

from ursina import Ursina, Color, Texture, mouse, color, camera, Vec3, Entity
from PIL import Image
from ursina.camera import Camera

app = Ursina()


def set_pixel(x: int, y: int, tex: Texture, pix_color: Color):
    try:
        if tex.get_pixel(x, y) == pix_color:
            return
    except: pass

    try:
        tex.set_pixel(x, y, pix_color)
    except IndexError:
        print(f"Failed to set pixed at {(x, y)}")
    else:
        print(f"Set pixel at {(x, y)}")


def draw_line(x1: int, y1: int, x2: int, y2: int, tex: Texture, pix_color: Color):
    slope = (y2 - y1) / (x2 - x1)
    b = y1 - slope * x1  # y-intercept

    start: int
    end: int
    step: int

    if abs(slope) < 1:
        # Angle with x-axis is less than 90 degrees. Iterate in terms of x

        if x1 < x2:
            start = x1
            end = x2 + 1
        else:
            start = x2
            end = x1 + 1

        for xi in range(start, end):
            yi = round(slope * xi + b)
            set_pixel(xi, yi, tex, pix_color)
    else:
        # Angle with x-axis is greater than 90 degrees. Iterate in terms of y

        if y1 < y2:
            start = y1
            end = y2 + 1
        else:
            start = y2
            end = y1 + 1

        for yi in range(start, end):
            xi = round((yi - y1) / slope + x1)
            set_pixel(xi, yi, tex, pix_color)


def draw_vertical(x: int, y1: int, y2: int, tex: Texture, pix_color: Color):
    start: int
    end: int

    if y1 < y2:
        start = y1
        end = y2 + 1
    else:
        start = y2
        end = y1 + 1

    for yi in range(start, end):
        set_pixel(x, yi, tex, pix_color)


class Canvas(Entity):
    def __init__(self, add_to_scene_entities=True, **kwargs):
        super().__init__(add_to_scene_entities, **kwargs)
        self.last_x = 0
        self.last_y = 0

    def update(self):
        loc = mouse.point

        if loc is not None:
            x = math.floor((loc.x + 0.5) * size)
            y = math.floor((loc.z + 0.5) * size)

            if mouse.left or mouse.right:
                pix_color = color.black if mouse.left else color.white

                x_diff = abs(self.last_x - x)
                y_diff = abs(self.last_y - y)

                if x_diff <= 1 and y_diff <= 1:
                    # just a pixel away, approximately. only have to write on pixel
                    set_pixel(x, y, self.texture, pix_color)
                elif x_diff == 0:
                    draw_vertical(x, self.last_y, y, self.texture, pix_color)
                else:
                    draw_line(self.last_x, self.last_y, x, y, self.texture, pix_color)

                self.texture.apply()

            self.last_x = x
            self.last_y = y


size = 64
canvas_texture = Texture(Image.new(mode="RGBA", size=(size, size), color=(255, 255, 255, 255)))
c = Canvas(model='plane', texture=canvas_texture, collider='box')

cam: Camera = camera
cam.position = Vec3(0, 3, 0)
cam.look_at(Vec3(0, 0, 0), axis='forward')

app.run()
