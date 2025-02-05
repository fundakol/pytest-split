from collections import namedtuple

import pytest
from pytest_split.algorithms import Algorithms
from pytest_split.ipynb_compatibility import ensure_ipynb_compatibility

item = namedtuple("item", "nodeid")


class TestIPyNb:
    @pytest.mark.parametrize("algo_name", ["duration_based_chunks"])
    def test_ensure_ipynb_compatibility(self, algo_name):
        durations = {
            "temp/nbs/test_1.ipynb::Cell 0": 1,
            "temp/nbs/test_1.ipynb::Cell 1": 1,
            "temp/nbs/test_1.ipynb::Cell 2": 1,
            "temp/nbs/test_2.ipynb::Cell 0": 3,
            "temp/nbs/test_2.ipynb::Cell 1": 5,
            "temp/nbs/test_2.ipynb::Cell 2": 1,
            "temp/nbs/test_2.ipynb::Cell 3": 4,
            "temp/nbs/test_3.ipynb::Cell 0": 5,
            "temp/nbs/test_3.ipynb::Cell 1": 1,
            "temp/nbs/test_3.ipynb::Cell 2": 1,
            "temp/nbs/test_3.ipynb::Cell 3": 2,
            "temp/nbs/test_3.ipynb::Cell 4": 1,
            "temp/nbs/test_4.ipynb::Cell 0": 1,
            "temp/nbs/test_4.ipynb::Cell 1": 1,
            "temp/nbs/test_4.ipynb::Cell 2": 3,
        }
        items = [item(x) for x in durations]
        algo = Algorithms[algo_name].value
        groups = algo(splits=3, items=items, durations=durations)

        assert groups[0].selected == [
            item(nodeid="temp/nbs/test_1.ipynb::Cell 0"),
            item(nodeid="temp/nbs/test_1.ipynb::Cell 1"),
            item(nodeid="temp/nbs/test_1.ipynb::Cell 2"),
            item(nodeid="temp/nbs/test_2.ipynb::Cell 0"),
            item(nodeid="temp/nbs/test_2.ipynb::Cell 1"),
        ]
        assert groups[1].selected == [
            item(nodeid="temp/nbs/test_2.ipynb::Cell 2"),
            item(nodeid="temp/nbs/test_2.ipynb::Cell 3"),
            item(nodeid="temp/nbs/test_3.ipynb::Cell 0"),
            item(nodeid="temp/nbs/test_3.ipynb::Cell 1"),
        ]
        assert groups[2].selected == [
            item(nodeid="temp/nbs/test_3.ipynb::Cell 2"),
            item(nodeid="temp/nbs/test_3.ipynb::Cell 3"),
            item(nodeid="temp/nbs/test_3.ipynb::Cell 4"),
            item(nodeid="temp/nbs/test_4.ipynb::Cell 0"),
            item(nodeid="temp/nbs/test_4.ipynb::Cell 1"),
            item(nodeid="temp/nbs/test_4.ipynb::Cell 2"),
        ]

        ensure_ipynb_compatibility(groups[0], items)
        assert groups[0].selected == [
            item(nodeid="temp/nbs/test_1.ipynb::Cell 0"),
            item(nodeid="temp/nbs/test_1.ipynb::Cell 1"),
            item(nodeid="temp/nbs/test_1.ipynb::Cell 2"),
            item(nodeid="temp/nbs/test_2.ipynb::Cell 0"),
            item(nodeid="temp/nbs/test_2.ipynb::Cell 1"),
            item(nodeid="temp/nbs/test_2.ipynb::Cell 2"),
            item(nodeid="temp/nbs/test_2.ipynb::Cell 3"),
        ]

        ensure_ipynb_compatibility(groups[1], items)
        assert groups[1].selected == [
            item(nodeid="temp/nbs/test_3.ipynb::Cell 0"),
            item(nodeid="temp/nbs/test_3.ipynb::Cell 1"),
            item(nodeid="temp/nbs/test_3.ipynb::Cell 2"),
            item(nodeid="temp/nbs/test_3.ipynb::Cell 3"),
            item(nodeid="temp/nbs/test_3.ipynb::Cell 4"),
        ]

        ensure_ipynb_compatibility(groups[2], items)
        assert groups[2].selected == [
            item(nodeid="temp/nbs/test_4.ipynb::Cell 0"),
            item(nodeid="temp/nbs/test_4.ipynb::Cell 1"),
            item(nodeid="temp/nbs/test_4.ipynb::Cell 2"),
        ]
