from __future__ import annotations

from graphplot.cli import main


def test_version_command(capsys):
    assert main(["--version"]) == 0
    assert "graphPlot 2.0.0" in capsys.readouterr().out


def test_run_python_script(tmp_path):
    script = tmp_path / "figure.py"
    marker = tmp_path / "marker.txt"
    script.write_text(
        "from pathlib import Path\n"
        f"Path({str(marker)!r}).write_text('ok', encoding='utf-8')\n",
        encoding="utf-8",
    )
    assert main([str(script)]) == 0
    assert marker.read_text(encoding="utf-8") == "ok"


def test_missing_script(tmp_path, capsys):
    assert main([str(tmp_path / "missing.py")]) == 2
    assert "not found" in capsys.readouterr().err


def test_check_command(capsys):
    assert main(["check"]) == 0
    output = capsys.readouterr().out
    assert "graphPlot environment check" in output
    assert "Python" in output


def test_info_command(capsys):
    assert main(["info", "data/zNormal.vtp"]) == 0
    output = capsys.readouterr().out
    assert "FieldData" in output
    assert "gammaDV" in output
