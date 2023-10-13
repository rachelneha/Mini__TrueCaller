from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from user.models import Contact, SpamNumber, User


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('first_name', 'last_name', 'username', 'password', 'email')
#


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    username = serializers.CharField(
        label="Mobile Number", help_text="Enter your 10 digit mobile number without std code."
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def validate_username(self, value):
        if not value.isdigit() or len(value) != 10:
            raise serializers.ValidationError("Username must be a 10-digit mobile number.")
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This mobile number is already registered.")
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must have at least 8 characters")
        return value
        # return make_password(value)


class ContactItemSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()
    is_spam = serializers.SerializerMethodField()

    class Meta:
        model = Contact
        fields = ('id', 'name', 'phone_number', 'email', 'is_spam', 'no_of_spam_count')

    def get_email(self, instance: Contact):
        user = User.objects.all().filter(username=instance.phone_number).first()
        if user:
            return user.email

    def get_is_spam(self, instance: Contact):
        return instance.no_of_spam_count >= 5


class ContactCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = ('name', 'phone_number' )


class SpamSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        phone_number = attrs['phone_number']
        request = self.context['request']
        user = request.user
        if SpamNumber.objects.all().filter(phone_number=phone_number, added_by=user):
            raise serializers.ValidationError("Already saved as spam by you")
        return attrs

    def validate_phone_number(self, value):
        if not value.isdigit() or len(value) != 10:
            raise serializers.ValidationError("Phone Number must be a 10-digit mobile number.")
        return value

    class Meta:
        model = SpamNumber
        fields = ('name', 'phone_number')



