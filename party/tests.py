"""
this holds all party app related test
"""

from django.test import TestCase
from django.test.client import Client
from party.views import PartyView
from trytonproteus.tryton_proteus import TrytonProteus


class PartyAppViewTest(TestCase):
    """
    Tests the party app views
    """
    def test_party_main_page(self):
        """
        Test Party App view index
        """
        client = Client()
        response = client.get('/party/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Registered parties",
                                              msg_prefix='/party/ should contained "Registered parties" if available')

    def test_if_parties_are_shown_if_they_exist(self):
        """
        Tests if parties that have been registered are shown on the party home page if any

        """
        client = Client()
        response = client.get('/party/')
        self.assertEqual(response.status_code, 200, "/party/ should be accessible")
        result1 = len(response.context['party_list']) > 0
        result2 = "remove party" in response.content
        self.assertEqual(result1, result2, 'if party_list is not empty or None in context then "remove party" should '
                                           'be in response body')

    def test_remove_party_if_party_id_does_not_exist(self):
        """
            Tests /party/remove/party-id when party-id doesn't exist
        """
        client = Client()
        party_home_response = client.get('/party/')
        remove_party_response = client.get('/party/remove/2000010003000/')#unavailable_party_id = 2000010003000

        self.assertEqual(remove_party_response.status_code, 200, "/party/remove/party-id/ should be accessible")
        self.assertEqual(party_home_response.status_code, 200, "/party/ should be accessible")
        self.assertEqual(remove_party_response.content, party_home_response.content, "both party_home_response and "
                                                                                     "response should be equal")
        self.assertEqual(party_home_response.context['party_list'], remove_party_response.context['party_list'],
                         'since deleting unavailable party will not remove any party, party_list before and after that '
                         'should be equal')

    def test_delete_a_party_if_available(self):
        """
            Tests /party/remove/party_id when there is party_id
        """
        tryton_proteus = TrytonProteus()
        Party = tryton_proteus.get_model('party.party')
        party_to_be_deleted = Party(name='testtesttest', code='to_be_deleted1')
        party_to_be_deleted.save()
        self.assertTrue(party_to_be_deleted.id > 0, 'if party_to_be_deleted was saved successfully, party_id should be > 0')

        client = Client()
        party_home_response = client.get('/party/')
        self.assertContains(party_home_response, party_to_be_deleted.name, msg_prefix="party_to_be_deleted.name should be in"
                                                                           "/party/ response content.")
        remove_party_response = client.get('/party/remove/'+str(party_to_be_deleted.id)+'/')
        self.assertNotContains(remove_party_response, party_to_be_deleted.name, msg_prefix="party_to_be_deleted.name should NOT be in"
                                                                           "/party/ response content.")

    def test_show_party_detail_if_party_is_available(self):
        """
        Test show party when party id is available
        """
        tryton_proteus = TrytonProteus()
        Party = tryton_proteus.get_model('party.party')
        party_to_be_shown = Party(name='testtesttest', code='to_party to be shown')
        party_to_be_shown.save()

        self.assertTrue(party_to_be_shown.id > 0, "party_to_be_shown id should be greater than zero after saving")

        client = Client()
        show_party_response = client.get('/party/'+str(party_to_be_shown.id)+"/")

        self.assertEqual(show_party_response.status_code, 200, "show party detail url should be accessible")
        self.assertContains(show_party_response, party_to_be_shown.name, msg_prefix="/party/party_to_be_shown.id"
                            " response content should contain party to be shown id")
        self.assertIsNotNone(show_party_response.context['party'], "party should not be none")

        client.get('/party/remove/'+str(party_to_be_shown.id)+'/')  #delete this party so we can reuse party name,
        # party code in next run of this test

    def test_show_party_detail_if_party_does_not_exist(self):
        client = Client()
        show_party_response = client.get('/party/110002020202020202020202202202/')
        #unavailable party_id =110002020202020202020202202202
        self.assertContains(show_party_response, "Party not found", msg_prefix="party does not exist, hence "
                            " show party response should contain 'Party not found'")
        self.assertNotContains(show_party_response, "Contact info", msg_prefix="party does not exist so response "
                            "content should not contain 'Contact info' " )

    def test_show_party_detail_with_non_numeric_party_id(self):
        client = Client()
        show_party_response = client.get('/party/A1b1#0020/')
        self.assertEqual(show_party_response.status_code, 404, "party/party-id should not be available when called "
                                                               " with non-numeric character.")

    def test_remove_party_with_non_numeric_party_id(self):
        client = Client()
        remove_party_response = client.get('/party/remove/A1b1#0020/')
        self.assertEqual(remove_party_response.status_code, 404, "party/remove/party-id/ should not be called with "
                                                                 " non numeric party_id")

    def test_add_party(self):
        pass
        #TODO: implement this