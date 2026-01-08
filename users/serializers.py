from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only =True)
    
    
    
    class Meta:
        model = User
        fields = ['id', 'username','email','password']
        
        
        
    def create(self, validated_data):
        user = User(
            username = validated_data['username'],
            email = validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password =  serializers.CharField(write_only =True)
    
    
    def validate(self,data):
        user = authenticate(
            email = data['email'],
            password = data['password']
        )
    
    
        if not user:
            raise serializers.ValidationError('invalid email or password')
        
        
        if user.is_blocked:
            raise serializers.ValidationError("User is blocked")
        
        
        return user