"""
Serializers for the user API View.
"""
from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from django.utils.translation import gettext as _


from rest_framework import serializers


####################################??????????
# alle serializer erlauben eine Validierung und können Daten sichern
class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    class Meta:
        # this is where we tell the django rest framework, the model
        # and the fields and any additional arguments that we want
        # to pass to the serialize set. The serialized needs to know
        # which model its representing and the way it does that as
        # we tell it, model equals get use a model.
        # so this serialize is going to be for our user model
        model = get_user_model()
        fields = ['email', 'password', 'name']
        # that is a dictionary that allows us to provide extra metadata to the different fields.
        # This tells Django rest framework things like do we want the field
        # to be write only or read only? or a minimum length on the value?
        # the user can set the password, but there wont be a value returned from the api response.
        # they can write the value but cant read the password (thats for secruity)
        # wenn die min_length : 5 nicht erfüllt ist, dann gibt es einen BAD_REQUEST 400 zurück
        # in dem Fall würde es die create Funktion (siehe unten) nicht aufrufen
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create and return a user with encrypted password."""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update and return user."""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token."""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """Validate and authenticate the user."""
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs