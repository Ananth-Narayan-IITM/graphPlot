import numpy as np


class Mesh:
    """
    Representation of a 2D polygonal mesh.
    """

    def __init__(self, points, cells):

        self.points = np.asarray(points)
        self.cells = cells

    @property
    def n_points(self):
        return len(self.points)

    @property
    def n_cells(self):
        return len(self.cells)

    @property
    def bounds(self):

        x = self.points[:, 0]
        y = self.points[:, 1]

        return (
            np.min(x),
            np.max(x),
            np.min(y),
            np.max(y),
        )

    @property
    def polygons(self):

        polygons = []

        for cell in self.cells:
            polygons.append(self.points[cell][:, :2])

        return polygons
