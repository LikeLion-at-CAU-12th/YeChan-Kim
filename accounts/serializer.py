from rest_framework_simplejwt.serializers import RefreshToken
from rest_framework import serializers
from .models import User

# 모델이랑 관련된 parameter 넣을 거니까 Serializer가 아닌 ModelSerializer 사용
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required = True)
    username = serializers.CharField(required = True)
    email = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['password', 'username', 'email']

    def save(self, request):

        user = User.objects.create(
            username = self.validated_data['username'],
            email=self.validated_data['email'],
        )

        #password 암호화
        user.set_password(self.validated_data['password'])
        user.save()

        return user
    
    def validate(self, data):
        email = data.get('email', None)         #None이 있어야 email이 없어도 에러 안 뜸.

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('email already exists')
        
        return data
    
class AuthSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['username', 'password']

    def validate(self, data):
        username = data.get("username", None)
        password = data.get("password", None)

        user = User.get_user_or_none_by_username(username=username)

        if user is None:
            raise serializers.ValidationError("user account not exist")
        else:
            if not user.check_password(raw_password=password):
                raise serializers.ValidationError("wrong password")

        token = RefreshToken.for_user(user)
        refresh_token = str(token)
        access_token = str(token.access_token)

        data = {
            "user": user,
            "refresh_token": refresh_token,
            "access_token": access_token,
        }

        return data