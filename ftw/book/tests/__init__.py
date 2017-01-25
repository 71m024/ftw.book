from ftw.book.testing import BOOK_FUNCTIONAL_TESTING
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from unittest2 import TestCase
import transaction


class FunctionalTestCase(TestCase):
    layer = BOOK_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.example_book = self.portal.restrictedTraverse(
            self.layer['example_book_path'])

    def grant(self, *roles):
        setRoles(self.portal, TEST_USER_ID, list(roles))
        transaction.commit()
