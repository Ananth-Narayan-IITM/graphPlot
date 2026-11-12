from __future__ import annotations

from graphplot.cli import main


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
