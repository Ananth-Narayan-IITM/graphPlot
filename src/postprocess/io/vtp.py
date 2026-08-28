from pathlib import Path
from typing import Union

import pyvista as pv

from postprocess.data.dataset import DataSet
from postprocess.data.mesh import Mesh


class VTPData:
    """
    Data loaded from a VTP file.
    """

    def __init__(
        self,
        dataset,
        filename,
    ):

        self.dataset = dataset
        self.filename = Path(filename)

        self._data = self._create_dataset()

    def _create_dataset(self):

        points = self.dataset.points

        faces = self.dataset.faces

        cells = []

        index = 0

        while index < len(faces):
            n_points = faces[index]

            cell = faces[index + 1 : index + 1 + n_points]

            cells.append(cell)

            index += n_points + 1

        mesh = Mesh(
            points=points,
            cells=cells,
        )

        return DataSet(
            mesh=mesh,
            point_data=dict(self.dataset.point_data),
            cell_data=dict(self.dataset.cell_data),
        )

    @property
    def mesh(self):

        return self._data.mesh

    @property
    def point_data(self):

        return self._data.point_data

    @property
    def cell_data(self):

        return self._data.cell_data

    @property
    def bounds(self):

        return self.dataset.bounds

    @property
    def n_points(self):

        return self.dataset.n_points

    @property
    def n_cells(self):

        return self.dataset.n_cells

    def get_field(
        self,
        name,
        association="cell",
    ):

        return self._data.get_field(
            name,
            association,
        )


def read_vtp(
    filename: Union[str, Path],
):

    filename = Path(filename)

    if not filename.exists():
        raise FileNotFoundError(f"VTP file not found: {filename}")

    dataset = pv.read(filename)

    return VTPData(
        dataset,
        filename,
    )
