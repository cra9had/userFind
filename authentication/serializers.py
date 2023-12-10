from rest_framework import serializers
from django.contrib.auth import password_validation
from rest_framework.authtoken.models import Token
from rest_captcha.serializers import RestCaptchaSerializer
from .models import User


class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'balance', 'avatar', 'username']


class UserRegisterSerializer(RestCaptchaSerializer):
    username = serializers.CharField(max_length=16, write_only=True)
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)
    token = serializers.CharField(read_only=True)
    captcha_key = serializers.CharField(max_length=64, write_only=True)
    captcha_value = serializers.CharField(max_length=8, trim_whitespace=True, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'password_confirm', 'token']

    def validate_username(self, value):
        # Check if a user with the same username (case-insensitive) already exists
        existing_users = User.objects.filter(username__iexact=value)
        if existing_users.exists():
            raise serializers.ValidationError("Username is already taken.")

        return value

    def validate_password(self, value):
        try:
            password_validation.validate_password(value)
        except password_validation.ValidationError:
            raise serializers.ValidationError("Password is too weak")
        return value

    def validate_password_confirm(self, value):
        if self.initial_data['password'] != value:
            raise serializers.ValidationError("Passwords do not match.")
        return value

    def create(self, validated_data):
        user = User(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        serializer_data = self.to_representation(User)
        serializer_data["token"] = Token.objects.create(user=user).key
        return serializer_data


class UserLoginSerializer(RestCaptchaSerializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'avatar']

    def update(self, instance, validated_data):
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.save()
        return instance


class UserPasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_old_password(self, value):
        user = self.context.get("user")
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect")

    def validate_new_password(self, value):
        try:
            password_validation.validate_password(value)
        except password_validation.ValidationError:
            raise serializers.ValidationError("Password is too weak")
        return value
