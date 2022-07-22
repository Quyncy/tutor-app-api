"""
Views for the user API.
"""
from rest_framework import generics
# das ist aus der Datei, die zuvor erstellt wurde user/serializers
from user.serializers import UserSerializer

#the Create api view handles a hasty post request thats
# designed for creating objects
class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""
    serializer_class = UserSerializer