from zen_resolver import ZenResolver

# Note the DEBUG=False this will actull mark as resolved at zendesk
# s = ZenResolver(product_uuids=['6dce72d9-6375-41a6-90fc-f6ffdcd81fb6'],
#                 query_zendesk=True)

s = ZenResolver(query_zendesk=True, ticket_filter={'status': 'open'})
print s.tickets  # get the tuple of those to be affected, (ticket_id, product_uuid, user_info)
#print s.users
