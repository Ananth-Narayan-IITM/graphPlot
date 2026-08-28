import numpy as np

import matplotlib
from matplotlib.colors import BoundaryNorm


class ColorScale:
    """
    Defines the color scale for a scientific plot.
    """

    def __init__(
        self,
        levels=30,
        cmap="viridis",
        vmin=None,
        vmax=None,
    ):
        self.levels = int(levels)
        self.cmap = cmap
        self.vmin = vmin
        self.vmax = vmax

        self._vmin = None
        self._vmax = None
        self.levels_array = None
        self.colormap = None
        self.norm = None

    def resolve(self, values):
        """
        Resolve the color scale using the supplied data.
        """

        values = np.asarray(values)

        if self.vmin is None:
            vmin = float(np.nanmin(values))
        else:
            vmin = float(self.vmin)

        if self.vmax is None:
            vmax = float(np.nanmax(values))
        else:
            vmax = float(self.vmax)

        if not np.isfinite(vmin):
            raise ValueError("Invalid vmin.")

        if not np.isfinite(vmax):
            raise ValueError("Invalid vmax.")

        if vmin >= vmax:
            raise ValueError("vmin must be smaller than vmax.")

        if self.levels < 1:
            raise ValueError("levels must be greater than zero.")

        self._vmin = vmin
        self._vmax = vmax

        self.levels_array = np.linspace(
            vmin,
            vmax,
            self.levels + 1,
        )

        self.colormap = matplotlib.colormaps.get_cmap(self.cmap).resampled(self.levels)

        self.norm = BoundaryNorm(
            self.levels_array,
            self.colormap.N,
        )

        return self

    @property
    def limits(self):

        if self._vmin is None:
            raise RuntimeError("ColorScale has not been resolved.")

        return (
            self._vmin,
            self._vmax,
        )
