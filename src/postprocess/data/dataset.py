class DataSet:
    """
    Generic scientific dataset.

    Contains geometry and associated fields.
    """

    def __init__(
        self,
        mesh,
        point_data=None,
        cell_data=None,
    ):

        self.mesh = mesh

        self.point_data = point_data if point_data is not None else {}

        self.cell_data = cell_data if cell_data is not None else {}

    def get_field(
        self,
        name,
        association="cell",
    ):

        if association == "cell":
            if name not in self.cell_data:
                raise KeyError(
                    f"Cell field '{name}' not found.\n"
                    f"Available fields: "
                    f"{list(self.cell_data.keys())}"
                )

            return self.cell_data[name]

        if association == "point":
            if name not in self.point_data:
                raise KeyError(
                    f"Point field '{name}' not found.\n"
                    f"Available fields: "
                    f"{list(self.point_data.keys())}"
                )

            return self.point_data[name]

        raise ValueError("association must be either 'cell' or 'point'.")
