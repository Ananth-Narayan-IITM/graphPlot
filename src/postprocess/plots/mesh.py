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
        color="black",
        linewidth=0.25,
        alpha=0.5,
    ):
        """
        Plot the original mesh.

        Parameters
        ----------
        axes
            Matplotlib axes.

        color
            Mesh line color.

        linewidth
            Mesh line width.

        alpha
            Mesh transparency.

        Returns
        -------
        PolyCollection
            Matplotlib mesh collection.
        """

        collection = PolyCollection(
            self.mesh.polygons,
            facecolors="none",
            edgecolors=color,
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

        # No Matplotlib background grid.
        axes.grid(False)

        return collection