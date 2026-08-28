import numpy as np
from matplotlib.collections import PolyCollection

from postprocess.layout.colors import ColorScale


class ContourPlot:
    """
    Create a cell-centered scalar contour plot.

    The field is associated with mesh cells.
    """

    def __init__(
        self,
        data,
        field,
        association="cell",
    ):
        """
        Parameters
        ----------
        data
            Post-processing dataset.

        field
            Name of the scalar field.

        association
            Location of the field:
            "cell" or "point".
        """

        self.data = data
        self.field = field
        self.association = association

        self.values = np.asarray(
            data.get_field(
                field,
                association,
            )
        )

        self.mesh = data.mesh

    def plot(
        self,
        axes,
        scale=None,
        rasterize=True,
    ):
        """
        Plot the scalar field.

        Parameters
        ----------
        axes
            Matplotlib axes.

        levels
            Number of discrete color levels.

        cmap
            Matplotlib colormap.

        vmin, vmax
            Color limits.

        Returns
        -------
        matplotlib.collections.PolyCollection
            Contour collection.
        """

        # -------------------------------------------------
        # Validate field
        # -------------------------------------------------
        if scale is None:
            scale = ColorScale()

        scale.resolve(self.values)
        if self.association != "cell":
            raise NotImplementedError(
                "ContourPlot currently supports cell-associated data only."
            )

        if len(self.values) != self.mesh.n_cells:
            raise ValueError(
                "Number of field values does not match "
                "number of mesh cells.\n"
                f"Field values: {len(self.values)}\n"
                f"Mesh cells:   {self.mesh.n_cells}"
            )

        # -------------------------------------------------
        # Get mesh polygons
        # -------------------------------------------------

        polygons = self.mesh.polygons

        # -------------------------------------------------
        # Create polygon collection
        # -------------------------------------------------

        collection = PolyCollection(
            polygons,
            array=self.values,
            cmap=scale.colormap,
            norm=scale.norm,
            edgecolors="none",
            linewidths=0.0,
            antialiased=False,
        )

        if rasterize:
            collection.set_rasterized(True)

        # -------------------------------------------------
        # Add to axes
        # -------------------------------------------------

        axes.add_collection(collection)

        # -------------------------------------------------
        # Set geometry limits
        # -------------------------------------------------

        x_min, x_max, y_min, y_max = self.mesh.bounds

        axes.set_xlim(
            x_min,
            x_max,
        )

        axes.set_ylim(
            y_min,
            y_max,
        )

        # -------------------------------------------------
        # Disable Matplotlib grid
        # -------------------------------------------------

        axes.grid(False)

        return collection
