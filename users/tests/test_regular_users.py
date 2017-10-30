from django.test import TestCase

from users.models import RegularUser


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

