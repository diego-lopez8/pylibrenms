# PyLibreNMS

A Python library for the LibreNMS API. 

## Installation

Requires Python>=3.8.

```
pip install pylibrenms
```


## Quick Start

Using the API

```python
from pylibrenms import Librenms

librenms_token = "YOUR_API_TOKEN"
nms = Librenms("YOUR_NMS_INSTANCE", librenms_token)
print(nms.get_all_ports())
```

## Documentation

Coming soon!