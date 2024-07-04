from dataclasses import dataclass
from typing import Dict, List, Optional
import pytest
from validiator.validate import validate


@dataclass
class SamplePerson:
    name: str
    age: int
    married: bool
    income: float
    emails: List[str]
    relationships: Dict[str, str]
    favorite_quote: Optional[str] = None


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
        pytest.param(
            SamplePerson("name", 1, False, 10.5, [], {}, None),
            str,
            True,
            id="dataclass_vs_primitive",
        ),
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
        pytest.param(
            [[1], [2]], List[List[int]], False, id="good_list_of_list_of_ints"
        ),
        pytest.param(
            [[1], [2], 1], List[List[int]], True, id="bad_list_of_list_of_ints"
        ),
        pytest.param(1.1, List[float], True, id="primitive_vs_list"),
        pytest.param({"str": 1}, List[str], True, id="mapping_vs_list"),
        pytest.param(
            SamplePerson("name", 1, False, 10.5, [], {}, None),
            List[str],
            True,
            id="dataclass_vs_list",
        ),
    ],
)
def test_validate_lists(data, datatype, should_fail: bool):
    mesg: str | None = validate(data, datatype)
    if should_fail:
        assert mesg is not None, mesg
    else:
        assert mesg is None, mesg


@pytest.mark.parametrize(
    ["data", "datatype", "should_fail"],
    [
        pytest.param({"a": 1}, Dict[str, int], False, id="good_dict_str_int"),
        pytest.param(
            {True: 1.1}, Dict[bool, float], False, id="good_dict_of_bool_float"
        ),
        pytest.param(
            {"a": {"b": 1}},
            Dict[str, Dict[str, int]],
            False,
            id="good_dict_of_str_dict_of_str_int",
        ),
        pytest.param(
            {"a": {"b": 1}, True: {"b": 1}},
            Dict[str, Dict[str, int]],
            True,
            id="bad_dict_of_str_dict_of_str_int",
        ),
        pytest.param(1.1, Dict[str, float], True, id="primitive_vs_dict"),
        pytest.param(["str"], Dict[str, str], True, id="list_vs_dict"),
        pytest.param(
            SamplePerson("name", 1, False, 10.5, [], {}),
            Dict[str, str],
            True,
            id="dataclass_vs_dict",
        ),
    ],
)
def test_validate_dictionaries(data, datatype, should_fail: bool):
    mesg: str | None = validate(data, datatype)
    if should_fail:
        assert mesg is not None, mesg
    else:
        assert mesg is None, mesg


@pytest.mark.parametrize(
    ["data", "datatype", "should_fail"],
    [
        pytest.param(
            {
                "name": "name",
                "age": 1,
                "married": False,
                "income": 10.5,
                "emails": [],
                "relationships": {},
                "favorite_quote": "To be or not to be",
            },
            SamplePerson,
            False,
            id="good_dataclass",
        ),
        pytest.param(
            {
                "name": "name",
                "age": 1,
                "married": False,
                "income": 10.5,
                "emails": [],
                "relationships": {},
            },
            SamplePerson,
            False,
            id="good_dataclass_optional_field",
        ),
        pytest.param(
            {
                "age": 1,
                "married": False,
                "income": 10.5,
                "emails": [],
                "relationships": {},
            },
            SamplePerson,
            True,
            id="bad_dataclass_missing_required_field",
        ),
        pytest.param(
            {
                "name": 5,
                "age": 1,
                "married": False,
                "income": 10.5,
                "emails": [],
                "relationships": {},
            },
            SamplePerson,
            True,
            id="bad_dataclass_incorrect_type",
        ),
        pytest.param(
            {
                "people": [
                    {
                        "name": "name",
                        "age": 1,
                        "married": False,
                        "income": 10.5,
                        "emails": [],
                        "relationships": {},
                    }
                ]
            },
            SampleGroup,
            False,
            id="good_dataclass_composed_dataclass",
        ),
        pytest.param(
            {
                "people": [
                    {
                        "name": 1,
                        "age": 1,
                        "married": False,
                        "income": 10.5,
                        "emails": [],
                        "relationships": {},
                    }
                ]
            },
            SampleGroup,
            True,
            id="bad_dataclass_bad_composed_dataclass",
        ),
        pytest.param(
            {
                "legal_name": 5,
                "age": 1,
                "married": False,
                "income": 10.5,
                "emails": [],
                "relationships": {},
            },
            SamplePerson,
            True,
            id="bad_dataclass_incorrect_field",
        ),
        pytest.param(
            {
                "name": "name",
                "age": 1,
                "married": False,
                "income": 10.5,
                "emails": [],
                "relationships": {},
                "favorite_drink": "coffee",
            },
            SamplePerson,
            True,
            id="bad_dataclass_extra_field",
        ),
        pytest.param(
            ["name", "age"],
            SamplePerson,
            True,
            id="list_vs_dataclass",
        ),
    ],
)
def test_validate_dataclasses(data, datatype, should_fail: bool):
    mesg: str | None = validate(data, datatype)
    if should_fail:
        print(mesg)
        assert mesg is not None, mesg
    else:
        assert mesg is None, mesg
