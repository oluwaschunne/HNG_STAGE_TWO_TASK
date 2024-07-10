from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from .models import User, Organisation
from .serializers import UserSerializer, OrganisationSerializer, UserRegistrationSerializer, UserLoginSerializer
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
import jwt
from datetime import datetime, timedelta
from django.conf import settings

# Create your views here.
def create_jwt_token(user):
    payload = {
        'userId': user.userId,
        'email': user.email,
        'exp': datetime.utcnow() + timedelta(days=1),
        'iat': datetime.utcnow(),
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token


class RegisterView(APIView):
    def post(self, request):
        data = request.data
        errors = []

        if not data.get('firstName'):
            errors.append({"field": "firstName", "message": "First name is required"})
        if not data.get('lastName'):
            errors.append({"field": "lastName", "message": "Last name is required"})
        if not data.get('email'):
            errors.append({"field": "email", "message": "Email is required"})
        if not data.get('password'):
            errors.append({"field": "password", "message": "Password is required"})

        if errors:
            return Response({"errors": errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
            user = serializer.save()

            org_name = f"{user.first_name}'s Organisation"
            organisation = Organisation.objects.create(name=org_name)
            organisation.users.add(user)

            token = create_jwt_token(user)
            return Response({
                "status": "success",
                "message": "Registration successful",
                "data": {
                    "accessToken": token,
                    "user": serializer.data
                }
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status": "Bad request",
            "message": "Registration unsuccessful",
            "statusCode": 400,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        data = request.data
        email = data.get('email')
        password = data.get('password')
        user = authenticate(username=email, password=password)
        if user is not None:
            token = create_jwt_token(user)
            return Response({
                "status": "success",
                "message": "Login successful",
                "data": {
                    "accessToken": token,
                    "user": UserSerializer(user).data
                }
            })
        return Response({
            "status": "Bad request",
            "message": "Authentication failed",
            "statusCode": 401
        }, status=status.HTTP_401_UNAUTHORIZED)

class UserDetailView(APIView):
    def get(self, request, userId):
        try:
            user = User.objects.get(userId=userId)
            serializer = UserSerializer(user)
            return Response({
                'status': 'success',
                'message': 'User details fetched successfully',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({
                'status': 'Not found',
                'message': 'User does not exist',
                'statusCode': status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_404_NOT_FOUND)

class OrganisationListView(APIView):
    def get(self, request):
        organisations = Organisation.objects.filter(users=request.user)
        serializer = OrganisationSerializer(organisations, many=True)
        return Response({
            'status': 'success',
            'message': 'Organisations fetched successfully',
            'data': {
                'organisations': serializer.data
            }
        }, status=status.HTTP_200_OK)

class OrganisationDetailView(APIView):
    def get(self, request, orgId):
        try:
            organisation = Organisation.objects.get(orgId=orgId, users=request.user)
            serializer = OrganisationSerializer(organisation)
            return Response({
                'status': 'success',
                'message': 'Organisation details fetched successfully',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        except Organisation.DoesNotExist:
            return Response({
                'status': 'Not found',
                'message': 'Organisation does not exist or you do not have permission',
                'statusCode': status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_404_NOT_FOUND)

class CreateOrganisationView(APIView):
    def post(self, request):
        serializer = OrganisationSerializer(data=request.data)
        if serializer.is_valid():
            organisation = serializer.save()
            organisation.users.add(request.user)
            return Response({
                'status': 'success',
                'message': 'Organisation created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'status': 'Bad request',
            'message': 'Failed to create organisation',
            'statusCode': status.HTTP_400_BAD_REQUEST,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class AddUserToOrganisationView(APIView):
    def post(self, request, orgId):
        data = request.data
        try:
            organisation = Organisation.objects.get(org_id=org_id, users=request.user)
            user_id = data.get('userId')
            try:
                user = User.objects.get(userId=user_id)
                organisation.users.add(user)
                return Response({
                    'status': 'success',
                    'message': 'User added to organisation successfully'
                }, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({
                    'status': 'Not found',
                    'message': 'User does not exist',
                    'statusCode': status.HTTP_404_NOT_FOUND
                }, status=status.HTTP_404_NOT_FOUND)
        except Organisation.DoesNotExist:
            return Response({
                'status': 'Not found',
                'message': 'Organisation does not exist or you do not have permission',
                'statusCode': status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_404_NOT_FOUND)