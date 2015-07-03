# -*- coding: utf-8 -*-
from zdesk import Zendesk
import requests
import os
import re
import csv
import json

pattern = re.compile(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}')

users = json.load(open('users.json'))
tickets = json.load(open('tickets.json'))

zendesk = {
    'zendesk_url': os.getenv('ZENDESK_URL'),
    'username': os.getenv('ZENDESK_USERNAME'),
    'token': os.getenv('ZENDESK_TOKEN')
}

client = Zendesk(zendesk.get('zendesk_url'), zendesk.get('username'), zendesk.get('token'))

def get_product_uuids(tickets):
    for t in tickets:
        match = set(pattern.findall(t['description']))
        if match:
            yield match.pop()

product_uuids = get_product_uuids(tickets.get('tickets'))

products = {}


def get_user(user_id):
    for u in users.get('users'):
        if user_id == u.get('id'):
            return u

    user = client.user_show(id=user_id)
    if user:
        return user

    user = client.end_user_show(id=user_id)
    if user:
        import pdb;pdb.set_trace()
        return user

    return None


def get_product(product_uuid):
    if product_uuid in products.keys():
        return products[product_uuid]

    else:
        resp = requests.get('https://api.manualone.com/v1/products/%s/full.json' % product_uuid)
        if resp.status_code in [200]:
            data = resp.json()
            products[data.get('uuid')] = data
            return data
    return None


f = csv.writer(open("report.csv", "wb+"))

# Write CSV Header
f.writerow(['Zendesk Ticket Nr', 'Anfrage eingegangen am', 'Ticket status', 'Ticket Recipient', 'User Name', 'User E-Mail', 'Brand', 'Product Name', 'Product UUID'])

for ticket in tickets.get('tickets'):
    product_uuid = get_product_uuids([ticket])
    for uuid in product_uuid:
        product = get_product(uuid)
        if product:
            user = get_user(ticket['requester_id'])

            f.writerow([ticket['id'],
                        ticket['created_at'],
                        ticket['status'],
                        ticket['recipient'],
                        user.get('name', user.get('url', 'None')).encode('utf-8'),
                        user.get('email', user.get('name', user.get('url', 'None'))).encode('utf-8'),
                        product["brand"]["name"].encode('utf-8'),
                        product["name"].encode('utf-8'),
                        product["uuid"]])

