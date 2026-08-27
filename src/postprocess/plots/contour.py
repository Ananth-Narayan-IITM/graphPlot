import numpy as np

from matplotlib import cm
from matplotlib.collections import PolyCollection
from matplotlib.colors import BoundaryNorm


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
        levels=30,
        cmap="viridis",
        vmin=None,
        vmax=None,
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

        if self.association != "cell":
            raise NotImplementedError(
                "ContourPlot currently supports "
                "cell-associated data only."
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
        # Determine color limits
        # -------------------------------------------------

        if vmin is None:
            vmin = np.nanmin(self.values)

        if vmax is None:
            vmax = np.nanmax(self.values)

        if vmin >= vmax:
            raise ValueError(
                f"Invalid color limits: "
                f"vmin={vmin}, vmax={vmax}"
            )

        # -------------------------------------------------
        # Create contour levels
        # -------------------------------------------------

        levels_array = np.linspace(
            vmin,
            vmax,
            levels + 1,
        )

        # -------------------------------------------------
        # Create colormap
        # -------------------------------------------------

        colormap = cm.get_cmap(
            cmap,
            levels,
        )

        norm = BoundaryNorm(
            levels_array,
            colormap.N,
        )

        # -------------------------------------------------
        # Create polygon collection
        # -------------------------------------------------

        collection = PolyCollection(
            polygons,
            array=self.values,
            cmap=colormap,
            norm=norm,
            edgecolors="none",
            linewidths=0.0,
            antialiased=True,
        )

        # -------------------------------------------------
        # Add to axes
        # -------------------------------------------------

        axes.add_collection(collection)

        # -------------------------------------------------
        # Set geometry limits
        # -------------------------------------------------

        x_min, x_max, y_min, y_max = (
            self.mesh.bounds
        )

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