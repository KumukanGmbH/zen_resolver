# -*- coding: utf-8 -*-
import os

from ..zen_resolver import ZenResolver

fixture_product_uuids = ['6f4b5c88-cdd9-47ec-bb35-68df6d882396', '1d4146da-fb3b-4421-8f78-a9f51ff17016']

ZenResolver.output_files = {
    'tickets': os.path.abspath('./tests/test_tickets.json'),
    'users': os.path.abspath('./tests/test_users.json'),
}

kwargs = {
    'product_uuids': fixture_product_uuids,
    'zendesk_url': 'https://manualone.zendesk.com/',
    'username': 'monkey@manualone.com',
    'token': '123456789'
}

def test_zen_resolver_output_files():
    s = ZenResolver(**kwargs)
    assert s.output_files == ZenResolver.output_files


def test_zen_resolver_process(capsys):
    s = ZenResolver(**kwargs)
    output = s.process()
    assert output == [(1,
                       '6f4b5c88-cdd9-47ec-bb35-68df6d882396',
                       {'email': u'monkey@helpme.com', 'name': u'Zendesk'}),
                      (2,
                       '1d4146da-fb3b-4421-8f78-a9f51ff17016',
                       {'email': u'monkey@helpme.com', 'name': u'Zendesk'})]
