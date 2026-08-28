from matplotlib.collections import PolyCollection


class MeshPlot:
    """
    Plot the original computational mesh.
    """

    def __init__(self, data):

        self.data = data
        self.mesh = data.mesh

    def plot(
        self,
        axes,
        edgecolor="black",
        facecolor="none",
        linewidth=0.15,
        alpha=0.30,
    ):
        """
        Plot the original mesh.

        Parameters
        ----------
        axes
            Matplotlib axes.

        edgecolor
            Color of the cell boundaries.

        facecolor
            Face color of the cells.
            Use "none" to keep the underlying
            contour visible.

        linewidth
            Width of the cell boundaries.

        alpha
            Transparency of the mesh.

        Returns
        -------
        PolyCollection
            Matplotlib mesh collection.
        """

        collection = PolyCollection(
            self.mesh.polygons,
            facecolors=facecolor,
            edgecolors=edgecolor,
            linewidths=linewidth,
            alpha=alpha,
        )

        axes.add_collection(collection)

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

        axes.grid(False)

        return collection