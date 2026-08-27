import numpy as np
import matplotlib.pyplot as plt


class VectorPlot:
    """
    Plot 2D vector fields from a PyVista dataset.

    Supports point-data and cell-data vector fields.
    """

    def __init__(
        self,
        data,
        field,
        association="auto",
    ):
        self.data = data
        self.field = field

        if association not in (
            "auto",
            "point",
            "cell",
        ):
            raise ValueError(
                "association must be 'auto', "
                "'point', or 'cell'."
            )

        self.association = association

    # =====================================================
    # Get vector data
    # =====================================================

    def _get_vectors(self):
        """
        Extract vector data from the dataset.

        Supports both the project's VTPData wrapper
        and raw PyVista datasets.
        """

        data = self._get_dataset()

        # -------------------------------------------------
        # Explicit point association
        # -------------------------------------------------

        if self.association == "point":

            if self.field not in data.point_data:
                raise KeyError(
                    "Vector field '{}' is not available "
                    "as point data.".format(
                        self.field
                    )
                )

            vectors = np.asarray(
                data.point_data[self.field]
            )

            coordinates = np.asarray(
                data.points
            )

            return coordinates, vectors

        # -------------------------------------------------
        # Explicit cell association
        # -------------------------------------------------

        if self.association == "cell":

            if self.field not in data.cell_data:
                raise KeyError(
                    "Vector field '{}' is not available "
                    "as cell data.".format(
                        self.field
                    )
                )

            vectors = np.asarray(
                data.cell_data[self.field]
            )

            coordinates = np.asarray(
                data.cell_centers().points
            )

            return coordinates, vectors

        # -------------------------------------------------
        # Automatic detection
        # -------------------------------------------------

        if self.field in data.point_data:

            vectors = np.asarray(
                data.point_data[self.field]
            )

            coordinates = np.asarray(
                data.points
            )

            return coordinates, vectors

        if self.field in data.cell_data:

            vectors = np.asarray(
                data.cell_data[self.field]
            )

            coordinates = np.asarray(
                data.cell_centers().points
            )

            return coordinates, vectors

        raise KeyError(
            "Vector field '{}' was not found "
            "in point or cell data.".format(
                self.field
            )
        )
    # =====================================================
    # Validate vectors
    # =====================================================

    @staticmethod
    def _validate_vectors(vectors):
        """
        Validate vector array shape.
        """

        vectors = np.asarray(
            vectors
        )

        if vectors.ndim != 2:
            raise ValueError(
                "Vector field must be a 2D array."
            )

        if vectors.shape[1] not in (
            2,
            3,
        ):
            raise ValueError(
                "Vector field must have 2 or 3 "
                "components."
            )

        return vectors

    # =====================================================
    # Downsample
    # =====================================================

    @staticmethod
    def _downsample(
        coordinates,
        vectors,
        density,
    ):
        """
        Reduce the number of arrows.

        density is approximately the desired number
        of arrows along the smaller spatial dimension.
        """

        if density is None:
            return coordinates, vectors

        if density <= 0:
            raise ValueError(
                "density must be greater than zero."
            )

        x = coordinates[:, 0]
        y = coordinates[:, 1]

        xmin = np.min(x)
        xmax = np.max(x)

        ymin = np.min(y)
        ymax = np.max(y)

        width = xmax - xmin
        height = ymax - ymin

        if width <= 0 or height <= 0:
            return coordinates, vectors

        # -------------------------------------------------
        # Determine grid spacing
        # -------------------------------------------------

        if width >= height:

            nx = density
            ny = max(
                1,
                int(
                    density
                    * height
                    / width
                ),
            )

        else:

            ny = density
            nx = max(
                1,
                int(
                    density
                    * width
                    / height
                ),
            )

        dx = width / nx
        dy = height / ny

        if dx == 0 or dy == 0:
            return coordinates, vectors

        ix = np.floor(
            (x - xmin) / dx
        ).astype(int)

        iy = np.floor(
            (y - ymin) / dy
        ).astype(int)

        ix = np.clip(
            ix,
            0,
            nx - 1,
        )

        iy = np.clip(
            iy,
            0,
            ny - 1,
        )

        cell_id = iy * nx + ix

        selected = []

        for identifier in np.unique(
            cell_id
        ):

            indices = np.where(
                cell_id == identifier
            )[0]

            if len(indices) == 0:
                continue

            # Use the vector nearest to the
            # average location of this bin.

            center = np.mean(
                coordinates[indices, :2],
                axis=0,
            )

            distance = np.sum(
                (
                    coordinates[
                        indices,
                        :2,
                    ]
                    - center
                ) ** 2,
                axis=1,
            )

            selected.append(
                indices[
                    np.argmin(distance)
                ]
            )

        selected = np.asarray(
            selected,
            dtype=int,
        )

        return (
            coordinates[selected],
            vectors[selected],
        )

    # =====================================================
    # Plot
    # =====================================================

    def plot(
        self,
        axes,
        density=20,
        scale=1.0,
        width=0.002,
        color="black",
        alpha=1.0,
        normalize=False,
        magnitude_color=False,
        cmap="viridis",
        pivot="mid",
        zorder=5,
        **kwargs,
    ):
        """
        Plot a 2D vector field.

        Parameters
        ----------
        axes:
            Matplotlib Axes.

        density:
            Approximate number of arrows along the
            smaller spatial dimension.

        scale:
            Quiver scale parameter.

        width:
            Arrow shaft width.

        normalize:
            Normalize all vectors to unit magnitude.

        magnitude_color:
            Color arrows according to vector magnitude.

        cmap:
            Colormap used when magnitude_color=True.
        """

        coordinates, vectors = (
            self._get_vectors()
        )

        vectors = self._validate_vectors(
            vectors
        )

        # -------------------------------------------------
        # Keep only x/y components
        # -------------------------------------------------

        x = coordinates[:, 0]
        y = coordinates[:, 1]

        u = vectors[:, 0]
        v = vectors[:, 1]

        # -------------------------------------------------
        # Remove invalid vectors
        # -------------------------------------------------

        valid = (
            np.isfinite(x)
            & np.isfinite(y)
            & np.isfinite(u)
            & np.isfinite(v)
        )

        x = x[valid]
        y = y[valid]
        u = u[valid]
        v = v[valid]

        coordinates = np.column_stack(
            [x, y]
        )

        vectors = np.column_stack(
            [u, v]
        )

        # -------------------------------------------------
        # Normalize
        # -------------------------------------------------

        if normalize:

            magnitude = np.sqrt(
                u ** 2 + v ** 2
            )

            nonzero = (
                magnitude > 0
            )

            u_normalized = np.zeros_like(
                u
            )

            v_normalized = np.zeros_like(
                v
            )

            u_normalized[nonzero] = (
                u[nonzero]
                / magnitude[nonzero]
            )

            v_normalized[nonzero] = (
                v[nonzero]
                / magnitude[nonzero]
            )

            u = u_normalized
            v = v_normalized

            vectors = np.column_stack(
                [u, v]
            )

        # -------------------------------------------------
        # Downsample
        # -------------------------------------------------

        coordinates, vectors = (
            self._downsample(
                coordinates,
                vectors,
                density,
            )
        )

        x = coordinates[:, 0]
        y = coordinates[:, 1]

        u = vectors[:, 0]
        v = vectors[:, 1]

        # -------------------------------------------------
        # Arrow colors
        # -------------------------------------------------

        if magnitude_color:

            magnitude = np.sqrt(
                u ** 2 + v ** 2
            )

            quiver = axes.quiver(
                x,
                y,
                u,
                v,
                magnitude,
                cmap=cmap,
                scale=scale,
                width=width,
                alpha=alpha,
                pivot=pivot,
                zorder=zorder,
                **kwargs,
            )

        else:

            quiver = axes.quiver(
                x,
                y,
                u,
                v,
                color=color,
                scale=scale,
                width=width,
                alpha=alpha,
                pivot=pivot,
                zorder=zorder,
                **kwargs,
            )

        return quiver
    # =====================================================
    # Underlying dataset
    # =====================================================

    def _get_dataset(self):
        """
        Return the underlying PyVista dataset.

        Supports both a raw PyVista dataset and the
        project's VTPData wrapper.
        """

        if hasattr(self.data, "dataset"):
            return self.data.dataset

        return self.data