from django.test import TestCase

from users.models import (
    AdministratorUser, INSTITUTION_CHOICES
)


class AdministratorUserTestCase(TestCase):
    fixtures = ['medcentermanager/fixtures/administrators.json']

    def setUp(self):
        """ 
        Hash the passwords of each saved administrator
        """

        self.administrators = AdministratorUser.objects.all()

        for administrator in self.administrators:
            administrator.set_password(administrator.password)
            administrator.save()

        return self.administrators

    def test_administrators_loaded(self):
        for idx, administrator in enumerate(self.administrators):
            assert isinstance(administrator, AdministratorUser)
            assert administrator.admin_id
            assert administrator.institution_name
            assert 'administrator_user_{}@email.com'.format(idx+1) == administrator.email
            assert administrator.mobile_number
            assert administrator.landline_number
            assert administrator.open_time
            assert administrator.close_time
            assert administrator.location
            assert administrator.category
            assert administrator.staff
            assert administrator.additional_info

            """ Check password is hashed but the real password works """
            assert administrator.password != 'password'
            assert administrator.check_password('password')
        
        assert len(self.administrators) == 3

    def test_regular_user_create_user_works(self):
        CATEGORIES = INSTITUTION_CHOICES + ['random_scrandom']

        new_administrator_data = {
            'institution_name': 'new_institution',
            'email': 'new_administrator.com',
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
                new_administrator = AdministratorUser.objects.create_administrator(
                    institution_name=new_administrator_data.get('institution_name'),
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

                new_administrator.set_password(new_administrator_data.get('password'))
                new_administrator.save()

                assert isinstance(new_administrator, AdministratorUser)
                assert new_administrator.admin_id
                assert new_administrator.admin_id == len(self.administrators) + idx + 1
                assert new_administrator.institution_name == new_administrator_data.get('institution_name')
                assert new_administrator.email == new_administrator_data.get('email')
                assert new_administrator.mobile_number == new_administrator_data.get('mobile_number')
                assert new_administrator.landline_number == new_administrator_data.get('landline_number')
                assert new_administrator.open_time == new_administrator_data.get('open_time')
                assert new_administrator.close_time == new_administrator_data.get('close_time')
                assert new_administrator.location == new_administrator_data.get('location')
                assert new_administrator.category == category
                assert new_administrator.staff == new_administrator_data.get('staff')
                assert new_administrator.additional_info == new_administrator_data.get('additional_info')

                """ Check password is hashed but the real password works """
                assert new_administrator.password != 'password'
                assert new_administrator.check_password('password')

                new_administrator.delete()
            except ValueError:
                assert category == 'random_scrandom'
                assert not new_administrator.admin_id
