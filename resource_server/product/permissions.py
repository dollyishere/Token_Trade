from rest_framework.permissions import BasePermission


class IsManagerForProduct(BasePermission):
    """Product 용 권한 클래스"""

    def has_permission(self, request, view):
        # 요청의 사용자 정보가 올바르게 설정되었는지 확인
        if hasattr(request, "user") and request.user:
            user_role = request.user.get("role", "none")
            # 관리자는 모든 액션 접근 가능
            if user_role == "manager":
                return True
            # 고객은 목록 조회 및 단일 조회만 가능
            if view.action in ["list", "retrieve"]:
                return True
        return False

    def has_object_permission(self, request, view, obj):
        # 요청의 사용자 정보가 올바르게 설정되었는지 확인
        if hasattr(request, "user") and request.user:
            user_role = request.user.get("role", "none")
            # 관리자는 모든 객체에 접근 가능
            return user_role == "manager"
        return False
