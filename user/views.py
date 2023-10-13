from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect
from rest_framework import permissions
from rest_framework.decorators import api_view

from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.reverse import reverse

from user.models import Contact, SpamNumber
from user.serializer import (
    ContactCreateSerializer, SpamSerializer,
    UserRegistrationSerializer, ContactItemSerializer
)


class CreateContactApiView(CreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(added_by=user)


class CreateSpamApiView(CreateAPIView):
    queryset = SpamNumber.objects.all()
    serializer_class = SpamSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        spam = serializer.save(added_by=self.request.user)
        contact_instance = Contact.objects.filter(phone_number=spam.phone_number).first()
        if contact_instance:
            contact_instance.no_of_spam_count += 1
            contact_instance.save()
        else:
            c = Contact()
            c.name = spam.name
            c.phone_number = spam.phone_number
            c.no_of_spam_count = 1
            c.added_by = self.request.user
            c.save()


class UserRegistrationAPIView(CreateAPIView):
    """

    This View expect username field to be the 10 digit mobile number

    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

    def perform_create(self, serializer: UserRegistrationSerializer):
        # user = serializer.save()
        # user.set_password(serializer.validated_data['password'])
        # user.save()

        user = User.objects.create_user(**serializer.validated_data)
        if Contact.objects.filter(phone_number=user.username).exists():
            return
        c = Contact()
        c.name = user.get_full_name()
        c.phone_number = user.username
        c.added_by = user
        c.save()


class ContactSearchView(ListAPIView):
    queryset = Contact.objects.all().order_by('name')
    serializer_class = ContactItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        q = super().get_queryset()
        name = self.request.GET.get("name")
        number = self.request.GET.get("phone_number")
        if name:
            q = q.filter(
                Q(name__istartswith=name) | Q(name__icontains=name)
            )
        if number:
            q = q.filter(phone_number=number)       # exact match
        return q


@api_view()
def api_list(request):
    base_url = request.build_absolute_uri('/')
    base_url = base_url[:-1]
    # base_url = "http://localhost:8000/"
    return Response({
        "login": base_url + reverse('rest_login'),
        "logout": base_url + reverse('rest_logout'),
        "profile": base_url + reverse('rest_user_details'),
        "user registration": base_url + reverse('user_registration'),

        "create contact": base_url + reverse('create_contact'),
        "mark as spam": base_url + reverse('create_spamcontact'),
        "search contact by name": base_url + reverse('contact_search') + '?name=Neha',
        "search contact by number": base_url + reverse('contact_search') + '?phone_number=9876543210',
        # "search": reverse('search'),
    })


def homepage(request):
    return redirect(reverse('apidoc'))




