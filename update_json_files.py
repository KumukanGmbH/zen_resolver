from zen_resolver import ZenResolver

# Note the DEBUG=False this will actull mark as resolved at zendesk
s = ZenResolver(product_uuids=['6dce72d9-6375-41a6-90fc-f6ffdcd81fb6'], query_zendesk=True)

print s.process()  # get the tuple of those to be affected, (ticket_id, product_uuid, user_info)