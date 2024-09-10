from rest_framework.permissions import BasePermission


class IsManagerOrCustomerForOrder(BasePermission):
    """Order 용 권한 클래스"""

    def has_permission(self, request, view):
        user_role = request.user.role

        if user_role == "manager":
            return True  # 관리자는 모든 액션 접근 가능
        if view.action in ["list", "retrieve", "create", "partial_update"]:
            return True  # 고객은 목록 조회, 단일 조회, 생성, 부분 업데이트 가능
        return False  # 그 외 액션 접근 불가

    def has_object_permission(self, request, view, obj):
        # 관리자는 모든 객체에 접근 가능
        if request.user.role == "manager":
            return True
        # 일반 사용자는 본인 주문에만 접근 가능
        return obj.customer == request.user
