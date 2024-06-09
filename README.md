# Validiator
A data validation and serializing library for converting JSON to and from Python dataclasses.

Written with no dependencies.

The primary purpose is to validate, serialize, and deserialize Python dataclasses as valid JSON. As such, Python data structures such as sets and tuples, which are not a part of the JSON spec, are not supported. Additionally, math.nan and datetimes will be converted to null and strings, respectively.


### TODO
- [ ] Add datetime support in validation



