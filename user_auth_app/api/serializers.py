from rest_framework import serializers
from django.conf import settings


class RegistrationSerializer(serializers.ModelSerializer):
    repeated_password = serializers.CharField(write_only=True)
    
    class Meta:
        model = settings.AUTH_USER_MODEL
        fields = ['email', 'password', 'repeated_password']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def save(self):
        pw = self.validated_data['password']
        repeated_pw = self.validated_data['repeated_password']

        if pw != repeated_pw:
            raise serializers.ValidationError({'error': 'Passwords don\'t match'})
        
        try:
            existing_user = settings.AUTH_USER_MODEL.objects.get(email=self.validated_data['email'])
        except:
            existing_user = None
        
        if existing_user:
            print('existing User with that email: ', existing_user)
            raise serializers.ValidationError({'error': 'Email already exists!'})
        else:
            account = settings.AUTH_USER_MODEL(email=self.validated_data['email'], username=self.validated_data['username'])
            account.set_password(pw)
            account.save()
            return account
