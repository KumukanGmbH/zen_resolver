# -*- coding: utf-8 -*-
from ..zen_resolver import ZenResolver

fixture_product_uuids = ['6f4b5c88-cdd9-47ec-bb35-68df6d882396', '1d4146da-fb3b-4421-8f78-a9f51ff17016']

ZenResolver.output_files = {
    'tickets': './test_tickets.json',
    'users': './test_users.json',
}


def test_zen_resolver_output_files():
    s = ZenResolver(product_uuids=fixture_product_uuids)
    assert s.output_files == ZenResolver.output_files