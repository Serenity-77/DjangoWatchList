from django.test import TestCase, Client
from django.contrib.auth.models import User as DjangoUserModel


class TestUserRegister(TestCase):

    def setUp(self):
        self.client = Client()

    def _do_test_validation(self, parameters, expected_messages, expected_status=422):
        response = self.client.post("/register/", parameters)

        self.assertEquals(expected_status, response.status_code)
        self.assertEquals(expected_messages, response.content.decode())
        self.assertEquals("text/plain", response.headers['Content-Type'])


    def test_register_firstname_required(self):
        self._do_test_validation({
            'lastname': "Harianja",
            'username': "harianja",
            'password': "FooBar",
            'repassword': "FooBar"
        }, "First Name: This field is required.")

    def test_register_username_required(self):
        self._do_test_validation({
            'firstname': "Lundu",
            'lastname': "Harianja",
            'password': "FooBar",
            'repassword': "FooBar"
        }, "Username: This field is required.")

    def test_register_password_required(self):
        self._do_test_validation({
            'firstname': "Lundu",
            'lastname': "Harianja",
            'username': "harianja",
            'repassword': "FooBar"
        }, "Password: This field is required.")

    def test_register_password_not_match(self):
        self._do_test_validation({
            'firstname': "Lundu",
            'lastname': "Harianja",
            'username': "harianja",
            'password': "Foo",
            'repassword': "FooBar"
        }, "Retype Password: Password not match.")

    def test_register_multiple_errors(self):
        self._do_test_validation({
            'lastname': "Harianja",
            'username': "harianja",
            'password': "Foo",
            'repassword': "FooBar"
        }, "First Name: This field is required.\nRetype Password: Password not match.")

    def test_user_register(self):
        response = self.client.post("/register/", {
            'firstname': "Lundu",
            'lastname': "Harianja",
            'username': "harianja123",
            'password': "FooBar",
            'repassword': "FooBar"
        })

        self.assertEquals(200, response.status_code)

        user = DjangoUserModel.objects.get(username="harianja123")
        self.assertEquals("harianja123", user.username)
        self.assertTrue(user.is_active)

    def test_user_register_already_taken(self):
        self.client.post("/register/", {
            'firstname': "Lundu",
            'lastname': "Harianja",
            'username': "harianja123",
            'password': "FooBar",
            'repassword': "FooBar"
        })

        response = self.client.post("/register/", {
            'firstname': "Lundu",
            'lastname': "Harianja",
            'username': "harianja123",
            'password': "FooBar",
            'repassword': "FooBar"
        })

        self.assertEquals(409, response.status_code)
        self.assertEquals("Username harianja123 already taken", response.content.decode())
        self.assertEquals("text/plain", response.headers['Content-Type'])
