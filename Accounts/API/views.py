from django.core.mail import send_mail
from django.core.validators import validate_email
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate, login

from Accounts.API.serializers import PasswordRestConfirmSerializer, passwordChangeSerializer,ProfileSerializer
from Reservation.API.serializers import ReservationSerializer
from Reservation.models import Reservation
from Accounts.API.serializers import user_creation_serializer
from Accounts.models import User, Profile
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)


@api_view(['POST'])
def guest_registration(request):
    if request.method == "POST":
        serializer = user_creation_serializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            profile = Profile(
                fname=request.data.get("fname"),
                nationality=request.data.get("nationality"),
                lname=request.data.get("lname"),
                organization=request.data.get("organization"),
                email=request.data.get("email"),
                homeAddress=request.data.get("address"),
                phone=request.data.get("phone"),
            )
            profile.user = account
            profile.save()
            serializer = ProfileSerializer(profile)
            token = Token.objects.get(user=account).key
            data['token'] = token
            data["data"] = serializer.data
        else:
            data = serializer.errors
        return Response(data)


# Manager Registration

@api_view(['POST'])
def manager_registration(request):
    if request.method == "POST":
        serializer = user_creation_serializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            account.is_manager = True
            account.is_staff = True
            account.save()
            profile = Profile(
                fname=request.data.get("fname"),
                nationality=request.data.get("nationality"),
                lname=request.data.get("lname"),
                organization=request.data.get("organization"),
                email=request.data.get("email"),
                homeAddress=request.data.get("address"),
                phone=request.data.get("phone"),
            )
            profile.user=account
            profile.save()
            serializer = ProfileSerializer(profile)
            token = Token.objects.get(user=account).key
            data['token'] = token
            data["data"] = serializer.data
        else:
            data = serializer.errors
        return Response(data)


# ##################################### end of registration ####################################
@api_view(["POST"])
def login_view(request):
    email = request.data.get("email")
    password = request.data.get("password")
    if email is None or password is None:
        return Response({'error': 'Please provide both username and password'}, status=HTTP_400_BAD_REQUEST)
    user = authenticate(request, email=email, password=password)
    data = {}
    if not user:
        data["error"] = 'Invalid Credentials'
        return Response(data, status=HTTP_404_NOT_FOUND)
    else:
        login(request, user)
        data = {}
        serializer = ProfileSerializer(Profile.objects.get(user=user))
        reservations = Reservation.objects.filter(guest=user)
        token, _ = Token.objects.get_or_create(user=user)
        data['token'] = token.key
        data["data"] = serializer.data
        if reservations:
           data["reservations"] = ReservationSerializer(reservations, many=True).data
        return Response(data, status=HTTP_200_OK)


# #####################password reset view############################################
@api_view(['POST', ])
def PasswordRestView(request):
    # checking the validity of the email entered by the user
    def validate_email_address(email):
        try:
            # if email is valid the code should continue
            validate_email(email)
            return True
        except validationError:
            # else it should through error
            return False

    email = request.data.get("email")

    # if the function for checking validity returns true,
    if validate_email_address(email):
        # search in the database for user with that email
        user = User.objects.get(email=email)
        data = {}
        # if the user exist,
        if user:
            # encode the pk of that user
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            # get the token of the user
            token = Token.objects.get(user=user)
            # email template('email/email_body.html') with parameters of user, uid, token .........
            msg_html = render_to_string('email/email_body.html',
                                        {'user': user, 'domain': "http://localhost:3000",
                                         'site_name': 'Hotel Reservation', 'uid': uid, 'token': token})

            # send email function
            send_mail(
                'Password reset for Hostels',
                "",
                'some@sender.com',
                [user.email],
                html_message=msg_html,
            )
            # if email sending is successful, return success message and token
            data["success"] = "A reset link has been sent to " + user.email + ". Open your email to reset your password"
            data['token'] = token.key
            data['uid'] = uid
        else:
            data["failure"] = "user can not be found"
    return Response(data)


@api_view(['POST', ])
# password reset confirm view
def passwordResetConfirmView(request, uidb64, token):
    # putting data into PasswordRestConfirmSerializer for validity check
    serializer = PasswordRestConfirmSerializer(data=request.data)
    # decoding the uid parsed into the url to get the pk of the user
    uid = urlsafe_base64_decode(uidb64)
    # checking if there is a user with that pk
    user = User.objects.get(pk=uid)
    # get the token of that user
    check_token = Token.objects.get(key=token)
    print(check_token)
    data = {}
    # if the user exist and the token is the same as the one in parsed into the url,
    if user and check_token:
        # check the validity of PasswordRestConfirmSerializer , if valid
        if serializer.is_valid():
            # there is a function in the PasswordRestConfirmSerializer serializer class
            # we assign new_password to the valid form of that function because it contains the new
            # password from the reset form
            new_password = serializer.new_password_validation()
            # overwriting the password filed of the user with the new password
            user.set_password(new_password)
            # delete the token of the user
            Token.objects.get(user=user).delete()
            # save the user instance
            user.save()
            # create a new token for the user
            token = Token.objects.create(user=user)
            # return the token and the success message when everything is successful
            data["success"] = "your password has been successfully reset"
            data['token'] = token.key

        else:
            data = serializer.error
    return Response(data)


@api_view(['POST', ])
@authentication_classes([TokenAuthentication, ])
@permission_classes([IsAuthenticated])
def passwordChangeView(request):
    user = request.user
    data = request.data
    serializer = passwordChangeSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        associated_user = User.objects.get(username=user)
        # password from the change form
        new_password = serializer.new_password_validation()
        # overwriting the password filed of the user with the new password
        associated_user.set_password(new_password)
        associated_user.save()
        token = Token.objects.get(user=user)
        # return the token and the success message when everything is successful
        data["success"] = "your password has been successfully changed"
        data['token'] = token.key
    else:
        data = serializer.error
    return Response(data)

# user profile view
@api_view(['PATCH', 'GET'])
@authentication_classes([TokenAuthentication, ])
@permission_classes([IsAuthenticated])
def profile(request):
    if request.method == 'GET':
        data={}
        profile = Profile.objects.filter(user=request.user)
        if profile:
            serializer = ProfileSerializer(profile,many=True)
            data["data"] = serializer.data
        else:
            data["error"] = "the data is invalid"
        return Response(data)
    else:
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(profile, request.data, partial=True)
        data = {}
        if serializer.is_valid():
            serializer.save()

            data["data"] = serializer.data
        else:
            data["failure"] = "we could not update your info due to some errors"

        return Response(data)
