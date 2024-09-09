from rest_framework.permissions import BasePermission


class IsManagerForProduct(BasePermission):
    """Product 용 권한 클래스"""

    def has_permission(self, request, view):
        # 관리자는 모든 액션 접근 가능
        if request.user.role == "manager":
            return True
        if view.action in ["list", "retrieve"]:
            return True  # 고객은 목록 조회, 단일 조회만 가능
        return False  # 그 외 액션 접근 불가

    def has_object_permission(self, request, view, obj):
        # 관리자는 모든 객체 접근 가능
        return request.user.role == "manager"
