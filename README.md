# Installation and Verification

## Requirements

`graphPlot` requires:

- Python 3.8 or newer
- `pip`
- A working C/C++/system environment is not required for the Python package itself.
- Doxygen and LaTeX are only required if you want to build the developer documentation.

The Python runtime dependencies are installed automatically from `pyproject.toml`.

---

## 1. Clone or copy the repository

Obtain the `graphPlot` repository and enter its root directory:

```bash
cd graphPlot
```

The repository root should contain at least:

```text
graphPlot/
├── pyproject.toml
├── README.md
├── src/
├── tests/
├── examples/
└── data/
```

---

## 2. Recommended installation

Install `graphPlot` together with its development dependencies:

```bash
python3 -m pip install --upgrade pip
python3 -m pip install -e ".[dev]"
```

The `-e` option installs the package in editable mode. Changes made under `src/` are therefore immediately available without reinstalling the package.

The `[dev]` extra installs development tools such as:

- `pytest`
- `ruff`

Runtime dependencies such as NumPy, Matplotlib, PyVista, and PyYAML are installed automatically from `pyproject.toml`.

---

## 3. Verify the installation

Check that the package can be imported:

```bash
python3 -c "import postprocess; print('graphPlot import: OK')"
```

Check the installed development tools:

```bash
python3 -m pytest --version
ruff --version
```

---

## 4. Run the complete test suite

Run:

```bash
python3 -m pytest -v
```

A successful installation should finish with all tests passing and no collection errors.

You can also check test collection independently:

```bash
python3 -m pytest --collect-only -q
```

---

## 5. Run an example

The examples progressively demonstrate the capabilities of `graphPlot`.

For example:

```bash
python3 examples/19_final_publication_figure.py
```

The generated output is written under:

```text
output/
```

Example 19 is the final integrated publication-figure example.

---

## 6. Verify all examples

To run every example from the repository:

```bash
for f in examples/*.py; do
    echo "========================================"
    echo "Running $f"
    python3 "$f" || exit 1
done
```

If an example requires a special environment or external input, run that example separately.

---

## 7. Build the Doxygen documentation

Doxygen is not a Python dependency and is not installed by `pip`.

If Doxygen is installed:

```bash
doxygen Doxyfile
```

If the Doxygen configuration generates a LaTeX directory:

```bash
cd docs/latex
make
```

The exact documentation output location is determined by `Doxyfile`.