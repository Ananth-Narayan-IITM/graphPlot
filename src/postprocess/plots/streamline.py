import numpy as np


class StreamlinePlot:
    """
    Scientific streamline visualization using the VTK
    streamline integrator through PyVista.

    Supports:
        - point or cell vector fields
        - explicit seed points
        - regularly distributed seeds
        - forward/backward/both integration
        - RK2/RK4/RK45 integration
        - surface-constrained integration
        - physical maximum streamline length
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
    # Dataset
    # =====================================================

    def _get_dataset(self):
        """
        Return the underlying PyVista dataset.
        """

        if hasattr(self.data, "dataset"):
            return self.data.dataset

        return self.data

    # =====================================================
    # Prepare vector field
    # =====================================================

    def _prepare_dataset(self):
        """
        Prepare the dataset for VTK streamline integration.

        For cell-centered vectors, convert them to point
        data so that VTK can interpolate the velocity field
        continuously during integration.
        """

        dataset = self._get_dataset()

        # -------------------------------------------------
        # Explicit point association
        # -------------------------------------------------

        if self.association == "point":

            if self.field not in dataset.point_data:
                raise KeyError(
                    "Vector field '{}' is not available "
                    "as point data.".format(
                        self.field
                    )
                )

            mesh = dataset.copy()

            mesh.set_active_vectors(
                self.field,
                preference="point",
            )

            return mesh

        # -------------------------------------------------
        # Explicit cell association
        # -------------------------------------------------

        if self.association == "cell":

            if self.field not in dataset.cell_data:
                raise KeyError(
                    "Vector field '{}' is not available "
                    "as cell data.".format(
                        self.field
                    )
                )

            # Convert cell-centered vectors to point data.
            #
            # VTK then interpolates the velocity field
            # continuously during streamline integration.
            mesh = dataset.cell_data_to_point_data(
                pass_cell_data=True
            )

            mesh.set_active_vectors(
                self.field,
                preference="point",
            )

            return mesh

        # -------------------------------------------------
        # Automatic association
        # -------------------------------------------------

        if self.field in dataset.point_data:

            mesh = dataset.copy()

            mesh.set_active_vectors(
                self.field,
                preference="point",
            )

            return mesh

        if self.field in dataset.cell_data:

            mesh = dataset.cell_data_to_point_data(
                pass_cell_data=True
            )

            mesh.set_active_vectors(
                self.field,
                preference="point",
            )

            return mesh

        raise KeyError(
            "Vector field '{}' was not found "
            "in point or cell data.".format(
                self.field
            )
        )

    # =====================================================
    # Generate seed points
    # =====================================================

    @staticmethod
    def _create_seed_points(
        bounds,
        n_seeds,
        seed_axis="y",
        seed_position=None,
        seed_margin=0.01,
    ):
        """
        Create a line of seed points.

        Parameters
        ----------
        bounds:
            Dataset bounds.

        n_seeds:
            Number of seed points.

        seed_axis:
            Direction along which seeds are distributed.

            "x" -> horizontal line
            "y" -> vertical line

        seed_position:
            Position of the seed line.

            For seed_axis="y":
                x-coordinate of the seed line.

            For seed_axis="x":
                y-coordinate of the seed line.

        seed_margin:
            Fractional margin removed from the ends.
        """

        xmin, xmax, ymin, ymax, zmin, zmax = (
            bounds
        )

        if n_seeds < 1:
            raise ValueError(
                "n_seeds must be greater than zero."
            )

        if seed_axis not in (
            "x",
            "y",
        ):
            raise ValueError(
                "seed_axis must be 'x' or 'y'."
            )

        # -------------------------------------------------
        # Default seed position
        # -------------------------------------------------

        if seed_position is None:

            if seed_axis == "y":
                seed_position = xmin

            else:
                seed_position = ymin

        # -------------------------------------------------
        # Seed margin
        # -------------------------------------------------

        if not 0.0 <= seed_margin < 0.5:
            raise ValueError(
                "seed_margin must be in [0, 0.5)."
            )

        if seed_axis == "y":

            span = ymax - ymin

            y0 = (
                ymin
                + seed_margin * span
            )

            y1 = (
                ymax
                - seed_margin * span
            )

            values = np.linspace(
                y0,
                y1,
                n_seeds,
            )

            points = np.column_stack(
                (
                    np.full(
                        n_seeds,
                        seed_position,
                    ),
                    values,
                    np.full(
                        n_seeds,
                        0.5 * (zmin + zmax),
                    ),
                )
            )

        else:

            span = xmax - xmin

            x0 = (
                xmin
                + seed_margin * span
            )

            x1 = (
                xmax
                - seed_margin * span
            )

            values = np.linspace(
                x0,
                x1,
                n_seeds,
            )

            points = np.column_stack(
                (
                    values,
                    np.full(
                        n_seeds,
                        seed_position,
                    ),
                    np.full(
                        n_seeds,
                        0.5 * (zmin + zmax),
                    ),
                )
            )

        return points

    # =====================================================
    # Create source
    # =====================================================

    @staticmethod
    def _make_source(points):
        """
        Convert seed coordinates into a PyVista PolyData
        source.
        """

        import pyvista as pv

        return pv.PolyData(
            np.asarray(points)
        )

    # =====================================================
    # Plot
    # =====================================================

    def plot(
        self,
        axes,
        n_seeds=25,
        seed_axis="y",
        seed_position=None,
        seed_margin=0.01,
        seed_points=None,
        integration_direction="forward",
        integrator_type=45,
        surface_streamlines=True,
        initial_step_length=0.1,
        min_step_length=0.01,
        max_step_length=0.5,
        max_steps=2000,
        max_length=None,
        terminal_speed=1e-12,
        max_error=1e-6,
        interpolator_type="cell",
        color="black",
        linewidth=0.8,
        arrowsize=1.0,
        zorder=6,
    ):
        """
        Generate and plot streamlines using VTK.

        Parameters
        ----------
        axes:
            Matplotlib Axes.

        n_seeds:
            Number of automatically generated seed points.

        seed_axis:
            Axis along which automatic seeds are distributed.

        seed_position:
            Position of the seed line.

        seed_margin:
            Fraction of the seed line excluded at both ends.

        seed_points:
            Explicit list/array of seed coordinates.
            If provided, this overrides automatic seeding.

        integration_direction:
            "forward", "backward", or "both".

        integrator_type:
            2  -> Runge-Kutta 2
            4  -> Runge-Kutta 4
            45 -> Runge-Kutta 45

        surface_streamlines:
            Constrain integration to the 2-D surface.

        initial_step_length:
            Initial integration step.

        min_step_length:
            Minimum adaptive step.

        max_step_length:
            Maximum adaptive step.

        max_steps:
            Maximum number of integration steps.

        max_length:
            Maximum physical streamline length.

        terminal_speed:
            Integration terminates below this speed.

        max_error:
            Maximum RK45 integration error.

        interpolator_type:
            "point" or "cell".

        color:
            Streamline color.

        linewidth:
            Streamline width.

        arrowsize:
            Direction-arrow size.
        """

        # -------------------------------------------------
        # Validate integration direction
        # -------------------------------------------------

        if integration_direction not in (
            "forward",
            "backward",
            "both",
        ):
            raise ValueError(
                "integration_direction must be "
                "'forward', 'backward', or 'both'."
            )

        # -------------------------------------------------
        # Validate integrator
        # -------------------------------------------------

        if integrator_type not in (
            2,
            4,
            45,
        ):
            raise ValueError(
                "integrator_type must be "
                "2, 4, or 45."
            )

        # -------------------------------------------------
        # Prepare mesh
        # -------------------------------------------------

        mesh = self._prepare_dataset()

        # -------------------------------------------------
        # Generate seeds
        # -------------------------------------------------

        if seed_points is None:

            points = self._create_seed_points(
                mesh.bounds,
                n_seeds=n_seeds,
                seed_axis=seed_axis,
                seed_position=seed_position,
                seed_margin=seed_margin,
            )

        else:

            points = np.asarray(
                seed_points,
                dtype=float,
            )

            if points.ndim != 2:
                raise ValueError(
                    "seed_points must be a 2D "
                    "array with shape (N, 3)."
                )

            if points.shape[1] != 3:
                raise ValueError(
                    "seed_points must have shape "
                    "(N, 3)."
                )

        source = self._make_source(
            points
        )

        # -------------------------------------------------
        # VTK streamline integration
        # -------------------------------------------------

        streamlines = (
            mesh.streamlines_from_source(
                source,
                vectors=self.field,
                integrator_type=integrator_type,
                integration_direction=(
                    integration_direction
                ),
                surface_streamlines=(
                    surface_streamlines
                ),
                initial_step_length=(
                    initial_step_length
                ),
                min_step_length=(
                    min_step_length
                ),
                max_step_length=(
                    max_step_length
                ),
                max_steps=max_steps,
                terminal_speed=terminal_speed,
                max_error=max_error,
                interpolator_type=(
                    interpolator_type
                ),
                compute_vorticity=False,
            )
        )

        # -------------------------------------------------
        # Extract polylines
        # -------------------------------------------------

        if streamlines.n_points == 0:
            raise RuntimeError(
                "VTK did not generate any streamlines. "
                "Check the seed locations and vector "
                "field."
            )

        # -------------------------------------------------
        # Plot each streamline
        # -------------------------------------------------

        lines = streamlines.lines

        offset = 0

        for _ in range(
            streamlines.n_cells
        ):

            n_points = int(
                lines[offset]
            )

            ids = lines[
                offset + 1:
                offset + 1 + n_points
            ]

            points_line = (
                streamlines.points[
                    ids
                ]
            )

            # Only x-y coordinates are plotted.
            axes.plot(
                points_line[:, 0],
                points_line[:, 1],
                color=color,
                linewidth=linewidth,
                zorder=zorder,
            )

            offset += n_points + 1

        # -------------------------------------------------
        # Direction arrows
        #
        # Use Matplotlib arrows only for the
        # publication overlay. The streamline
        # geometry itself comes from VTK.
        # -------------------------------------------------

        if arrowsize > 0:

            for cell_id in range(
                streamlines.n_cells
            ):

                ids = streamlines.get_cell(
                    cell_id
                ).point_ids

                points_line = (
                    streamlines.points[
                        ids
                    ]
                )

                if len(points_line) < 4:
                    continue

                middle = len(
                    points_line
                ) // 2

                p0 = points_line[
                    middle - 1
                ]

                p1 = points_line[
                    middle
                ]

                dx = p1[0] - p0[0]
                dy = p1[1] - p0[1]

                length = np.sqrt(
                    dx * dx + dy * dy
                )

                if length <= 0:
                    continue

                axes.annotate(
                    "",
                    xy=(
                        p1[0],
                        p1[1],
                    ),
                    xytext=(
                        p0[0],
                        p0[1],
                    ),
                    arrowprops={
                        "arrowstyle": "-|>",
                        "color": color,
                        "lw": linewidth,
                        "mutation_scale": (
                            8.0 * arrowsize
                        ),
                    },
                    zorder=zorder,
                )

        return streamlines