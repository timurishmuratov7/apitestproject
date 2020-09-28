import pytest
from django.urls import reverse
from registration.utils import create_user_account
from mainapp.utils import create_album_in_db

from django.contrib.auth.models import User
from mainapp.models import Album


@pytest.mark.django_db
def test_user_create():
  create_user_account('lennon@thebeatles.com', 'johnpassword')
  assert User.objects.count() == 1

@pytest.mark.django_db
def test_album_create():
  author = create_user_account('lennon@thebeatles.com', 'johnpassword')
  create_album_in_db('my_album', author)
  assert Album.objects.count() == 1

@pytest.mark.django_db
@pytest.mark.parametrize(
   "email, password, status_code", [
       ("", "", 400),
       ("", "strong_pass", 400),
       ("user@example.com", "", 400),
       ("user@example.com", "invalid_pass", 400),
       ("lennon@thebeatles.com", "johnpassword", 200),
   ]
)
def test_login_data_validation(
   email, password, status_code, api_client
):
   user = create_user_account("lennon@thebeatles.com", "johnpassword")
   data = {
       "email": email,
       "password": password
   }
   print(User.objects.all())
   url = reverse('auth-login')
   print(data)
   response = api_client.post(url, data=data, format = 'json')
   print(response.data)
   assert status_code == response.status_code

def test_logout(api_client):
      url = reverse('auth-logout')
      response = api_client.post(url)
      assert response.status_code == 200
