from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS
from config import settings

class IsRightKey(BasePermission):
    # header에 키 입력 맞게 해야 모든 API 허용
    def has_permission(self, request, view):
        secret_key = getattr(settings, 'SECRET_KEY', None)
        # 헤더에서 사용자가 제공한 키를 가져오기.
        provided_key = request.headers.get('X-Secret-Key')

        return provided_key == secret_key

class IsWriterOrReadonly(BasePermission):
    # 게시글 작성자만 수정, 삭제 가능. 
    # 이외의 사용자는 읽기 권한만 갖도록.
    def has_permission(self, request, view):
        # header에 비밀키를 받아 맞게 입력한 사용자만 모든 API 요청을 허용해야한다
        secret_key = getattr(settings, 'SECRET_KEY', None)
        provided_key = request.headers.get('X-Secret-Key')
        if provided_key != secret_key:
            return False
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS: #SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS")
            return True
        # PUT, DELETE (수정, 삭제) 요청에 대해, 작성자일 경우에만 요청 허용.
        return obj.writer == request.user
