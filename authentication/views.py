from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from django.contrib.auth import logout
from .models import User
from .permissions import IsOwner
from .serializers import (UserRegisterSerializer, UserLoginSerializer, UserDetailsSerializer,
                          UserUpdateSerializer, UserPasswordChangeSerializer)


class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = User.objects.get(username=serializer.validated_data['username'])
            except User.DoesNotExist:
                return Response({'password': 'Пользователя не существует'}, status=status.HTTP_400_BAD_REQUEST)
            if not user.check_password(serializer.validated_data['password']):
                return Response({'password': 'Пользователя не существует'}, status=status.HTTP_400_BAD_REQUEST)
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(APIView):
    def post(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response({'error': 'Token was not provided'}, status=status.HTTP_400_BAD_REQUEST)
        Token.objects.filter(user=user).delete()
        logout(request)
        return Response({'detail': 'Successfully logged out.'}, status=status.HTTP_200_OK)


class UserDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserDetailsSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = [IsOwner, IsAuthenticated]

    def get_object(self):
        return self.request.user

    def perform_update(self, serializer):
        serializer.save()


class UserPasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def post(self, request):
        serializer = UserPasswordChangeSerializer(data=request.data, context={"user": self.get_object()})
        if serializer.is_valid():
            request.user.set_password(serializer.validated_data['new_password'])
            request.user.save()
            return Response({'detail': 'Password changed successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

