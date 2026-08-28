import numpy as np


class Data1D:
    """
    Generic one-dimensional scientific dataset.

    Parameters
    ----------
    x : array-like
        Independent variable.

    y : array-like
        Dependent variable.

    label : str, optional
        Dataset label.

    x_label : str, optional
        Label for x-axis.

    y_label : str, optional
        Label for y-axis.

    x_unit : str, optional
        Unit of x.

    y_unit : str, optional
        Unit of y.

    metadata : dict, optional
        Additional metadata.
    """

    def __init__(
        self,
        x,
        y,
        label=None,
        x_label=None,
        y_label=None,
        x_unit=None,
        y_unit=None,
        metadata=None,
    ):

        self.x = np.asarray(
            x,
            dtype=float,
        )

        self.y = np.asarray(
            y,
            dtype=float,
        )

        if self.x.ndim != 1:
            raise ValueError("x must be a one-dimensional array.")

        if self.y.ndim != 1:
            raise ValueError("y must be a one-dimensional array.")

        if len(self.x) != len(self.y):
            raise ValueError("x and y must have the same length.")

        self.label = label

        self.x_label = x_label
        self.y_label = y_label

        self.x_unit = x_unit
        self.y_unit = y_unit

        self.metadata = {} if metadata is None else dict(metadata)

    # =====================================================
    # Basic information
    # =====================================================

    @property
    def size(self):
        """Number of data points."""
        return len(self.x)

    @property
    def x_min(self):
        return np.min(self.x)

    @property
    def x_max(self):
        return np.max(self.x)

    @property
    def y_min(self):
        return np.min(self.y)

    @property
    def y_max(self):
        return np.max(self.y)

    # =====================================================
    # Remove invalid values
    # =====================================================

    def remove_invalid(self):
        """
        Remove NaN and infinite values.

        Returns
        -------
        Data1D
            Cleaned dataset.
        """

        valid = np.isfinite(self.x) & np.isfinite(self.y)

        return Data1D(
            self.x[valid],
            self.y[valid],
            label=self.label,
            x_label=self.x_label,
            y_label=self.y_label,
            x_unit=self.x_unit,
            y_unit=self.y_unit,
            metadata=self.metadata,
        )

    # =====================================================
    # Sort
    # =====================================================

    def sort(self):
        """
        Sort data according to x.

        Returns
        -------
        Data1D
            Sorted dataset.
        """

        order = np.argsort(self.x)

        return Data1D(
            self.x[order],
            self.y[order],
            label=self.label,
            x_label=self.x_label,
            y_label=self.y_label,
            x_unit=self.x_unit,
            y_unit=self.y_unit,
            metadata=self.metadata,
        )

    # =====================================================
    # Representation
    # =====================================================

    def __len__(self):
        return self.size

    def __repr__(self):

        return f"Data1D(size={self.size}, x=[{self.x_min}, {self.x_max}], y=[{self.y_min}, {self.y_max}])"

    # =====================================================
    # Scaling
    # =====================================================

    def scale_x(
        self,
        scale,
        label=None,
        unit=None,
    ):
        """
        Return a new Data1D with x scaled by `scale`.

        x_new = x / scale

        The original dataset is not modified.

        Parameters
        ----------
        scale : float
            Scaling reference.

        label : str, optional
            New x-axis label.

        unit : str, optional
            New x-axis unit.

        Returns
        -------
        Data1D
            Scaled dataset.
        """

        scale = float(scale)

        if scale == 0.0:
            raise ValueError("x scale cannot be zero.")

        return Data1D(
            x=self.x / scale,
            y=self.y.copy(),
            label=self.label,
            x_label=(self.x_label if label is None else label),
            y_label=self.y_label,
            x_unit=(self.x_unit if unit is None else unit),
            y_unit=self.y_unit,
            metadata=self.metadata.copy(),
        )

    def scale_y(
        self,
        scale,
        label=None,
        unit=None,
    ):
        """
        Return a new Data1D with y scaled by `scale`.

        y_new = y / scale

        The original dataset is not modified.

        Parameters
        ----------
        scale : float
            Scaling reference.

        label : str, optional
            New y-axis label.

        unit : str, optional
            New y-axis unit.

        Returns
        -------
        Data1D
            Scaled dataset.
        """

        scale = float(scale)

        if scale == 0.0:
            raise ValueError("y scale cannot be zero.")

        return Data1D(
            x=self.x.copy(),
            y=self.y / scale,
            label=self.label,
            x_label=self.x_label,
            y_label=(self.y_label if label is None else label),
            x_unit=self.x_unit,
            y_unit=(self.y_unit if unit is None else unit),
            metadata=self.metadata.copy(),
        )
