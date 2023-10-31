from django.contrib.auth import authenticate

from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.serializers import Serializer, CharField, EmailField


class LoginSerializer(Serializer): # noqa
    email = EmailField(required=True)
    password = CharField(required=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email,
                                password=password)
            if user is None:
                raise AuthenticationFailed('Invalid email or password')
        else:
            raise ValidationError()

        data['user'] = user
        return data
