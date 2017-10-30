from django.test import TestCase

from users.models import (AdministratorUser, RegularUser)


class RegularUserTestCase(TestCase):
    fixtures = ['medcentermanager/fixtures/regular_users.json']

    def setUp(self):
        self.users = RegularUser.objects.all()

        for user in self.users:
            user.set_password(user.password)
            user.save()

        return self.users
    
    def test_regular_users_loaded(self):
        for user in self.users:
            assert user.user_id
            assert 'regular_user_' in user.email
            assert '@email.com' in user.email
            assert user.mobile_number
            assert user.landline_number
            assert user.password != 'password'
        
        assert len(self.users) == 3

    def test_regular_user_create_user_works(self):
        new_user_data = {
            'username': 'new_user',
            'email': 'new_user_email.com',
            'mobile_number': '0917-858-2342',
            'landline_number': '321-5832',
            'password': 'password'
        }
        
        new_user = RegularUser.objects.create_user(
            username=new_user_data.get('username'),
            email=new_user_data.get('email'),
            mobile_number=new_user_data.get('mobile_number'),
            landline_number=new_user_data.get('landline_number'),
            password=new_user_data.get('password')
        )

        assert isinstance(new_user, RegularUser)
        assert new_user.user_id
        assert new_user.user_id == len(self.users)+1
        assert new_user.username == new_user_data.get('username')
        assert new_user.email == new_user_data.get('email')
        assert new_user.mobile_number == new_user_data.get('mobile_number')
        assert new_user.landline_number == new_user_data.get('landline_number')
        assert new_user.password != new_user_data.get('password')
        assert new_user.check_password(new_user_data.get('password'))


class AdministratorUserTestCase(TestCase):
    fixtures = ['medcentermanager/fixtures/administrators.json']

    def setUp(self):
        self.administrators = AdministratorUser.objects.all()

        for administrator in self.administrators:
            administrator.set_password(administrator.password)
            administrator.save()

        return self.administrators

    def test_administrators_loaded(self):
        for administrator in self.administrators:
            assert administrator.admin_id
            assert administrator.institution_name
            assert 'administrator_user_' in administrator.email
            assert '@email.com' in administrator.email
            assert administrator.mobile_number
            assert administrator.landline_number
            assert administrator.open_time
            assert administrator.close_time
            assert administrator.location
            assert administrator.category
            assert administrator.staff
            assert administrator.additional_info
            assert administrator.password != 'password'
            assert administrator.check_password('password')
        
        assert len(self.administrators) == 3

    def test_regular_user_create_user_works(self):
        CATEGORIES = ['treatment_center', 'social_hygiene_clinic', 'testing_hub', 'random_scrandom']

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
                assert new_administrator.password != 'password'
                assert new_administrator.check_password('password')

                new_administrator.delete()
            except ValueError:
                assert category == 'random_scrandom'
                assert not new_administrator.admin_id
