

# https://en.wikipedia.org/wiki/Quadtree#Point_quadtree
# https://www.youtube.com/watch?v=OJxEcs0w_kE&vl
# https://www.pygame.org/wiki/QuadTree

from collections import namedtuple
import pygame


RECT_COLOR = (0, 0, 255)
POINT_COLOR = (0, 255, 0)


Point = namedtuple('Point', ['x', 'y'])


class Rectangle:
    # Can use floats while pygame.Rect must have integer dimensions.
    def __init__(self, left, top, right, bottom):
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom
        self.width = self.right - self.left
        self.height = self.bottom - self.top
        self.center_x = (self.left + self.right) / 2
        self.center_y = (self.top + self.bottom) / 2

        # width and height + 1 to make the lines 1 pixel wide by overlapping
        # neighboring edges
        self.visible_rect = pygame.Rect(
            self.left, self.top,
            self.width + 1, self.height + 1
        )

    def collide_point(self, point):
        # A point on the right or bottom edge is not considered to be
        # inside the reclangle.
        return self.left <= point.x < self.right and self.top <= point.y < self.bottom

    def intersect(self, other):
        pass

    def __str__(self):
        return f"Rectangle(left={self.left}, top={self.top}, right={self.right}, bottom={self.bottom})"


class PointQuadtree:
    def __init__(self, left, top, right, bottom, capacity=4, depth=10):
        self.boundary = Rectangle(left, top, right, bottom)
        self.capacity = capacity  # How many elements before it subdivides.
        self.points = []
        self.depth = depth - 1  # Recursion limit. Don't subdivide if depth == 0

        self.is_divided = False
        self.north_west = None
        self.north_east = None
        self.south_west = None
        self.south_east = None

    def insert(self, point):
        if not self.boundary.collide_point(point):
            # Point does not belong here.
            return False

        if self.depth == 0:
            self.points.append(point)
            return True
        elif not self.is_divided:
            if len(self.points) < self.capacity:
                self.points.append(point)
                return True
            else:
                self.subdivide()

        # FIXME: It would be enough to check if the point is left or right
        #  and above ot below the center. If it is outside this rect then it
        #  wouldn't be here. Just need to handle the root rect differently
        #  because that one has outside borders?
        #  Check if this makes it faster!
        if self.north_west.insert(point) or \
                self.north_east.insert(point) or \
                self.south_west.insert(point) or \
                self.south_east.insert(point):
            return True

        # Point cannot be inserted for some unknown reason. This should never happen.
        raise Exception(f"{point} can not be inserted into {self.boundary}")

    def subdivide(self):
        # remember to add the points to the children afterwards using insert into self
        self.north_west = PointQuadtree(
            self.boundary.left, self.boundary.top,
            self.boundary.center_x, self.boundary.center_y,
            self.capacity, self.depth
        )
        self.north_east = PointQuadtree(
            self.boundary.center_x, self.boundary.top,
            self.boundary.right, self.boundary.center_y,
            self.capacity, self.depth
        )
        self.south_west = PointQuadtree(
            self.boundary.left, self.boundary.center_y,
            self.boundary.center_x, self.boundary.bottom,
            self.capacity, self.depth
        )
        self.south_east = PointQuadtree(
            self.boundary.center_x, self.boundary.center_y,
            self.boundary.right, self.boundary.bottom,
            self.capacity, self.depth
        )

        self.is_divided = True
        while self.points:
            self.insert(self.points.pop())

    def draw(self, target_surface):
        if self.is_divided:
            self.north_west.draw(target_surface)
            self.north_east.draw(target_surface)
            self.south_west.draw(target_surface)
            self.south_east.draw(target_surface)
        else:
            pygame.draw.rect(
                target_surface, RECT_COLOR,
                self.boundary.visible_rect, width=1
            )
            for p in self.points:
                pygame.draw.circle(target_surface, POINT_COLOR, p, 1)
