class LaTeXTextRegistry:
    """
    Stores LaTeX strings associated with temporary
    placeholders used during PDF+TeX export.
    """

    def __init__(self):

        self._labels = {}
        self._counter = 0

    def register(self, text):
        """
        Register a LaTeX string and return a unique
        plain-text placeholder.
        """

        if text is None:
            return None

        self._counter += 1

        placeholder = (
            "GRAPHPlotLabel{:04d}".format(
                self._counter
            )
        )

        self._labels[placeholder] = text

        return placeholder

    def replace_in_file(self, filename):
        """
        Replace all registered placeholders in a
        PDF_TeX file with their original LaTeX text.
        """

        with open(
            filename,
            "r",
            encoding="utf-8",
        ) as file:

            content = file.read()

        for placeholder, latex_text in (
            self._labels.items()
        ):

            content = content.replace(
                placeholder,
                latex_text,
            )

        with open(
            filename,
            "w",
            encoding="utf-8",
        ) as file:

            file.write(content)

    @property
    def labels(self):
        """
        Return the registered labels.
        """

        return dict(
            self._labels
        )