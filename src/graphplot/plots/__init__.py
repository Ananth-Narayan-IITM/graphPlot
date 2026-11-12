"""Plot implementations."""

from graphplot.plots.contour import ColorScale, plot_field_contour
from graphplot.plots.mesh import plot_mesh
from graphplot.plots.streamline import plot_streamlines
from graphplot.plots.vector import plot_vectors

__all__ = [
    "ColorScale",
    "plot_field_contour",
    "plot_mesh",
    "plot_streamlines",
    "plot_vectors",
]
