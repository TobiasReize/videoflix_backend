from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
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

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError({'msg': ['Email already exists!']})
        return value

    def validate_repeated_password(self, value):
        password = self.initial_data.get('password')
        if password and value and password != value:
            raise serializers.ValidationError({'msg': ['Passwords don\'t match']})
        return value

    def save(self):
        """
        Creates a new CustomUser instance.
        """
        pw = self.validated_data['password']
        email = self.validated_data['email']
        username = email.split('@')[0]
        account = CustomUser(email=email, username=username)
        account.set_password(pw)
        account.save()
        return account


class ForgotPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email']
    
    def validate_email(self, value):
        if not CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError(['User with this email does not exist!'])
        return value


class ResetPasswordSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(write_only=True)
    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'new_password', 'repeated_password']
    
    def validate_email(self, value):
        if not CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError(['User with this email does not exist!'])
        return value
    
    def save(self):
        """
        Change the user's password to the new password.
        """
        new_pw = self.validated_data['new_password']
        repeated_pw = self.validated_data['repeated_password']
        email = self.validated_data['email']

        if new_pw != repeated_pw:
            raise serializers.ValidationError({'msg': ['Passwords don\'t match']})
        
        user = CustomUser.objects.get(email=email)
        user.set_password(new_pw)
        user.save()
        return user


class UserProfileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'confirmed', 'last_login', 'date_joined']


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'username' in self.fields:
            self.fields.pop('username')

    def validate(self, values):
        email = values.get('email')
        password = values.get('password')

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError({'msg': ['Invalid email or password!']})

        if not user.check_password(password):
            raise serializers.ValidationError({'msg': ['Invalid email or password!']})
        
        data = super().validate({'username': user.username, 'password': password})
        return data
