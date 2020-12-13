# bayard-python

[bayard](https://github.com/bayard-search/bayard) client for Python.


## Installation

```
$ pip install bayard-python
```

## Usage

```python
from bayard import BayardHTTPClient

client = BayardHTTPClient(port=8088)
schema = client.schema()

your_schema_data = {}
client.set_document("id1", your_schema_data)
client.commit()

client.get_document("id1")
```

## for developer

```
$ pip install poetry
$ poetry build
$ pytest
```

## LICENSE

MIT
