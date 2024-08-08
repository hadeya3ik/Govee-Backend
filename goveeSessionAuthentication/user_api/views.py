from django.contrib.auth import get_user_model, login, logout
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserRegisterSerializer, UserLoginSerializer, UserSerializer
from rest_framework import permissions, status 
from .validations import custom_validation, validate_email, validate_password
from django.contrib.auth import get_user_model
UserModel = get_user_model()
from django.contrib.auth.models import User


# class UserRegister(APIView):
#     permission_classes = (permissions.AllowAny,)
#     def post(self, request):
#         clean_data = custom_validation(request.data)
#         serializer = UserRegisterSerializer(data=clean_data)
#         if serializer.is_valid(raise_exception=True):
#             user = serializer.create(clean_data)
#             if user: 
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(status=status.HTTP_400_BAD_REQUEST)


class UserRegister(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request):
        email = request.data['email'].strip()
        username = request.data['username'].strip()
        password = request.data['password'].strip()

        if not email or UserModel.objects.filter(email=email).exists():
            return Response({'detail': 'Email already exists on an account'}, status=status.HTTP_409_CONFLICT)
        if not password or len(password) < 8:
            return Response({'detail': 'choose another password, min 8 characters'}, status=status.HTTP_400_BAD_REQUEST)
        if not username:
            return Response({'detail': 'choose another username'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = UserRegisterSerializer(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            user = serializer.create(request.data)
            if user: 
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else : 
                return Response({'detail': 'user can not be made'}, status=status.HTTP_400_BAD_REQUEST)
                 
        
        return Response({'detail': 'worst case error'}, status=status.HTTP_400_BAD_REQUEST)


# class UserLogin(APIView):
#     permission_classes = (permissions.AllowAny, )
#     authentication_classes = (SessionAuthentication, )

#     def post(self, request):
#         data = request.data
#         assert validate_email(data)
#         assert validate_password(data)

#         serializer=UserLoginSerializer(data=data)
#         if serializer.is_valid(raise_exception=True):
#             user = serializer.check_user(data)
#             login(request, user)
#             return Response(serializer.data, status=status.HTTP_200_OK) 


# class UserLogin(APIView):
#     permission_classes = (permissions.AllowAny,)
#     authentication_classes = (SessionAuthentication,)

#     def post(self, request):
#         data = request.data
#         serializer = UserLoginSerializer(data=data)
        
#         if serializer.is_valid():
#             user = serializer.check_user(serializer.validated_data)
#             if user:
#                 login(request, user)
#                 return Response(serializer.data, status=status.HTTP_200_OK)
#             else:
#                 return Response({'detail': "Username or password is invalid."}, status=status.HTTP_401_UNAUTHORIZED)
        
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLogin(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (SessionAuthentication,)

    def post(self, request):
        data = request.data
        serializer = UserLoginSerializer(data=data)
        
        if serializer.is_valid():
            user = serializer.check_user(serializer.validated_data)
            if user:
                login(request, user)
                print(request.session.session_key)  # Debug: Print session key
                return Response({'message': 'Logged in successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'detail': "Username or password is invalid."}, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLogout(APIView):
	permission_classes = (permissions.AllowAny,)
	authentication_classes = ()
	def post(self, request):
		logout(request)
		return Response(status=status.HTTP_200_OK)

class UserView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response({'user': serializer.data}, status=status.HTTP_200_OK)


# class UserView(APIView):
#     permission_classes = (permissions.IsAuthenticated,)
#     authentication_classes = (SessionAuthentication,)

#     def get(self, request):
#         if request.user.is_authenticated:
#             serializer = UserSerializer(request.user)
#             return Response({'user': serializer.data}, status=status.HTTP_200_OK)
#         else:
#             return Response({'error': 'User is not authenticated'}, status=status.HTTP_403_FORBIDDEN)

