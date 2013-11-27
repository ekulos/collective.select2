import json
from itertools import chain
from Acquisition import aq_inner

from zope.component import getMultiAdapter
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView


class users_search(BrowserView):

    def results(self, search_term):
        """Search for users and returning member items
        """
        mtool = getToolByName(self.context, 'portal_membership')

        searchView = getMultiAdapter(
            (aq_inner(self.context), self.request),
            name='pas_search')

        results = searchView.merge(
            chain(*[searchView.searchUsers(
                **{field: search_term}) for field in
                ['login', 'fullname', 'email']]), 'userid')

        for u in results:
            usr = mtool.getMemberById(u['id'])
            if not usr:
                continue

            yield {
                "text": usr.getProperty('fullname') or u['id'],
                "id": u['id']
            }

        yield {
            "text": search_term,
            "id": search_term
        }

    def __call__(self):
        results = self.results(self.request.form.get('term'))
        return json.dumps([i for i in results])
