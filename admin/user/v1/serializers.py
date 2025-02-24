from rest_framework import serializers

from user.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','email', 'firstname', 'lastname', 'password','is_active')
        extra_kwargs = {'password': {'write_only': True}}

