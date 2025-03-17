from rest_framework import serializers
from users_app.models import CustomUser


class RegistrationSerializer(serializers.ModelSerializer):
    repeated_password = serializers.CharField(write_only=True)
    
    class Meta:
        model = CustomUser
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
        
        if CustomUser.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError({'error': 'Email already exists!'})
        
        account = CustomUser(email=self.validated_data['email'], username=self.validated_data['email'])
        account.set_password(pw)
        account.save()
        return account


class ForgotPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email']
    
    def validate_email(self, value):
        if not CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError('User with this email does not exist!')
        return value


class ResetPasswordSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'new_password']
    
    def validate_email(self, value):
        if not CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError('User with this email does not exist!')
        return value


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'confirmed', 'last_login', 'date_joined']
