from django.contrib import admin
from django.urls import path

from user.views import CreateContactApiView, CreateSpamApiView, UserRegistrationAPIView, ContactSearchView

urlpatterns = [
    path("create/contact/", CreateContactApiView.as_view(), name='create_contact'),
    path("create/spam-contact/", CreateSpamApiView.as_view(), name='create_spamcontact'),
    path("registration/", UserRegistrationAPIView.as_view(), name='user_registration'),
    path("search/", ContactSearchView.as_view(), name='contact_search')
]
