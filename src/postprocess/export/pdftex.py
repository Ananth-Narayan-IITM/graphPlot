from pathlib import Path
from typing import Union

import subprocess


class PDFTeXExporter:
    """
    Export an SVG figure to PDF + PDF_TeX using Inkscape.
    """

    def __init__(
        self,
        inkscape="inkscape",
    ):
        self.inkscape = inkscape

    def export(
        self,
        svg_file: Union[str, Path],
        output_file: Union[str, Path],
    ):
        """
        Export SVG to PDF + PDF_TeX.

        Parameters
        ----------
        svg_file
            Input SVG file.

        output_file
            PDF output filename.

        Returns
        -------
        tuple
            PDF filename and PDF_TeX filename.
        """

        svg_file = Path(svg_file)
        output_file = Path(output_file)

        # -------------------------------------------------
        # Validate input
        # -------------------------------------------------

        if not svg_file.exists():

            raise FileNotFoundError(
                f"SVG file not found: {svg_file}"
            )

        # -------------------------------------------------
        # Create output directory
        # -------------------------------------------------

        output_file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        # -------------------------------------------------
        # Inkscape command
        # -------------------------------------------------

        command = [
            self.inkscape,
            str(svg_file),
            "--export-filename",
            str(output_file),
            "--export-latex",
        ]

        print(
            "Running:",
            " ".join(command),
        )

        # -------------------------------------------------
        # Run Inkscape
        # -------------------------------------------------

        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )

        # -------------------------------------------------
        # Check Inkscape
        # -------------------------------------------------

        if result.returncode != 0:

            raise RuntimeError(
                "Inkscape PDF+LaTeX export failed.\n\n"
                f"Command:\n"
                f"{' '.join(command)}\n\n"
                f"stdout:\n"
                f"{result.stdout}\n\n"
                f"stderr:\n"
                f"{result.stderr}"
            )

        # -------------------------------------------------
        # Expected PDF_TeX file
        # -------------------------------------------------

        pdf_tex_file = Path(
            str(output_file) + "_tex"
        )

        # -------------------------------------------------
        # Validate output
        # -------------------------------------------------

        if not output_file.exists():

            raise RuntimeError(
                "Inkscape completed but PDF "
                "file was not created:\n"
                f"{output_file}"
            )

        if not pdf_tex_file.exists():

            raise RuntimeError(
                "Inkscape completed but PDF_TeX "
                "file was not created:\n"
                f"{pdf_tex_file}"
            )

        return (
            output_file,
            pdf_tex_file,
        )