from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,

)

from Accounts.models import User, Staff


class user_creation_serializer(serializers.ModelSerializer):
    email = serializers.EmailField(allow_blank=False)
    password = serializers.CharField(min_length=6, write_only=True, required=False, style={'input_type': 'password'})
    password2 = serializers.CharField(min_length=6, write_only=True, required=False, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['email',  'password', 'password2',  'is_manager', "fname", "lname", "isBlackListed", "phone", "nationality", "homeAddress", "is_accountant"]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        account = User(
            email=self.validated_data['email'],
            fname=self.validated_data['fname'],
            lname=self.validated_data['lname'],
            phone=self.validated_data['phone'],
            nationality=self.validated_data['nationality'],
            homeAddress=self.validated_data['homeAddress'],
            username=self.validated_data['fname']
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.validationError({'password': 'passwords must match.'})
        account.set_password(password)
        account.save()
        return (account)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


# create a class serializer for passwordresetview

class PasswordRestSerializer(serializers.Serializer):
    email = serializers.EmailField()


# create a class serializer of passwordresetconfirm view
class PasswordRestConfirmSerializer(serializers.Serializer):
    new_password1 = serializers.CharField(min_length=4, write_only=True, required=True,
                                          style={'input_type': 'password'})
    new_password2 = serializers.CharField(min_length=4, write_only=True, required=True,
                                          style={'input_type': 'password'})

    def new_password_validation(self):
        new_password1 = self.validated_data['new_password1']
        new_password2 = self.validated_data['new_password2']
        if new_password1 and new_password2:
            if new_password1 != new_password2:
                return Response({'error': 'Please provide both password must match'}, status=HTTP_400_BAD_REQUEST)
            return new_password1


# password change serializer

class passwordChangeSerializer(serializers.Serializer):
    new_password1 = serializers.CharField(min_length=4, write_only=True, required=True,
                                          style={'input_type': 'password'})
    new_password2 = serializers.CharField(min_length=4, write_only=True, required=True,
                                          style={'input_type': 'password'})

    def new_password_validation(self):
        new_password1 = self.validated_data['new_password1']
        new_password2 = self.validated_data['new_password2']
        if new_password1 and new_password2:
            if new_password1 != new_password2:
                return Response({'error': 'Please provide both password must match'}, status=HTTP_400_BAD_REQUEST)
            return new_password1

class userSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'is_manager', "fname", "lname", "isBlackListed", "phone", "nationality", "homeAddress", "is_accountant", "username"]

class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ['email',  "fname", "lname", "phone", "nationality", "homeAddress", "job", "idNumber"]
