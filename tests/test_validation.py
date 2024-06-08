from dataclasses import dataclass
from typing import Dict, List, Optional
import pytest
from validiator.validation import validate


@dataclass
class SamplePerson:
    name: str
    age: int
    married: bool
    income: float
    emails: List[str]
    relationships: Dict[str, str]
    favorite_quote: Optional[str]


@dataclass
class SampleGroup:
    people: List[SamplePerson]


@pytest.mark.parametrize(
    ["data", "datatype", "should_fail"],
    [
        pytest.param("hi", str, False, id="good_str"),
        pytest.param(1, str, True, id="bad_str"),
        pytest.param(1, int, False, id="good_int"),
        pytest.param(1.1, int, True, id="bad_int"),
        pytest.param(1.1, float, False, id="good_float"),
        pytest.param(True, float, True, id="bad_float"),
        pytest.param(True, bool, False, id="good_bool"),
        pytest.param("hi", bool, True, id="bad_bool"),
        pytest.param([1], int, True, id="sequence_vs_primitive"),
        pytest.param({"a": 1}, str, True, id="mapping_vs_primitive"),
    ],
)
def test_validate_primitives(data, datatype, should_fail: bool):
    mesg: str | None = validate(data, datatype)
    if should_fail:
        assert mesg is not None, mesg
    else:
        assert mesg is None, mesg


@pytest.mark.parametrize(
    ["data", "datatype", "should_fail"],
    [
        pytest.param(["hi"], List[str], False, id="good_list_of_strs"),
        pytest.param([1], List[int], False, id="good_list_of_ints"),
        pytest.param([[1], [2]], List[List[int]], False,
                     id="good_list_of_list_of_ints"),
        pytest.param(1.1, List[float], True, id="primitive_vs_sequence"),
        pytest.param({"str": 1}, List[str], True, id="mapping_vs_sequence"),
    ],
)
def test_validate_lists(data, datatype, should_fail: bool):
    mesg: str | None = validate(data, datatype)
    if should_fail:
        assert mesg is not None, mesg
    else:
        assert mesg is None, mesg
