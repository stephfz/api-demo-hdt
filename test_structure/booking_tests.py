import unittest
import json

from booking_service import BookingService
from authorization_service import AuthorizationService

from data_services import DataProvider

from config import *

class BookingTests(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.booking_service = BookingService(BASE_URL, 'booking')
        self.data_services = DataProvider()

    def test_get_existing_booking(self):
        r = self.booking_service.get_booking(1)
        self.assertTrue(r.status_code == 200)

    def test_get_non_existing_booking(self):
        r = self.booking_service.get_booking(34541)
        self.assertTrue(r.status_code == 404)

    def test_create_new_booking_sucessful(self):
        booking_data = self.data_services.new_booking_data()
        r = self.booking_service.new_booking(booking_data)
        self.assertTrue(r.status_code == 200)

    def test_update_booking(self):
        booking_data = self.data_services.new_booking_data()
        r = self.booking_service.new_booking(booking_data)
        self.assertTrue(r.status_code == 200)
        bookingid = r.json()["bookingid"]
        print bookingid
        # get authorization
        auth_service = AuthorizationService(BASE_URL, 'auth')
        authorization = auth_service.authorize_user('admin', 'password123')
        token = authorization.json()["token"]
        #update
        new_need = 'Non-Smooking Room'
        booking_data['additionalneeds'] = new_need
        r = self.booking_service.update_booking(booking_data,
                                        bookingid, token = token)
        self.assertTrue(r.status_code == 200)
        self.assertTrue(r.json()['additionalneeds'] == new_need)






if __name__ == "__main__":
    unittest.main()
