from django.db import models
from django.contrib.auth.models import AbstractUser

#accounts/models.py

class User(AbstractUser):
    pass

    @staticmethod  #모델 내부 함수. 데이터 직접 소통은 모델 내부 함수에서만.
    def get_user_or_none_by_username(username):
        try:
            return User.objects.get(username=username) #get은 없으면 에러 발생. filter는 없어도 에러 발생 X.
        except Exception:
            return None
        
    @staticmethod  #모델 내부 함수. 데이터 직접 소통은 모델 내부 함수에서만.
    def get_user_or_none_by_email(email):
        try:
            return User.objects.get(email = email)
        except Exception:
            return None