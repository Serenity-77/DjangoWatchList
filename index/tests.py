from django.test import TestCase, Client
from django.contrib.auth.models import User as DjangoUserModel
from django.contrib.auth import SESSION_KEY

# Create your tests here.


class TestLogin(TestCase):

    def setUp(self):
        self.client = Client()

    def _do_test_validation(self, parameters, expected_messages, expected_status=422):
        response = self.client.post("/", parameters)

        self.assertEquals(expected_status, response.status_code)
        self.assertEquals(expected_messages, response.content.decode())
        self.assertEquals("text/plain", response.headers['Content-Type'])

    def test_login_username_required(self):
        self._do_test_validation({
            'password': "FooBar"
        }, "Username: This field is required.")

    def test_login_password_required(self):
        self._do_test_validation({
            'username': "harianja"
        }, "Password: This field is required.")

    def test_login_username_password_required(self):
        self._do_test_validation({},
        "Username: This field is required.\nPassword: This field is required.")

    def test_login_success(self):
        DjangoUserModel.objects.create_user(
            username="harianja",
            password="123456")

        response = self.client.post("/", {'username': "harianja", 'password': "123456"})

        self.assertIn(SESSION_KEY, self.client.session)
        self.assertEquals(302, response.status_code)
        self.assertEquals("/", response.url)

    def test_login_invalid_credentials(self):
        DjangoUserModel.objects.create_user(
            username="harianja",
            password="123456")

        response = self.client.post("/", {'username': "harianja", 'password': "13456"})

        self.assertEquals(403, response.status_code)
        self.assertEquals(
            "Authentication failed, please check your username or password",
            response.content.decode())

    def test_login_redirect_if_already_login(self):
        DjangoUserModel.objects.create_user(
            username="harianja",
            password="123456")

        self.client.post("/", {'username': "harianja", 'password': "123456"})

        response = self.client.post("/", {})
        self.assertIn(SESSION_KEY, self.client.session)
        self.assertEquals(302, response.status_code)
        self.assertEquals("/", response.url)
