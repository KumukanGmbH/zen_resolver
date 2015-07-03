# -*- coding: utf-8 -*-
from zdesk import Zendesk

import os
import json
import logging

logging.basicConfig()
logger = logging.getLogger('zen-resolver')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('zen-resolver.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)


class ZenResolver(object):
    """
    Class to query zendesk for tickets to update where we match a set of
    product uuids

    @TODO need to not jsut check subject and description but also ensure that
    the ticket is a valid "missing pdf" ticket

    @TODO need to ensure the email from teh request PDF includes the reply-to
    that is the users email address otherwise the zendesk auto reply wont work

    @USAGE:
    >>> s = ZenResolver(product_uuids=['6dce72d9-6375-41a6-90fc-f6ffdcd81fb6'])

    # get the tuple of those to be affected, (ticket_id, product_uuid, user_info)
    >>> print s.process()
    [(423, '6dce72d9-6375-41a6-90fc-f6ffdcd81fb6', {'name': u'JaneundKarsten', 'email': u'janeundkarsten@gmx.de'}), ...]

    # Mark the tickets in zendesk as solved
    >>> s.mark_resolved(matches=s.process())
    423 6dce72d9-6375-41a6-90fc-f6ffdcd81fb6 {'name': u'JaneundKarsten', 'email': u'janeundkarsten@gmx.de'}
    """
    output_files = {
        'tickets': 'tickets.json',
        'users': 'users.json',
    }

    def __init__(self, **kwargs):
        self.DEBUG = kwargs.get('DEBUG', True)
        self.query_zendesk = kwargs.get('query_zendesk', False)

        self.target_product_uuids = kwargs.get('product_uuids', [])
        self.matched_tickets = []
        self.matched_products = []
        self.matched_requesters = []
        self.matched_users = []

        zendesk = {
            'zendesk_url': kwargs.get('zendesk_url', os.getenv('ZENDESK_URL')),
            'username': kwargs.get('username', os.getenv('ZENDESK_USERNAME')),
            'token': kwargs.get('token', os.getenv('ZENDESK_TOKEN'))
        }

        self.client = Zendesk(zendesk.get('zendesk_url'),
                              zendesk.get('username'),
                              zendesk.get('token'))
        logger.info('Initialized with kwargs: %s zendesk: %s' % (kwargs, zendesk))

    @property
    def tickets(self):
        filename = self.output_files.get('tickets')
        logger.debug('Reading tickets: %s' % filename)
        if os.path.exists(filename) is True and self.query_zendesk is False:
            resp = json.load(open(filename, 'r'))
        else:
            resp = self.client.tickets_list(get_all_pages=True)
            with open(filename, 'w+') as fname:
                fname.write(json.dumps(resp))

        return resp.get('tickets', [])

    @property
    def users(self):
        filename = self.output_files.get('users')
        logger.debug('Reading users: %s' % filename)
        if os.path.exists(filename) is True and self.query_zendesk is False:
            resp = json.load(open(filename, 'r'))
        else:
            resp = self.client.users_list(get_all_pages=True)
            with open(filename, 'w+') as fname:
                fname.write(json.dumps(resp))

        return resp.get('users', [])

    def __match_tickets(self):
        """
        Build a set of ticket_id requester_id and product_uuid to act apon
        may need to ensure that the tickets.json is up to date,
        by forcing query_zendesk=True
        """
        for ticket in self.tickets:
            subject = ticket.get('subject')
            description = ticket.get('description')

            logger.debug('Trying to match for TicketId: %s and RequesterId: %s' % (ticket['id'], ticket.get('requester_id')))
            matched_product_uuid = [target for target in self.target_product_uuids if target in subject or target in description]

            if matched_product_uuid:
                rid = ticket.get('requester_id')
                if rid:  # because sometimes there is no requestor
                    logger.debug('Match found for TicketId: %s and RequesterId: %s' % (ticket['id'], ticket.get('requester_id')))
                    self.matched_tickets += [ticket['id']]
                    self.matched_requesters += [ticket['requester_id']]
                    self.matched_products += matched_product_uuid
                else:
                    logger.debug('RequesterId: %s was invalid' % ticket.get('requester_id'))

    def __match_users(self):
        """
        Find the matching user details from each request
        may need to ensure that the users.json is up to date,
        by forcing query_zendesk=True
        """
        for user in self.users:
            user_id = user.get('id')
            indices = [i for i, x in enumerate(self.matched_requesters) if x == user_id]
            if indices:
                for i in indices:
                    self.matched_requesters[i] = {'name':user['name'], 'email': user['email']}

    def mark_resolved(self, matches):
        """
        Update the zendesk ticket_ids mark as solved and trigger the auto
        responses
        """
        update_ticket_ids = []
        for ticket_id, product_uuid, user_info in matches:
            update_ticket_ids += [ticket_id]

        update_ticket_data = {'ticket': {'status': 'solved'}}

        logger.info('Will be marking these tickets as resolved: %s' % update_ticket_ids)

        if update_ticket_ids and self.DEBUG is False:
            self.client.tickets_update_many(ids=update_ticket_ids,
                                            data=update_ticket_data)

    def process(self):
        """
        Primary process call
        returns a tuple of tuples: (ticket_id, product_uuid, user_info)
        [(423, '6dce72d9-6375-41a6-90fc-f6ffdcd81fb6', {'name': u'JaneundKarsten', 'email': u'janeundkarsten@gmx.de'}), ...]
        """
        self.__match_tickets()
        self.__match_users()

        return zip(self.matched_tickets,
                   self.matched_products,
                   self.matched_requesters)
