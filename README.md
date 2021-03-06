Zendesk PDF Found
=================

Class to allow the marking of zendesk tickets solved when we find the appropriate product pdf


Basic Usage:
------------

in your .bashrc

```
export ZENDESK_URL=https://yoursite.zendesk.com/
export ZENDESK_USERNAME=tomdickorharry@example.com/token
export ZENDESK_TOKEN=u7dDfGDaT2qKAKQYJongDO2qUdKwc1TmnanJwc32
```

in main.py

```
# -*- coding: utf-8 -*-
from zen_resolver import ZenResolver

# Note the DEBUG=False this will actull mark as resolved at zendesk
# Note: Change debug=False if you actually want to update the tickets at zendesk
>>> s = ZenResolver(product_uuids=['6dce72d9-6375-41a6-90fc-f6ffdcd81fb6'], DEBUG=True)

>>> print s.process()  # get the tuple of those to be affected, (ticket_id, product_uuid, user_info)
[(423, '6dce72d9-6375-41a6-90fc-f6ffdcd81fb6', {'name': u'JaneundKarsten', 'email': u'janeundkarsten@gmx.de'}), ...]


>>> s.mark_resolved(matches=s.process())  # Mark the tickets in zendesk as solved
423 6dce72d9-6375-41a6-90fc-f6ffdcd81fb6 {'name': u'JackAndJill', 'email': u'jackandjill@ranupthehill.net'}
```

Logging:
--------

logs to zen-resolver.log


Report for Jane
---------------

```
python update_json_files.py  # get the latest json data from zendesk
python report.py  # build the report.csv
```

Testing
-------

Run

```
py.test tests/
```