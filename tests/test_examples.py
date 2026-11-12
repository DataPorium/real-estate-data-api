import pandas as pd
import pytest

import examples
from dataporium import DataPorium


@pytest.mark.parametrize("name", list(examples.EXAMPLES))
def test_example_uses_a_real_endpoint_and_parameters(name):
    _question, method, params, _key = examples.EXAMPLES[name]
    endpoint = DataPorium(api_key="test").describe(method)
    known = {p.name for p in endpoint.params}
    assert set(params) <= known, f"{name}: unknown parameters {set(params) - known}"


class FakeClient:
    def __init__(self, *args, **kwargs):
        self.calls = []

    def call(self, method, **params):
        self.calls.append((method, params))
        return {"total": 2, "rows": [{"date": "2026-01-01", "value": 1.0}, {"date": "2026-02-01", "value": 2.0}]}


def test_runs_and_saves_csv(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(examples, "DataPorium", FakeClient)
    name = next(n for n, e in examples.EXAMPLES.items() if e[3] is None)
    out = tmp_path / "out.csv"
    assert examples.main([name, "--csv", str(out)]) == 0
    assert list(pd.read_csv(out)["value"]) == [1.0, 2.0]


def test_lists_examples(capsys):
    assert examples.main([]) == 0
    assert len(capsys.readouterr().out.splitlines()) == len(examples.EXAMPLES)
