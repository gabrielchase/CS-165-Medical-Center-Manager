from django.test import TestCase

from users.models import (
    BaseUser, AdministratorDetails, INSTITUTION_CHOICES
)

import json
from pprint import pprint


class AdministratorUserTestCase(TestCase):
    

    def setUp(self):
        """ 
        Hash the passwords of each saved administrator
        """

        with open('medcentermanager/fixtures/administrators.json') as data_file:
            data = json.load(data_file)

        for datum in data:
            username = datum.get('fields', {}).get('username')
            email = datum.get('fields', {}).get('email')
            mobile_number = datum.get('fields', {}).get('mobile_number')
            landline_number = datum.get('fields', {}).get('landline_number')
            password = datum.get('fields', {}).get('password')
            open_time = datum.get('fields', {}).get('open_time')
            close_time = datum.get('fields', {}).get('close_time')
            location = datum.get('fields', {}).get('location')
            category = datum.get('fields', {}).get('category')
            staff = datum.get('fields', {}).get('staff')
            additional_info = datum.get('fields', {}).get('additional_info')

            AdministratorDetails.objects.create_administrator(
                username=username,
                email=email,
                mobile_number=mobile_number,
                landline_number=landline_number,
                open_time=open_time,
                close_time=close_time,
                location=location,
                category=category,
                staff=staff,
                additional_info=additional_info,
                password=password
            )

        self.administrators = AdministratorDetails.objects.all()

    def test_administrators_loaded(self):
        for idx, administrator in enumerate(self.administrators):
            assert isinstance(administrator, AdministratorDetails)
            assert isinstance(administrator.user, BaseUser)
            assert administrator.user_id ==  administrator.user.user_id
            assert 'administrator_{}@email.com'.format(idx+1) == administrator.user.email
            assert administrator.user.username
            assert administrator.user.mobile_number
            assert administrator.user.landline_number
            assert administrator.open_time
            assert administrator.close_time
            assert administrator.location
            assert administrator.category
            assert administrator.staff
            assert administrator.additional_info

            """ Check password is hashed but the real password works """
            assert administrator.user.password != 'password'
            assert administrator.user.check_password('password')
        
        assert len(self.administrators) == 3

    def test_administrator_details_create_administrator_works(self):
        CATEGORIES = INSTITUTION_CHOICES + ['random_scrandom']

        new_administrator_data = {
            'username': 'institution69',
            'email': 'new_administrator@email.com',
            'mobile_number': '0917-858-2342',
            'landline_number': '321-5832',
            'open_time': '07:00',
            'close_time': '19:00',
            'location': 'Quezon City',
            'staff': 'test_staff',
            'additional_info': 'test_additional_info',
            'password': 'password'
        }

        for idx, category in enumerate(CATEGORIES):
            """ 
            Create a 'new_administrator' for each category. 
            Should fail if the category is 'random_scrandom' which is not a 
            valid institution choice.
            """
            
            try:
                new_administrator = AdministratorDetails.objects.create_administrator(
                    username=new_administrator_data.get('username'),
                    email=new_administrator_data.get('email'),
                    mobile_number=new_administrator_data.get('mobile_number'),
                    landline_number=new_administrator_data.get('landline_number'),
                    open_time=new_administrator_data.get('open_time'),
                    close_time=new_administrator_data.get('close_time'),
                    location=new_administrator_data.get('location'),
                    category=category,
                    staff=new_administrator_data.get('staff'),
                    additional_info=new_administrator_data.get('additional_info'),
                    password=new_administrator_data.get('password')
                )

                assert isinstance(new_administrator, AdministratorDetails)
                assert isinstance(new_administrator.user, BaseUser)
                assert new_administrator.user.user_id
                assert new_administrator.user.username == new_administrator_data.get('username')
                assert new_administrator.user.email == new_administrator_data.get('email')
                assert new_administrator.user.mobile_number == new_administrator_data.get('mobile_number')
                assert new_administrator.user.landline_number == new_administrator_data.get('landline_number')
                assert new_administrator.open_time == new_administrator_data.get('open_time')
                assert new_administrator.close_time == new_administrator_data.get('close_time')
                assert new_administrator.location == new_administrator_data.get('location')
                assert new_administrator.category == category
                assert new_administrator.staff == new_administrator_data.get('staff')
                assert new_administrator.additional_info == new_administrator_data.get('additional_info')

                """ Check password is hashed but the real password works """
                assert new_administrator.user.password != 'password'
                assert new_administrator.user.check_password('password')

                new_administrator.user.delete()
                AdministratorDetails.objects.count() == 3
            except ValueError:
                assert category == 'random_scrandom'
                assert not new_administrator.admin_id
