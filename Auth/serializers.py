
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
# class UserSerializer(serializers.ModelSerializer):
#     username = serializers.CharField()
#     password = serializers.CharField(min_length=8, write_only=True)

#     class Meta:
#         model = User
#         fields = ('usrname', 'password')
#         extra_kwargs = {'password': {'write_only': True}}

# def create(self, validated_data):
#     password = validated_data.pop('password', None)
#     instance = self.Meta.model(**validated_data)
#     if password is not None:
#         instance.set_password(password)

#     instance.save()
#     return instance


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        # Add extra responses here
        user = {}
        user['id'] = self.user.id
        user['username'] = self.user.username
        user['first_name'] = self.user.first_name
        user['last_name'] = self.user.last_name

        #self.user.groups.values_list('name', flat=True)
        data['user'] = user
        return data


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_message = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):

        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            self.fail('bad_token')
